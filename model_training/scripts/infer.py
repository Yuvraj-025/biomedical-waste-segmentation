from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Union

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run inference with a YOLOv8 model.")
    parser.add_argument("--weights", required=True, help="Path to weights file (best.pt).")
    parser.add_argument("--source", required=True, help="Image/video path, URL, or webcam index (e.g., 0).")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold (default: 0.25).")
    parser.add_argument("--save", action="store_true", help="Save predictions to disk.")
    return parser.parse_args()


def parse_source(source: str) -> Union[str, int]:
    if source.isdigit() and not Path(source).exists():
        return int(source)
    return source


def main() -> None:
    args = parse_args()
    weights_path = Path(args.weights)

    if not weights_path.exists():
        print(
            "ERROR: weights file not found.\n"
            "Example: python scripts/infer.py --weights outputs/run1/weights/best.pt --source 0",
            file=sys.stderr,
        )
        sys.exit(1)

    source = parse_source(args.source)
    model = YOLO(str(weights_path))
    model.predict(source=source, conf=args.conf, save=args.save)


if __name__ == "__main__":
    main()
