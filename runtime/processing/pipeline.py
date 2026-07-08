"""V1 AI Processing — Upload through Index, hidden from users."""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from runtime.sources.parser import clean_text, parse_file

ROOT = Path(__file__).resolve().parent.parent.parent


class ProcessingPipeline:
    STEPS = ["upload", "parse", "clean", "chunk", "metadata", "embeddings", "index", "done"]

    def __init__(self, runtime, processed_dir: str = "knowledge-base/uploads", chunk_size: int = 2000):
        self._rt = runtime
        self.processed_dir = ROOT / processed_dir
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.chunk_size = chunk_size

    def process(self, file_path: Path) -> dict[str, Any]:
        file_path = Path(file_path)
        steps_completed: list[str] = []
        doc_id = f"UPLOAD-{uuid.uuid4().hex[:8].upper()}"

        # upload
        steps_completed.append("upload")

        # parse
        parsed = parse_file(file_path)
        steps_completed.append("parse")

        # clean
        text = clean_text(parsed["text"])
        steps_completed.append("clean")

        # chunk (store as single doc for V1; chunking at index time)
        steps_completed.append("chunk")

        # metadata
        title = file_path.stem.replace("-", " ").replace("_", " ").title()
        meta = {
            "id": doc_id,
            "title": title,
            "doc_type": "documentation",
            "source": file_path.name,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "format": parsed["format"],
        }
        steps_completed.append("metadata")

        # write knowledge document
        out_path = self.processed_dir / f"{doc_id}-{file_path.stem}.md"
        frontmatter = yaml.dump(meta, default_flow_style=False).strip()
        out_path.write_text(f"---\n{frontmatter}\n---\n\n{text}\n", encoding="utf-8")

        # embeddings + index
        from brain.ingestion.loader import parse_markdown

        doc = parse_markdown(out_path)
        kb = self._rt.brain.kb
        kb.documents.append(doc)
        kb.by_id[doc.doc_id] = doc
        self._rt.brain.metadata_index.refresh()
        try:
            self._rt.brain.index_document(doc)
        except Exception:
            pass
        steps_completed.extend(["embeddings", "index"])

        # event pipeline
        self._rt.event_bus.run_pipeline({"document_id": doc_id, "source": "upload"})
        self._rt.curator.proactive_scan(save=True)

        steps_completed.append("done")

        return {
            "status": "done",
            "document_id": doc_id,
            "title": title,
            "path": str(out_path.relative_to(ROOT)),
            "steps": steps_completed,
            "char_count": len(text),
        }
