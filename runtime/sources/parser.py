"""Parse uploaded knowledge source files into plain text."""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text:
            self.parts.append(text)

    def text(self) -> str:
        return "\n".join(self.parts)


def parse_file(path: Path) -> dict:
    suffix = path.suffix.lower().lstrip(".")
    raw = path.read_bytes()

    if suffix in ("md", "markdown", "txt"):
        text = raw.decode("utf-8", errors="replace")
    elif suffix == "json":
        data = json.loads(raw.decode("utf-8", errors="replace"))
        text = json.dumps(data, indent=2) if isinstance(data, (dict, list)) else str(data)
    elif suffix in ("html", "htm"):
        parser = _TextExtractor()
        parser.feed(raw.decode("utf-8", errors="replace"))
        text = parser.text()
    elif suffix == "pdf":
        text = _parse_pdf(path)
    elif suffix == "docx":
        text = _parse_docx(path)
    else:
        text = raw.decode("utf-8", errors="replace")

    return {"format": suffix, "text": text, "char_count": len(text)}


def _parse_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(str(path))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    except ImportError:
        return f"[PDF uploaded: {path.name}. Install pypdf for text extraction: pip install pypdf]"
    except Exception as exc:
        return f"[PDF parse error: {exc}]"


def _parse_docx(path: Path) -> str:
    try:
        import docx  # type: ignore
        doc = docx.Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        return f"[DOCX uploaded: {path.name}. Install python-docx: pip install python-docx]"
    except Exception as exc:
        return f"[DOCX parse error: {exc}]"


def clean_text(text: str) -> str:
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
