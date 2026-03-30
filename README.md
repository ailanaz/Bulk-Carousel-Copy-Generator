# Bulk Carousel Copy Generator

Bulk Carousel Copy Generator is an MCP server and standalone Python script for generating TikTok photo carousel copy in bulk.

The five Income Spectrum categories in this repo are starter examples. They show how the generator can be structured, but they are not required topics.

It ships with these five example category labels:

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

The standalone script ships with these starter topics from the Income Spectrum example set:

- Business Ideas: Biohazard cleanup service
- Self Directed Income: Medical billing and coding
- Knowledge Resources: QuickBooks certification
- Supportive Services: LLC formation services
- Official Links: Cottage food laws by state

## Custom topics and subtopics

Other people can use their own topics and subtopics without editing the code. The Income Spectrum topics are examples only.

The easiest way is to make a JSON file like this:

```json
{
  "topics": {
    "Business Ideas": {
      "topic": "Mobile notary business",
      "subtopics": ["startup costs", "local demand", "buyer type", "first services to offer"]
    },
    "Self Directed Income": {
      "topic": "Bookkeeping services",
      "subtopics": ["who pays for it", "monthly offers", "trust building", "first client steps"]
    },
    "Knowledge Resources": {
      "topic": "Google Ads certification",
      "subtopics": ["what you learn", "real work use", "client trust", "skill overlap"]
    },
    "Supportive Services": {
      "topic": "Registered agent services",
      "subtopics": ["what it handles", "time saved", "state compliance", "cost tradeoffs"]
    },
    "Official Links": {
      "topic": "Seller permit rules by state",
      "subtopics": ["which agency to check", "when registration is required", "state differences", "official forms"]
    }
  }
}
```

You can also keep the old simple format if you only want one topic per category:

```json
{
  "topics": {
    "Business Ideas": "Mobile notary business",
    "Self Directed Income": "Bookkeeping services",
    "Knowledge Resources": "Google Ads certification",
    "Supportive Services": "Registered agent services",
    "Official Links": "Seller permit rules by state"
  }
}
```

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
    "Business Ideas": {
      "topic": "Biohazard cleanup service",
      "subtopics": ["startup costs", "buyer demand", "repeat business", "risk review"]
    },
    "Self Directed Income": "Medical billing and coding",
    "Knowledge Resources": "QuickBooks certification",
    "Supportive Services": "LLC formation services",
    "Official Links": "Cottage food laws by state"
  },
  "videos_per_topic": 20,
  "output_path": "tiktok-carousels-output.json",
  "csv_output_path": "tiktok-carousels-output.csv"
}
```

The sample topics in that example are only there to show the format. Users can replace every topic and subtopic with their own.

The tool writes:

- `tiktok-carousels-output.json`
- `tiktok-carousels-output.csv`

The CSV file is flat and Canva-friendly. Each row is one carousel with these columns:

- `title`
- `hook`
- `body_1`
- `body_2`
- `body_3`
- `body_4`
- `body_5`
- `cta`

## Standalone use

Run this anytime:

```bash
python3 tiktok-carousel-gen.py
```

That writes:

```text
tiktok-carousels-output.json
tiktok-carousels-output.csv
```

The CSV file is the one to use for Canva Bulk Create. It only includes the text fields most people will map in Canva.

## Standalone use with your own topics

1. Create a JSON file with your topics.
2. Run:

```bash
python3 tiktok-carousel-gen.py --input my-topics.json
```

That will use your topics and still create both output files.

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
- output includes both JSON and CSV so it is easy to route into sheets, design tools, Canva Bulk Create, or later post-processing
