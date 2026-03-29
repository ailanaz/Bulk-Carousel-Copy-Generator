#!/usr/bin/env python3
"""MCP server for bulk TikTok carousel copy generation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover
    FastMCP = None  # type: ignore[assignment]


DEFAULT_TOPICS: Dict[str, str] = {
    "Business Ideas": "Biohazard cleanup service",
    "Self Directed Income": "Medical billing and coding",
    "Knowledge Resources": "QuickBooks certification",
    "Supportive Services": "LLC formation services",
    "Official Links": "Cottage food laws by state",
}

REQUIRED_CATEGORIES = tuple(DEFAULT_TOPICS.keys())

FORBIDDEN_TERMS = (
    "hustle",
    "gig",
    "freelance",
    "passive income",
    "unlock",
    "game changer",
    "revolutionary",
    "synergy",
    "leverage",
    "seamless",
    "transformative",
)


@dataclass(frozen=True)
class CategoryProfile:
    descriptor: str
    audience: str
    category_tags: List[str]
    emphasis: str
    first_filter: str
    second_filter: str
    third_filter: str
    warning: str
    goal: str
    cta: str


CATEGORY_PROFILES: Dict[str, CategoryProfile] = {
    "Business Ideas": CategoryProfile(
        descriptor="business idea",
        audience="people comparing business ideas",
        category_tags=["#businessideas", "#smallbusiness", "#businessowner"],
        emphasis="real demand and clean positioning",
        first_filter="who already pays for this problem",
        second_filter="what the average job is worth",
        third_filter="how repeat demand shows up",
        warning="judging the idea by image instead of demand",
        goal="choose a business idea that solves a real problem",
        cta="Save this if you are comparing business ideas.",
    ),
    "Self Directed Income": CategoryProfile(
        descriptor="self directed income path",
        audience="people building income on their own terms",
        category_tags=["#selfdirectedincome", "#independentincome", "#skillbasedbusiness"],
        emphasis="clear deliverables and buyer trust",
        first_filter="what someone will actually pay to get done",
        second_filter="how easy the result is to explain",
        third_filter="how fast trust can be built",
        warning="treating it like a job title instead of a paid service",
        goal="turn a skill into a clear paid offer",
        cta="Save this if you want more self directed income ideas.",
    ),
    "Knowledge Resources": CategoryProfile(
        descriptor="knowledge resource",
        audience="people building useful skills",
        category_tags=["#skillbuilding", "#certification", "#practicallearning"],
        emphasis="usable skill and practical payoff",
        first_filter="what this helps you do in real work",
        second_filter="how quickly it shortens the learning curve",
        third_filter="whether it builds trust or confidence",
        warning="collecting information without a clear use case",
        goal="choose learning resources that lead to practical use",
        cta="Save this if you are sorting through training options.",
    ),
    "Supportive Services": CategoryProfile(
        descriptor="supportive service",
        audience="people setting up or cleaning up operations",
        category_tags=["#businesssupport", "#operations", "#smallbusinesstools"],
        emphasis="time saved and mistakes prevented",
        first_filter="what delay or confusion this removes",
        second_filter="what setup work it saves",
        third_filter="what risk it helps reduce",
        warning="buying support before the need is clear",
        goal="pick support that makes the operation cleaner",
        cta="Save this if you are comparing support services.",
    ),
    "Official Links": CategoryProfile(
        descriptor="official information topic",
        audience="people checking rules before they move",
        category_tags=["#officiallinks", "#businessrules", "#statebystate"],
        emphasis="official guidance and rule clarity",
        first_filter="what changes by state or agency",
        second_filter="what action requires an official source",
        third_filter="what can go wrong if you guess",
        warning="relying on summaries instead of the source",
        goal="check official information before you act",
        cta="Save this if you need official links in one place.",
    ),
}


def clean_text(value: str) -> str:
    value = " ".join(value.split()).strip()
    return value.replace("—", "-")


def sentence(text: str) -> str:
    text = clean_text(text).rstrip()
    if text.endswith(("?", "!", ".")):
        return text
    return f"{text}."


def ensure_voice_rules(text: str) -> str:
    text = clean_text(text)
    lowered = text.lower()
    for term in FORBIDDEN_TERMS:
        if term in lowered:
            raise ValueError(f'Generated text used forbidden term "{term}".')
    return text


def build_hashtags(category: str, topic: str, index: int) -> List[str]:
    profile = CATEGORY_PROFILES[category]
    topic_slug = "".join(ch for ch in topic.title() if ch.isalnum())
    angle_tag = f"#carousel{index + 1}"
    return profile.category_tags + [f"#{topic_slug}", "#tiktokcarousel", angle_tag]


def make_hook(topic: str, category: str, index: int) -> str:
    hooks = [
        f"{topic}: what to check first.",
        f"How to check {topic} before you commit.",
        f"{topic} looks different once you check these three things.",
        f"Before you choose {topic}, read this.",
        f"{topic} is simpler to check than it seems.",
        f"{topic}: start with the main filter.",
        f"The plain way to look at {topic}.",
        f"{topic}: the key details to review.",
        f"What matters most in {topic}.",
        f"{topic}: the first filter that matters.",
        f"A plain way to review {topic}.",
        f"{topic}: where people usually start too late.",
        f"How to compare {topic} without wasting time.",
        f"{topic}: the details worth checking.",
        f"The simplest way to judge {topic}.",
        f"{topic}: what actually changes the choice.",
        f"What to review before you move on {topic}.",
        f"{topic}: a simpler way to compare it.",
        f"The plain read on {topic}.",
        f"{topic}: use this before making a decision.",
    ]
    return ensure_voice_rules(hooks[index])


def make_body_slides(topic: str, category: str, index: int) -> List[str]:
    profile = CATEGORY_PROFILES[category]
    body_sets = [
        [
            f"Start with {profile.first_filter}.",
            f"Then check {profile.second_filter}.",
            f"Then check {profile.third_filter}.",
        ],
        [
            f"A common mistake is {profile.warning}.",
            f"The better check is {profile.emphasis}.",
            f"That usually tells you more about {topic}.",
        ],
        [
            f"{topic} matters more when it helps you {profile.goal}.",
            f"That means looking at {profile.first_filter}.",
            "Not just the label or the pitch.",
        ],
        [
            "Most people start with surface details.",
            f"A better sequence starts with {profile.first_filter}.",
            f"Then {profile.second_filter}.",
            "Then compare what still makes sense after the first month.",
            "Then decide whether the fit is real.",
        ],
        [
            "If you skip the source, the decision gets weaker.",
            f"Check {profile.first_filter}.",
            f"Check {profile.third_filter}.",
            f"Then decide whether {topic} actually fits.",
        ],
        [
            "The quick read is usually incomplete.",
            f"The useful read is about {profile.emphasis}.",
            f"That is what tells you whether {topic} is worth more review.",
        ],
        [
            "Do not start with tools or opinions.",
            f"Start with {profile.first_filter}.",
            f"Then look at {profile.second_filter}.",
            "That usually saves time later.",
        ],
        [
            f"The point of {topic} is not the title.",
            f"The point is what it helps you do.",
            f"That is why {profile.emphasis} matters more.",
        ],
        [
            "A cleaner decision starts with one clear sequence.",
            f"Check {profile.first_filter}.",
            f"Then look at {profile.second_filter}.",
            f"Then look at {profile.third_filter}.",
            "Then look at the real cost of delay.",
        ],
        [
            f"The wrong filter makes {topic} look weaker than it is.",
            f"The right filter is {profile.first_filter}.",
            f"That is where the useful signal is.",
        ],
        [
            "Stop chasing more information too early.",
            f"Look for {profile.first_filter}.",
            f"Look for {profile.third_filter}.",
            "That is usually enough for a first pass.",
        ],
        [
            "People often check this too late.",
            "That is when avoidable mistakes show up.",
            f"{topic} gets easier when you start with the source.",
        ],
        [
            "The first step is usually smaller than people think.",
            f"Check {profile.first_filter}.",
            f"Write down what you find.",
            f"Then compare options from there.",
        ],
        [
            f"You do not need more noise around {topic}.",
            "You need a better filter.",
            f"Use {profile.first_filter}.",
            f"Then test the fit.",
        ],
        [
            "The useful question is simple.",
            f"Does this make the next move clearer?",
            f"If yes, keep going.",
            f"If not, reset the filter.",
        ],
        [
            "Most people focus on the front end.",
            "A better read is the downstream effect.",
            f"What does this save or change later?",
        ],
        [
            "A lot of confusion comes from skipping the less visible part.",
            "That part usually controls the result.",
            f"That is why {profile.first_filter} matters.",
        ],
        [
            "The goal is not to collect more talking points.",
            "The goal is to make a better call.",
            "That happens when you check the right things first.",
        ],
        [
            f"Do not decide on {topic} from one article or one opinion.",
            f"Check the source.",
            f"Check the fit.",
            f"Then move.",
        ],
        [
            "The easiest way to reduce risk is simple.",
            f"Check {profile.first_filter}.",
            f"Check {profile.second_filter}.",
            f"Check {profile.third_filter}.",
            "Then check what changes if you ignore it.",
        ],
    ]
    slides = [ensure_voice_rules(sentence(slide)) for slide in body_sets[index]]
    return slides


def make_caption(topic: str, category: str, index: int) -> str:
    profile = CATEGORY_PROFILES[category]
    captions = [
        f"{topic} is easier to check when you start with {profile.first_filter} and then move through the details that matter next.",
        f"{topic} usually gets clearer when you begin with {profile.first_filter}.",
        f"A good review of {topic} starts with the basics, then moves into fit, demand, and real-world use.",
        f"{topic} is easier to compare when you check the source, the fit, and the details that affect the choice.",
        f"{topic} is usually judged too quickly. A better review stays close to the real problem and the actual use case.",
        f"A better read on {topic} starts with better questions and fewer assumptions.",
        f"{topic} gets easier to judge when you check the part that actually controls the outcome.",
        f"{topic} is easier to review when you stop guessing and check the right details first.",
        f"The real value in {topic} usually shows up after you check fit, timing, and what changes next.",
        f"{topic} makes more sense when you focus on the actual use case instead of surface-level advice.",
        f"If {topic} still feels unclear, start with the practical details first.",
        f"One pass through the right details will usually tell you more about {topic} than broad general advice.",
        f"The goal with {topic} is not more noise. The goal is a better decision.",
        f"{topic} usually gets easier to understand when the question gets narrower and more specific.",
        f"If you are still unsure about {topic}, the next step is usually to check the real constraint rather than collect more opinions.",
        f"The less visible checks around {topic} are often the ones that save the most time later.",
        f"{topic} works better as a decision test than a vague research topic.",
        f"The simpler read on {topic} is often the more useful one.",
        f"A better review of {topic} stays close to the source and the real use case.",
        f"{topic} usually gets clearer when you check what actually changes after the decision is made.",
    ]
    return ensure_voice_rules(captions[index])


def normalize_topics(topics: Dict[str, str] | None) -> Dict[str, str]:
    source = topics or DEFAULT_TOPICS
    normalized: Dict[str, str] = {}

    for category in REQUIRED_CATEGORIES:
        value = clean_text(source.get(category, ""))
        if not value:
            raise ValueError(f'Missing topic for "{category}".')
        normalized[category] = value

    return normalized


def build_carousels(topics: Dict[str, str], videos_per_topic: int = 20) -> List[Dict[str, Any]]:
    if videos_per_topic != 20:
        raise ValueError("videos_per_topic must be 20 for this build.")

    topics = normalize_topics(topics)
    carousels: List[Dict[str, Any]] = []

    for category_index, category in enumerate(REQUIRED_CATEGORIES):
        topic = topics[category]
        for index in range(videos_per_topic):
            hook = make_hook(topic, category, index)
            body_slides = make_body_slides(topic, category, index)
            caption = make_caption(topic, category, index)
            hashtags = build_hashtags(category, topic, index)

            carousels.append(
                {
                    "id": f"{category.lower().replace(' ', '-')}-{index + 1:02d}",
                    "category": category,
                    "topic": topic,
                    "hook": hook,
                    "body_slides": body_slides,
                    "caption": caption,
                    "hashtags": hashtags,
                }
            )

    return carousels


def generate_payload(
    topics: Dict[str, str] | None = None,
    videos_per_topic: int = 20,
    output_path: str = "tiktok-carousels-output.json",
) -> Dict[str, Any]:
    topics = normalize_topics(topics)
    carousels = build_carousels(topics, videos_per_topic)

    payload: Dict[str, Any] = {
        "generator": "Bulk Carousel Copy Generator",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_carousels": len(carousels),
        "videos_per_topic": videos_per_topic,
        "voice_rules": {
            "no_em_dash": True,
            "forbidden_terms": list(FORBIDDEN_TERMS[:4]),
            "tone": "neutral human tone",
            "no_ai_fluff": True,
            "search_friendly": True,
        },
        "topics": topics,
        "carousels": carousels,
    }

    output_file = Path(output_path).resolve()
    output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    payload["output_file"] = str(output_file)
    return payload


if FastMCP is not None:
    mcp = FastMCP("Bulk Carousel Copy Generator", json_response=True)

    @mcp.tool()
    def generate_carousels(
        topics: Dict[str, str] | None = None,
        videos_per_topic: int = 20,
        output_path: str = "tiktok-carousels-output.json",
    ) -> Dict[str, Any]:
        """Generate bulk TikTok photo carousel copy and write it to a JSON file."""
        return generate_payload(topics=topics, videos_per_topic=videos_per_topic, output_path=output_path)
else:  # pragma: no cover
    mcp = None


def main() -> None:
    if mcp is None:
        raise SystemExit("Install the mcp package before running the MCP server.")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
