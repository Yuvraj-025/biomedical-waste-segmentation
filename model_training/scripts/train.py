from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a YOLOv8 model.")
    parser.add_argument("--data", required=True, help="Path to data.yaml.")
    parser.add_argument("--model", default="yolov8n.pt", help="Model checkpoint (default: yolov8n.pt).")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size (default: 640).")
    parser.add_argument("--epochs", type=int, default=50, help="Epochs (default: 50).")
    parser.add_argument("--batch", type=int, default=16, help="Batch size (default: 16).")
    parser.add_argument("--device", default="auto", help="Device: auto, cpu, 0, 0,1,2,3 (default: auto).")
    parser.add_argument("--project", default="outputs", help="Project directory (default: outputs).")
    parser.add_argument("--name", default="run1", help="Run name (default: run1).")
    parser.add_argument("--close-mosaic", type=int, default=None, help="Disable mosaic augmentation this many epochs before end.")
    parser.add_argument("--mixup", type=float, default=None, help="MixUp augmentation probability (0.0-1.0).")
    parser.add_argument("--copy-paste", type=float, default=None, help="Copy-paste augmentation probability (0.0-1.0).")
    return parser.parse_args()


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_device(device_arg: str) -> str:
    if device_arg == "auto":
        return "0" if torch.cuda.is_available() else "cpu"
    return device_arg


def main() -> None:
    args = parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(
            "ERROR: data.yaml not found.\n"
            "Run: python scripts/download_dataset.py ...",
            file=sys.stderr,
        )
        sys.exit(1)

    device = resolve_device(args.device)
    batch = args.batch
    if device.lower() == "cpu":
        if batch > 4:
            print("Warning: CPU detected. Reducing batch size to 4 for safety.")
            batch = 4

    project_root = get_project_root()
    project_dir = project_root / args.project
    project_dir.mkdir(parents=True, exist_ok=True)

    model = YOLO(args.model)
    train_kwargs = {
        "data": str(data_path),
        "imgsz": args.imgsz,
        "epochs": args.epochs,
        "batch": batch,
        "device": device,
        "project": str(project_dir),
        "name": args.name,
        "pretrained": True,
        "patience": 20,
    }
    if args.close_mosaic is not None:
        train_kwargs["close_mosaic"] = args.close_mosaic
    if args.mixup is not None:
        train_kwargs["mixup"] = args.mixup
    if args.copy_paste is not None:
        train_kwargs["copy_paste"] = args.copy_paste

    model.train(
        **train_kwargs
    )


if __name__ == "__main__":
    main()
