"""Document ingestion for Coltex Platform."""

from __future__ import annotations

import re
import textwrap
import uuid
from pathlib import Path
from urllib.parse import urlparse

import yaml

from coltex_platform.store import Collection, DocumentRecord, PlatformStore


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")[:80] or "document"


class IngestionService:
    def __init__(self, store: PlatformStore, chunk_size: int = 1200, chunk_overlap: int = 150):
        self.store = store
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _collection_dir(self, collection: Collection) -> Path:
        path = Path(collection.kb_path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _write_markdown(
        self,
        collection: Collection,
        title: str,
        content: str,
        doc_type: str = "documentation",
        category: str = "",
        tags: list[str] | None = None,
        source_uri: str = "",
        source_type: str = "upload",
    ) -> tuple[Path, DocumentRecord]:
        doc_id = f"DOC-{uuid.uuid4().hex[:12]}"
        filename = f"{doc_id}-{slugify(title)}.md"
        kb_dir = self._collection_dir(collection)
        file_path = kb_dir / filename

        frontmatter = {
            "id": doc_id,
            "title": title,
            "doc_type": doc_type,
            "category": category,
            "tags": tags or [],
            "source_uri": source_uri,
            "source_type": source_type,
        }
        body = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False).strip()
        file_path.write_text(f"---\n{body}---\n\n{content.strip()}\n", encoding="utf-8")

        record = self.store.add_document(
            collection_id=collection.id,
            title=title,
            file_path=str(file_path),
            source_type=source_type,
            source_uri=source_uri,
            doc_type=doc_type,
            category=category,
        )
        return file_path, record

    def ingest_text(
        self,
        collection: Collection,
        title: str,
        content: str,
        doc_type: str = "documentation",
        category: str = "",
        tags: list[str] | None = None,
    ) -> DocumentRecord:
        chunks = self._maybe_chunk(content, title)
        if len(chunks) == 1:
            _, record = self._write_markdown(
                collection, title, content, doc_type, category, tags, source_type="text"
            )
            return record

        records: list[DocumentRecord] = []
        for i, chunk in enumerate(chunks, start=1):
            chunk_title = f"{title} (part {i}/{len(chunks)})"
            _, record = self._write_markdown(
                collection,
                chunk_title,
                chunk,
                doc_type,
                category,
                tags,
                source_type="text",
            )
            records.append(record)
        return records[0]

    def ingest_file(
        self,
        collection: Collection,
        filename: str,
        data: bytes,
        title: str | None = None,
        doc_type: str = "documentation",
        category: str = "",
    ) -> DocumentRecord:
        ext = Path(filename).suffix.lower()
        title = title or Path(filename).stem.replace("_", " ").title()

        if ext in (".md", ".txt", ".html", ".json", ".csv"):
            content = data.decode("utf-8", errors="replace")
        elif ext == ".pdf":
            content = self._extract_pdf_text(data)
        else:
            content = data.decode("utf-8", errors="replace")

        _, record = self._write_markdown(
            collection,
            title,
            content,
            doc_type,
            category,
            source_uri=filename,
            source_type="upload",
        )
        return record

    def ingest_url(
        self,
        collection: Collection,
        url: str,
        title: str | None = None,
        doc_type: str = "documentation",
        category: str = "",
    ) -> DocumentRecord:
        content, fetched_title = self._fetch_url(url)
        title = title or fetched_title or urlparse(url).netloc
        _, record = self._write_markdown(
            collection,
            title,
            content,
            doc_type,
            category,
            source_uri=url,
            source_type="url",
        )
        return record

    def _maybe_chunk(self, content: str, title: str) -> list[str]:
        if len(content) <= self.chunk_size * 2:
            return [content]
        paragraphs = content.split("\n\n")
        chunks: list[str] = []
        current: list[str] = []
        current_len = 0
        for para in paragraphs:
            if current_len + len(para) > self.chunk_size and current:
                chunks.append("\n\n".join(current))
                overlap = "\n\n".join(current[-2:]) if len(current) >= 2 else current[-1]
                current = [overlap] if overlap else []
                current_len = len(overlap)
            current.append(para)
            current_len += len(para)
        if current:
            chunks.append("\n\n".join(current))
        return chunks or [content]

    @staticmethod
    def _fetch_url(url: str) -> tuple[str, str]:
        try:
            import httpx
        except ImportError as exc:
            raise RuntimeError("httpx required for URL ingestion. pip install httpx") from exc

        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            resp = client.get(url)
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "")
            text = resp.text
            title = url
            if "html" in content_type:
                title_match = re.search(r"<title[^>]*>([^<]+)</title>", text, re.I)
                if title_match:
                    title = title_match.group(1).strip()
                text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.I | re.S)
                text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.I | re.S)
                text = re.sub(r"<[^>]+>", " ", text)
                text = re.sub(r"\s+", " ", text).strip()
            return textwrap.dedent(text), title

    @staticmethod
    def _extract_pdf_text(data: bytes) -> str:
        try:
            from pypdf import PdfReader
            from io import BytesIO

            reader = PdfReader(BytesIO(data))
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n\n".join(pages).strip() or "[PDF content could not be extracted]"
        except ImportError:
            return "[PDF upload received — install pypdf for text extraction]"
