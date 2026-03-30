#!/usr/bin/env python3
"""Standalone runner for Bulk Carousel Copy Generator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from server import DEFAULT_TOPICS, generate_payload


def load_topics(input_path: str | None) -> Dict[str, Any]:
    if not input_path:
        return DEFAULT_TOPICS

    file_path = Path(input_path).expanduser().resolve()
    data = json.loads(file_path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "topics" in data:
        return data["topics"]
    if isinstance(data, dict):
        return data
    raise ValueError("Input JSON must be an object with category keys or a top-level \"topics\" object.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate bulk TikTok carousel copy.")
    parser.add_argument("--input", help="Path to a JSON file with your own topics and optional subtopics.")
    parser.add_argument("--output-json", default="tiktok-carousels-output.json", help="Path for the JSON output file.")
    parser.add_argument("--output-csv", default="tiktok-carousels-output.csv", help="Path for the CSV output file.")
    args = parser.parse_args()

    topics = load_topics(args.input)
    payload = generate_payload(
        topics=topics,
        output_path=args.output_json,
        csv_output_path=args.output_csv,
    )
    print(
        json.dumps(
            {
                "output_file": payload["output_file"],
                "csv_output_file": payload["csv_output_file"],
                "total_carousels": payload["total_carousels"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
