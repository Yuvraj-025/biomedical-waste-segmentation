import argparse
import sys
import os
from pathlib import Path

# Add project root to path so we can import things if needed
# script is in model_training/scripts/
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

def check_dependencies():
    """Ensure seaborn, matplotlib, and pandas are installed."""
    try:
        import seaborn
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        return True
    except ImportError as e:
        print(f"Missing dependency: {e.name}. Attempting to install...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "seaborn", "matplotlib", "pandas"])
            return True
        except Exception as install_error:
            print(f"Failed to install dependencies: {install_error}")
            return False

def generate_confusion_matrix(weights, data_yaml, output_path):
    from ultralytics import YOLO
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    
    print(f"Loading model: {weights}")
    model = YOLO(weights)
    
    print(f"Running validation on: {data_yaml}")
    # val() returns validation results which contain the confusion matrix
    results = model.val(data=data_yaml, plots=False) # We'll do our own plots
    
    try:
        # Access the ConfusionMatrix object
        cm_obj = results.confusion_matrix
        cm = cm_obj.matrix # This is the numpy array
        names = list(results.names.values())
        
        # YOLO confusion matrix includes a background class at the end
        if cm.shape[0] > len(names):
            display_names = names + ["background"]
        else:
            display_names = names

        # Normalize the matrix by row (actual class)
        # Add epsilon to avoid division by zero
        row_sums = cm.sum(axis=1, keepdims=True)
        cm_norm = cm / (row_sums + 1e-7)
        
        # Create the plot
        plt.figure(figsize=(14, 11))
        sns.set_theme(style="whitegrid")
        
        # Create heatmap
        ax = sns.heatmap(
            cm_norm, 
            annot=True, 
            fmt='.2f', 
            cmap='Blues', 
            xticklabels=display_names, 
            yticklabels=display_names,
            square=True,
            cbar_kws={"shrink": .8}
        )
        
        plt.title(f'Confusion Matrix (Normalized)\nModel: {Path(weights).name}', fontsize=18, fontweight='bold', pad=25)
        plt.xlabel('Predicted Class', fontsize=14, labelpad=15)
        plt.ylabel('True Class', fontsize=14, labelpad=15)
        
        # Rotate labels
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(rotation=0, fontsize=10)
        
        plt.tight_layout()
        
        # Save output
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✨ Success! Fresh confusion matrix saved to: {output_path}")
        print(f"Classes evaluated: {len(names)}")
        
    except Exception as e:
        print(f"\n❌ Error processing confusion matrix: {e}")
        import traceback
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description="Professional Confusion Matrix Generator for YOLOv8/v26")
    
    # Auto-detect available models in model_training folder
    available_models = list(project_root.glob("*.pt"))
    default_model = str(available_models[0].name) if available_models else None
    
    parser.add_argument("--weights", type=str, default=default_model, 
                        help=f"Model weight file. Available: {[m.name for m in available_models]}")
    parser.add_argument("--data", type=str, default="data/roboflow_dataset/data.yaml", 
                        help="Path to data.yaml (relative to model_training/)")
    parser.add_argument("--output", type=str, default="outputs/fresh_confusion_matrix.png", 
                        help="Output image path (relative to model_training/)")
    
    args = parser.parse_args()
    
    if not args.weights:
        print("Error: No .pt model files found in model_training directory.")
        sys.exit(1)

    # Resolution
    weights_path = project_root / args.weights
    data_path = project_root / args.data
    output_path = project_root / args.output
    
    if not weights_path.exists():
        print(f"Error: Weights file not found at {weights_path}")
        sys.exit(1)
        
    if not data_path.exists():
        print(f"Error: Data config not found at {data_path}")
        sys.exit(1)

    if check_dependencies():
        generate_confusion_matrix(str(weights_path), str(data_path), str(output_path))
    else:
        print("Please manually install: pip install seaborn matplotlib pandas")

if __name__ == "__main__":
    main()
