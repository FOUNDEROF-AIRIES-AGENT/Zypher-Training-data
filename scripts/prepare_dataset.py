"""Convert Zypher knowledge-base markdown chunks into SFT training JSONL."""

from __future__ import annotations

import argparse
import json
import random
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

SYSTEM_PROMPT = (
    "You are Zypher, an enterprise AI coding assistant with deep expertise in "
    "Retrieval-Augmented Generation (RAG), GraphRAG, agentic workflows, and "
    "software architecture for code intelligence systems."
)

CHUNK_FILE_RE = re.compile(r"^CHUNK-(\d+)-(.+)\.md$", re.IGNORECASE)
ANSWER_RE = re.compile(r"\*\*Answer:\*\*\s*(.+)", re.DOTALL | re.IGNORECASE)


@dataclass
class Chunk:
    number: int
    suffix: str
    path: Path
    metadata: dict[str, Any] = field(default_factory=dict)
    body: str = ""

    @property
    def chunk_id(self) -> str:
        return f"CHUNK-{self.number:05d}"


def parse_chunk_file(path: Path) -> Chunk | None:
    match = CHUNK_FILE_RE.match(path.name)
    if not match:
        return None

    number = int(match.group(1))
    suffix = match.group(2)
    text = path.read_text(encoding="utf-8")

    metadata: dict[str, Any] = {}
    body = text

    parts = text.split("---")
    if len(parts) >= 3:
        # Files contain two YAML frontmatter blocks; use the second block.
        yaml_block = parts[1].strip()
        body = "---".join(parts[2:]).strip()
        if yaml_block:
            try:
                loaded = yaml.safe_load(yaml_block)
                metadata = loaded if isinstance(loaded, dict) else {}
            except yaml.YAMLError:
                metadata = {}

    return Chunk(number=number, suffix=suffix, path=path, metadata=metadata, body=body)


def load_chunks(kb_dir: Path) -> list[Chunk]:
    chunks = [parse_chunk_file(path) for path in sorted(kb_dir.glob("CHUNK-*.md"))]
    return [chunk for chunk in chunks if chunk is not None]


def make_example(
    messages: list[dict[str, str]],
    *,
    source: str,
    chunk_ids: list[str],
    task_type: str,
) -> dict[str, Any]:
    return {
        "messages": messages,
        "metadata": {
            "source": source,
            "chunk_ids": chunk_ids,
            "task_type": task_type,
        },
    }


def extract_title(chunk: Chunk) -> str:
    title = chunk.metadata.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()

    for line in chunk.body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
        if line.startswith("## "):
            return line[3:].strip()
    return chunk.suffix.replace("_", " ").title()


def extract_faq_answer(body: str) -> str | None:
    match = ANSWER_RE.search(body)
    if match:
        return match.group(1).strip()
    return None


def extract_question_from_body(body: str, fallback_title: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback_title


def section_content(body: str) -> str:
  """Return markdown body without the top-level heading."""
  lines = body.splitlines()
  if lines and lines[0].startswith("#"):
      lines = lines[1:]
  return "\n".join(line for line in lines).strip()


def example_from_standalone(chunk: Chunk) -> dict[str, Any] | None:
    title = extract_title(chunk)
    body = section_content(chunk.body)
    if len(body) < 80:
        return None

    answer = extract_faq_answer(chunk.body)
    if answer:
        question = extract_question_from_body(chunk.body, title)
        user_msg = question if question.endswith("?") else f"{question}?"
        return make_example(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
                {"role": "assistant", "content": answer},
            ],
            source=chunk.path.name,
            chunk_ids=[chunk.chunk_id],
            task_type="faq",
        )

    tags = chunk.metadata.get("tags") or []
    tag_hint = f" (tags: {', '.join(tags)})" if tags else ""
    user_msg = (
        f"Provide a detailed explanation about: {title}{tag_hint}. "
        "Include implementation details and best practices where relevant."
    )
    return make_example(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": body},
        ],
        source=chunk.path.name,
        chunk_ids=[chunk.chunk_id],
        task_type="documentation",
    )


def example_from_adr(parent: Chunk, parts: dict[str, Chunk]) -> dict[str, Any] | None:
    title = extract_title(parent)
    sections = []
    for key in ("context", "decision", "consequences"):
        part = parts.get(key)
        if part and section_content(part.body):
            heading = key.replace("_", " ").title()
            sections.append(f"## {heading}\n\n{section_content(part.body)}")

    if not sections:
        return None

    response = f"# Architecture Decision: {title}\n\n" + "\n\n".join(sections)
    return make_example(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Document the architecture decision record for: {title}. "
                    "Include context, the decision made, and consequences."
                ),
            },
            {"role": "assistant", "content": response},
        ],
        source=parent.path.name,
        chunk_ids=[parent.chunk_id] + [parts[k].chunk_id for k in ("context", "decision", "consequences") if k in parts],
        task_type="architecture_decision",
    )


def example_from_code_review(parent: Chunk, parts: dict[str, Chunk]) -> dict[str, Any] | None:
    title = extract_title(parent)
    before = parts.get("before")
    final = parts.get("final_code")
    if not before or not final:
        return None

    before_code = section_content(before.body)
    final_code = section_content(final.body)
    if not before_code or not final_code:
        return None

    comments = section_content(parts["reviewer_comments"].body) if "reviewer_comments" in parts else ""
    reasoning = section_content(parts["reasoning"].body) if "reasoning" in parts else ""

    review_parts = [f"## Suggested Changes\n\n{final_code}"]
    if comments:
        review_parts.append(f"## Reviewer Comments\n\n{comments}")
    if reasoning:
        review_parts.append(f"## Reasoning\n\n{reasoning}")

    return make_example(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Review the following code for: {title}\n\n"
                    f"```python\n{before_code}\n```"
                ),
            },
            {"role": "assistant", "content": "\n\n".join(review_parts)},
        ],
        source=parent.path.name,
        chunk_ids=[parent.chunk_id] + [c.chunk_id for c in parts.values()],
        task_type="code_review",
    )


def example_from_incident(parent: Chunk, parts: dict[str, Chunk]) -> dict[str, Any] | None:
    title = extract_title(parent)
    section_keys = ("timeline", "impact", "root_cause", "resolution", "lessons_learned")
    sections = []
    for key in section_keys:
        part = parts.get(key)
        if part and section_content(part.body):
            heading = key.replace("_", " ").title()
            sections.append(f"## {heading}\n\n{section_content(part.body)}")

    if not sections:
        return None

    response = f"# {title}\n\n" + "\n\n".join(sections)
    return make_example(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Write a complete incident report for: {title}",
            },
            {"role": "assistant", "content": response},
        ],
        source=parent.path.name,
        chunk_ids=[parent.chunk_id] + [parts[k].chunk_id for k in section_keys if k in parts],
        task_type="incident_report",
    )


def example_from_support_ticket(parent: Chunk, parts: dict[str, Chunk]) -> dict[str, Any] | None:
    title = extract_title(parent)
    section_keys = ("problem", "environment", "solution", "related_docs")
    sections = []
    for key in section_keys:
        part = parts.get(key)
        if part and section_content(part.body):
            heading = key.replace("_", " ").title()
            sections.append(f"## {heading}\n\n{section_content(part.body)}")

    if not sections:
        return None

    response = f"# {title}\n\n" + "\n\n".join(sections)
    return make_example(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Resolve this support ticket and document the solution: {title}",
            },
            {"role": "assistant", "content": response},
        ],
        source=parent.path.name,
        chunk_ids=[parent.chunk_id] + [parts[k].chunk_id for k in section_keys if k in parts],
        task_type="support_ticket",
    )


def example_from_operational_issue(parent: Chunk, parts: dict[str, Chunk]) -> dict[str, Any] | None:
    title = extract_title(parent)
    description = parts.get("description")
    resolution = parts.get("resolution")
    if not description or not resolution:
        return None

    desc_text = section_content(description.body)
    res_text = section_content(resolution.body)
    if not desc_text or not res_text:
        return None

    response = (
        f"# {title}\n\n"
        f"## Description\n\n{desc_text}\n\n"
        f"## Resolution\n\n{res_text}"
    )
    return make_example(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Diagnose and resolve this operational issue: {title}",
            },
            {"role": "assistant", "content": response},
        ],
        source=parent.path.name,
        chunk_ids=[parent.chunk_id, description.chunk_id, resolution.chunk_id],
        task_type="operational_issue",
    )


def example_from_graph_link(parent: Chunk, description: Chunk) -> dict[str, Any] | None:
    title = extract_title(parent)
    desc_text = section_content(description.body)
    if not desc_text:
        return None

    return make_example(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Explain this architecture graph relationship: {title}",
            },
            {"role": "assistant", "content": desc_text},
        ],
        source=parent.path.name,
        chunk_ids=[parent.chunk_id, description.chunk_id],
        task_type="graph_link",
    )


def build_examples(chunks: list[Chunk]) -> list[dict[str, Any]]:
    by_number = {chunk.number: chunk for chunk in chunks}
    consumed: set[int] = set()
    examples: list[dict[str, Any]] = []

    def take_following(parent_num: int, suffixes: list[str]) -> dict[str, Chunk]:
        found: dict[str, Chunk] = {}
        for offset, suffix in enumerate(suffixes, start=1):
            candidate = by_number.get(parent_num + offset)
            if candidate and candidate.suffix == suffix:
                found[suffix] = candidate
                consumed.add(candidate.number)
        return found

    for chunk in chunks:
        if chunk.number in consumed:
            continue

        suffix = chunk.suffix

        if suffix.startswith("code_review_"):
            parts = take_following(chunk.number, ["before", "reviewer_comments", "final_code", "reasoning"])
            example = example_from_code_review(chunk, parts)
            if example:
                examples.append(example)
                consumed.add(chunk.number)
            continue

        if suffix.startswith("incident_report_"):
            parts = take_following(
                chunk.number,
                ["timeline", "impact", "root_cause", "resolution", "lessons_learned"],
            )
            example = example_from_incident(chunk, parts)
            if example:
                examples.append(example)
                consumed.add(chunk.number)
            continue

        if suffix.startswith("support_ticket_"):
            parts = take_following(chunk.number, ["problem", "environment", "solution", "related_docs"])
            example = example_from_support_ticket(chunk, parts)
            if example:
                examples.append(example)
                consumed.add(chunk.number)
            continue

        if suffix.startswith("graph_link_"):
            next_chunk = by_number.get(chunk.number + 1)
            if next_chunk and next_chunk.suffix == "description":
                example = example_from_graph_link(chunk, next_chunk)
                if example:
                    examples.append(example)
                    consumed.update({chunk.number, next_chunk.number})
            continue

        if suffix.endswith("_unique_0") or suffix.endswith("_unique_1"):
            if "context" not in suffix and "decision" not in suffix and "consequences" not in suffix:
                parts = take_following(chunk.number, ["context", "decision", "consequences"])
                example = example_from_adr(chunk, parts)
                if example:
                    examples.append(example)
                    consumed.add(chunk.number)
                    continue

        if "_unique_" in suffix and not any(
            suffix.endswith(s) for s in ("_context", "_decision", "_consequences")
        ):
            # Operational issues: title + description + resolution
            if suffix not in ("description", "resolution", "context", "decision", "consequences"):
                parts = take_following(chunk.number, ["description", "resolution"])
                if parts:
                    example = example_from_operational_issue(chunk, parts)
                    if example:
                        examples.append(example)
                        consumed.add(chunk.number)
                        continue

        if chunk.number not in consumed:
            example = example_from_standalone(chunk)
            if example:
                examples.append(example)
                consumed.add(chunk.number)

    return examples


def split_dataset(
    examples: list[dict[str, Any]],
    *,
    val_ratio: float,
    test_ratio: float,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    rng = random.Random(seed)
    shuffled = examples.copy()
    rng.shuffle(shuffled)

    n = len(shuffled)
    n_test = int(n * test_ratio)
    n_val = int(n * val_ratio)

    test = shuffled[:n_test]
    val = shuffled[n_test : n_test + n_val]
    train = shuffled[n_test + n_val :]
    return train, val, test


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def summarize(examples: list[dict[str, Any]]) -> dict[str, Any]:
    by_type: dict[str, int] = {}
    for example in examples:
        task_type = example["metadata"]["task_type"]
        by_type[task_type] = by_type.get(task_type, 0) + 1
    return {
        "total_examples": len(examples),
        "by_task_type": by_type,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare fine-tuning dataset from knowledge base")
    parser.add_argument(
        "--kb-dir",
        type=Path,
        default=Path("knowledge-base"),
        help="Path to extracted knowledge-base directory",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data"),
        help="Directory for train/val/test JSONL files",
    )
    parser.add_argument("--val-ratio", type=float, default=0.1)
    parser.add_argument("--test-ratio", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    chunks = load_chunks(args.kb_dir)
    examples = build_examples(chunks)
    train, val, test = split_dataset(
        examples,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        seed=args.seed,
    )

    write_jsonl(args.output_dir / "train.jsonl", train)
    write_jsonl(args.output_dir / "val.jsonl", val)
    write_jsonl(args.output_dir / "test.jsonl", test)

    stats = summarize(examples)
    stats.update(
        {
            "train_examples": len(train),
            "val_examples": len(val),
            "test_examples": len(test),
            "source_chunks": len(chunks),
        }
    )
    stats_path = args.output_dir / "dataset_stats.json"
    stats_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    print(json.dumps(stats, indent=2))
    print(f"Wrote datasets to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
