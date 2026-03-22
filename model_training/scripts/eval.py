from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a YOLOv8 model.")
    parser.add_argument("--weights", required=True, help="Path to run folder or best.pt.")
    parser.add_argument("--data", default=None, help="Optional path to data.yaml.")
    return parser.parse_args()


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_weights_path(weights_arg: str) -> tuple[Path, Path]:
    p = Path(weights_arg)
    if p.is_dir():
        candidate = p / "weights" / "best.pt"
        run_dir = p
    else:
        candidate = p
        if p.parent.name == "weights":
            run_dir = p.parent.parent
        else:
            run_dir = p.parent
    return candidate, run_dir


def resolve_data_path(run_dir: Path, cli_data: Optional[str]) -> Optional[str]:
    if cli_data:
        return cli_data

    args_yaml = run_dir / "args.yaml"
    if args_yaml.exists():
        try:
            data = yaml.safe_load(args_yaml.read_text())
            if isinstance(data, dict) and "data" in data:
                return str(data["data"])
        except Exception:
            return None
    return None


def to_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except Exception:
        return None


def metrics_to_dict(metrics: Any, weights_path: Path) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "weights": str(weights_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if hasattr(metrics, "box"):
        box = metrics.box
        result["mAP50-95"] = to_float(getattr(box, "map", None))
        result["mAP50"] = to_float(getattr(box, "map50", None))
        result["mAP75"] = to_float(getattr(box, "map75", None))
        result["precision"] = to_float(getattr(box, "p", None))
        result["recall"] = to_float(getattr(box, "r", None))
        maps = getattr(box, "maps", None)
        if maps is not None:
            try:
                result["per_class_map"] = [float(v) for v in maps]
            except Exception:
                result["per_class_map"] = None
    if hasattr(metrics, "fitness"):
        result["fitness"] = to_float(metrics.fitness)
    return result


def main() -> None:
    args = parse_args()
    weights_path, run_dir = resolve_weights_path(args.weights)

    if not weights_path.exists():
        print(
            "ERROR: best.pt not found. Provide a run folder or weights file.\n"
            "Example: python scripts/eval.py --weights outputs/run1",
            file=sys.stderr,
        )
        sys.exit(1)

    data_path = resolve_data_path(run_dir, args.data)
    if not data_path:
        print(
            "ERROR: Could not determine data.yaml.\n"
            "Ensure you trained from this run folder or pass --data path/to/data.yaml.",
            file=sys.stderr,
        )
        sys.exit(1)

    model = YOLO(str(weights_path))
    metrics = model.val(data=data_path)

    metrics_dict = metrics_to_dict(metrics, weights_path)

    output_path = get_project_root() / "outputs" / "metrics.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics_dict, indent=2))
    print(f"Saved metrics to {output_path}")


if __name__ == "__main__":
    main()
