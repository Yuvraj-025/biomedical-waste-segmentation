# Biomedical Waste Object Detection System

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Powered by YOLOv8](https://img.shields.io/badge/Powered_by-YOLOv8-blueviolet?style=for-the-badge)

A complete full-stack machine learning application designed to instantly detect, classify, and provide the correct disposal protocols for hazardous biomedical waste using a custom-trained **YOLOv8** computer vision model.

<p>My Role: Connected the model to the backend and helped display the prediction results on the frontend.</p>
---


## 🌟 Key Features

- **Real-Time Inference**: Connects a sleek React frontend to a fast Flask backend for immediate AI predictions.
- **Precise Categorization**: Detects syringes, contaminated gauze, bio-tissue, gloves, and more.
- **Actionable Disposal Guidelines**: Automatically maps detected items to globally recognized waste management protocols (e.g., Red Bag vs. Yellow Sharps Container).
- **Isolated ML Workspace**: Completely segregates the web-application runtime from heavy machine learning datasets and training artifacts.

---

## 📂 Project Architecture

The repository is organized cleanly into three distinct environments:

- **`frontend/`**: The modern web user interface built with **React** and **Vite**. Provides a fast, interactive way to upload images and seamlessly view bounding boxes and disposal instructions.
- **`backend/`**: The lightweight **Flask** API server. It loads the compiled YOLOv8 weights (contained in `backend/models/best.pt`), processes uploaded images, and returns structured JSON predictions and waste management routing.
- **`model_training/`**: The dedicated machine learning research workspace. Contains all necessary scripts, Roboflow datasets, training runs, and raw `.pt` weights used to iteratively train the YOLOv8 model. *(These heavy artifacts are securely ignored by Git to keep the primary repo clean)*.

---

## 🚀 Quick Start (Windows)

The absolute easiest way to start the entire application is to simply double-click the included batch script in the root directory:

```bash
run_app.bat
```
This script will automatically open two terminal windows:
1. One that activates your Python virtual environment (`.venv`) and starts the **Flask Backend** on `http://localhost:5000`.
2. Another that spins up the **React Frontend** on `http://localhost:5173` and instantly opens your default browser!

---

## 🛠️ Manual Setup & Execution

If you prefer to start the services manually to view logs separately or are deploying to a server:

### 1. Start the Flask API (Backend)
Navigate to the root directory and run:
```powershell
# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Start the Flask development server
python backend\app.py
```

### 2. Start the React UI (Frontend)
Open a new terminal and run:
```powershell
cd frontend

# Install dependencies if this is your first time
npm install

# Start the Vite development server
npm run dev -- --open
```

---

## 📚 API Reference

**Endpoint:** `POST /predict`
- **Description:** Accepts an image upload, passes it through the YOLOv8 neural network, and returns the highest confidence detection and its disposal protocol.
- **Payload:** `multipart/form-data` containing a `file` field with the image.
- **Response Format:**
```json
{
  "class": "Syringe",
  "confidence": 0.9588,
  "disposal": "Sharps Container (Yellow) - Handle with Extreme Caution",
  "all_detections": [
    { "name": "syringe", "confidence": 0.9588 },
    { "name": "-bt- body tissue or organ", "confidence": 0.3848 }
  ]
}
```

---

## 🏥 Waste Management Protocol Matrix

The application maps specific detections to the following safety protocols:

| Detected Object | Target Disposal Route |
| :--- | :--- |
| **Syringe / Needles** | 🟡 **Sharps Container** (Yellow/Puncture-Proof) - Autoclave |
| **Gauze / Bandages** | 🟡 **Yellow Bag** (Clinical Waste) - Incineration |
| **Bio-Tissue / Organs** | 🔴 **Red Bag** (Infectious/Anatomical) - Incineration Required |
| **Used Gloves** | 🔴 **Red Bag** (Infectious Waste) - Chemical Treatment |
| **Masks** | 🟡 **Yellow Bag** (Clinical Waste) - Secure Disposal |
| **Organic Wastes** | 🟡 **Yellow Bag** (Clinical Waste) - Specialized Treatment |
| **Tweezers** | 🟡 **Sharps / Sterilization Bin** (If Reusable) |
| **Plastic Packaging** | 🟢 **Recycle Bin** / Non-Infectious Waste |

---

## 🧠 Model Retraining Guide

If you wish to augment the dataset or retrain the model to capture more classes from Roboflow:
1. Ensure your `ROBOFLOW_API_KEY` is set in the `.env` file at the root of the project.
2. Navigate to the `model_training/` directory and use the setup scripts (`scripts/train.py`, `scripts/download_dataset.py`, etc.).
3. Once a new, more accurate epoch is trained, manually copy the resulting `best.pt` file from `model_training/outputs/.../weights/best.pt` directly into the live `backend/models/` directory. 
4. Restart your Flask backend to instantly apply the new model parameters.
