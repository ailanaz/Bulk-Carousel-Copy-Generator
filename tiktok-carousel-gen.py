#!/usr/bin/env python3
"""Standalone runner for Bulk Carousel Copy Generator."""

from __future__ import annotations

import json

from server import DEFAULT_TOPICS, generate_payload


def main() -> None:
    payload = generate_payload(
        topics=DEFAULT_TOPICS,
        videos_per_topic=20,
        output_path="tiktok-carousels-output.json",
        csv_output_path="tiktok-carousels-output.csv",
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
