from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from roboflow import Roboflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Roboflow dataset.")
    parser.add_argument("--workspace", required=True, help="Roboflow workspace slug.")
    parser.add_argument("--project", required=True, help="Roboflow project slug.")
    parser.add_argument("--version", required=True, type=int, help="Dataset version number.")
    parser.add_argument("--format", default="yolov8", help="Export format (default: yolov8).")
    return parser.parse_args()


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def get_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        print(
            "ERROR: ROBOFLOW_API_KEY is not set.\n"
            "Create a .env file in the project root and add:\n"
            "ROBOFLOW_API_KEY=your_key_here",
            file=sys.stderr,
        )
        sys.exit(1)
    return api_key


def main() -> None:
    args = parse_args()
    api_key = get_api_key()
    project_root = get_project_root()
    data_dir = project_root / "data" / "roboflow_dataset"
    data_dir.mkdir(parents=True, exist_ok=True)

    rf = Roboflow(api_key=api_key)
    workspace = rf.workspace(args.workspace)
    project = workspace.project(args.project)

    dataset = project.version(args.version).download(args.format, location=str(data_dir))
    dataset_path = Path(dataset.location)
    data_yaml = dataset_path / "data.yaml"

    if not data_yaml.exists():
        yaml_candidates = list(dataset_path.glob("*.yaml"))
        if yaml_candidates:
            data_yaml = yaml_candidates[0]
        else:
            print(
                f"ERROR: data.yaml not found in {dataset_path}.",
                file=sys.stderr,
            )
            sys.exit(1)

    print(str(data_yaml.resolve()))


if __name__ == "__main__":
    main()
