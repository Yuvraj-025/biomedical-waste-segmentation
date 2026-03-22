from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export YOLOv8 weights.")
    parser.add_argument("--weights", required=True, help="Path to weights file (best.pt).")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size (default: 640).")
    parser.add_argument("--device", default="auto", help="Device: auto, cpu, 0 (default: auto).")
    parser.add_argument("--no-onnx", action="store_true", help="Disable ONNX export.")
    parser.add_argument("--torchscript", action="store_true", help="Also export to TorchScript.")
    return parser.parse_args()


def resolve_device(device_arg: str) -> str:
    if device_arg == "auto":
        return "0" if torch.cuda.is_available() else "cpu"
    return device_arg


def main() -> None:
    args = parse_args()
    weights_path = Path(args.weights)

    if not weights_path.exists():
        print(
            "ERROR: weights file not found.\n"
            "Example: python scripts/export.py --weights outputs/run1/weights/best.pt",
            file=sys.stderr,
        )
        sys.exit(1)

    device = resolve_device(args.device)
    model = YOLO(str(weights_path))

    if not args.no_onnx:
        model.export(format="onnx", imgsz=args.imgsz, device=device)

    if args.torchscript:
        model.export(format="torchscript", imgsz=args.imgsz, device=device)


if __name__ == "__main__":
    main()
