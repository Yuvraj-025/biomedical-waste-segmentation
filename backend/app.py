from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)
# Enable CORS for frontend across local network
CORS(app, resources={r"/*": {"origins": "*"}})

import os

# Load the custom biomedical waste detection model 
# Path points to local models dir in the restructured backend
model_path = os.path.join(os.path.dirname(__file__), 'models', 'best.pt')
model = YOLO(model_path)

@app.route("/", methods=["GET"])
def read_root():
    return jsonify({"message": "Biomedical Waste Detection API is operational"})

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})
        
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files["file"]
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    try:
        image = Image.open(io.BytesIO(file.read())).convert("RGB")
    except Exception as e:
        print(f"Error opening image: {e}")
        return jsonify({"error": "Invalid image file"}), 400

    # Run inference with maximum sensitivity
    # Low conf threshold (0.1) and explicit 768px resolution
    results = model(image, conf=0.1, imgsz=768)
    
    # RAW LOGGING for deep debugging
    print("\n[DEBUG] RAW DETECTIONS FROM MODEL:")
    if results[0].boxes:
        for i, box in enumerate(results[0].boxes):
            name = results[0].names[int(box.cls)]
            conf = float(box.conf)
            print(f"  Det {i}: {name} ({conf:.4f})")
    else:
        print("  No objects found even at 0.1 threshold")
    print("-" * 30 + "\n")
    
    # Precise Biomedical Disposal Mapping
    disposal_map = {
        "-bt- body tissue or organ": "Red Bag (Infectious/Anatomical Waste) - Incineration Required",
        "-ow- organic wastes": "Yellow Bag (Clinical Waste) - Specialized Treatment",
        "-pp- plastic packaging": "Recycle Bin or Non-Infectious Waste Container",
        "-sn- syringe needles": "Sharps Container (Yellow/Puncture-Proof) - Final Disposal: Autoclave",
        "gauze": "Yellow Bag (Clinical Waste) - Incineration",
        "gloves": "Red Bag (Infectious Waste) - Chemical Treatment",
        "mask": "Yellow Bag (Clinical Waste) - Secure Disposal",
        "syringe": "Sharps Container (Yellow) - Handle with Extreme Caution",
        "tweezers": "Sharps Container or Sterilization Bin if Reusable",
        "unknown": "Contain in Biohazard Bag and Request Inspection"
    }

    detections = []
    if results[0].boxes:
        for box in results[0].boxes:
            c_id = int(box.cls)
            name = str(results[0].names[c_id])
            conf = float(box.conf)
            detections.append({"name": name, "confidence": conf})

    # Logic Fix: Prioritize Syringes/Needles if detected with > 25% confidence
    best_detection = detections[0] if detections else {"name": "Unknown", "confidence": 0.0}
    
    critical_classes = ["syringe", "-sn- syringe needles", "gauze", "gloves", "mask", "-bt- body tissue or organ"]
    for det in detections:
        # If a critical class is detected with significant confidence, prefer it over a generic detection
        name_str = str(det["name"]).lower()
        if name_str in critical_classes and float(det["confidence"]) > 0.25:
            best_name_str = str(best_detection["name"]).lower()
            if best_name_str not in critical_classes or float(det["confidence"]) > float(best_detection["confidence"]):
                best_detection = det
                break 

    detected_class = str(best_detection["name"])
    confidence = float(best_detection["confidence"])
    
    # Normalized class name for cleaner UI display
    display_class = detected_class.strip().replace("-", " ").title()
    if not display_class: display_class = "Unknown"

    # Default fallback if class is not in map
    disposal = disposal_map.get(detected_class.lower(), "Contact Waste Management (Standard Protocol)")

    return jsonify({
        "class": display_class,
        "confidence": confidence,
        "all_detections": detections[:3], # Return top 3 for transparency
        "disposal": disposal
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
