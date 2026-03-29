# Bulk Carousel Copy Generator

Bulk Carousel Copy Generator is an MCP server and standalone Python script for generating TikTok photo carousel copy in bulk.

It is built for five Income Spectrum categories:

- Business Ideas
- Self Directed Income
- Knowledge Resources
- Supportive Services
- Official Links

For each topic, it generates 20 carousels. That gives you 100 total carousels from one run.

Each carousel includes:

- hook
- 3 to 5 body slides
- caption
- hashtags

The built-in voice rules are strict:

- no em dashes
- no AI fluff
- no "hustle", "gig", "freelance", or "passive income"
- plain human tone

## Default topics

The standalone script ships with these starter topics:

- Business Ideas: Biohazard cleanup service
- Self Directed Income: Medical billing and coding
- Knowledge Resources: QuickBooks certification
- Supportive Services: LLC formation services
- Official Links: Cottage food laws by state

## Files

- `requirements.txt`
- `server.py`
- `pyproject.toml`
- `tiktok-carousel-gen.py`
- `README.md`

## Install

```bash
pip install git+https://github.com/ailanaz/Bulk-Carousel-Copy-Generator.git
```

## MCP config

Add it to your MCP config as a stdio server:

```json
{
  "mcpServers": {
    "bulk-carousel-copy-generator": {
      "command": "python",
      "args": ["-m", "server"],
      "cwd": "/path/to/Bulk-Carousel-Copy-Generator"
    }
  }
}
```

If you prefer running the installed console script instead of the module:

```json
{
  "mcpServers": {
    "bulk-carousel-copy-generator": {
      "command": "bulk-carousel-copy-generator"
    }
  }
}
```

## MCP tool

Tool name:

- `generate_carousels`

Input shape:

```json
{
  "topics": {
    "Business Ideas": "Biohazard cleanup service",
    "Self Directed Income": "Medical billing and coding",
    "Knowledge Resources": "QuickBooks certification",
    "Supportive Services": "LLC formation services",
    "Official Links": "Cottage food laws by state"
  },
  "videos_per_topic": 20
}
```

The tool writes `tiktok-carousels-output.json` and returns the full payload plus the output file path.

## Standalone use

Run this anytime:

```bash
python3 tiktok-carousel-gen.py
```

That writes:

```text
tiktok-carousels-output.json
```

## Output format

The JSON output looks like this:

```json
{
  "generator": "Bulk Carousel Copy Generator",
  "total_carousels": 100,
  "videos_per_topic": 20,
  "topics": {
    "Business Ideas": "Biohazard cleanup service"
  },
  "carousels": [
    {
      "id": "business-ideas-01",
      "category": "Business Ideas",
      "topic": "Biohazard cleanup service",
      "hook": "Biohazard cleanup service gets judged too fast.",
      "body_slides": [
        "Start with who already pays for this problem.",
        "Then check what the average job is worth.",
        "Then check how repeat demand shows up."
      ],
      "caption": "Biohazard cleanup service gets easier to judge when you stop reacting to the label and start checking what actually matters.",
      "hashtags": [
        "#businessideas",
        "#smallbusiness",
        "#businessowner",
        "#BiohazardCleanupService",
        "#tiktokcarousel",
        "#carousel1"
      ]
    }
  ]
}
```

## Notes

- `videos_per_topic` is fixed at `20` for this build
- all five categories are required
- output stays JSON so it is easy to route into sheets, design tools, or later post-processing
