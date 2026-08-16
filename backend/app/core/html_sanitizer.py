from html import escape
from html.parser import HTMLParser
from urllib.parse import urlparse


ALLOWED_TAGS = {
    "a",
    "blockquote",
    "br",
    "code",
    "em",
    "h1",
    "h2",
    "h3",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "strong",
    "u",
    "ul",
}
VOID_TAGS = {"br", "hr"}
DISCARDED_WITH_CONTENT = {"script", "style"}


def _safe_href(value: str) -> str | None:
    parsed = urlparse(value.strip())
    if parsed.scheme.lower() not in {"", "http", "https", "mailto"}:
        return None
    return value.strip()


class _RichTextSanitizer(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.output: list[str] = []
        self.discard_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in DISCARDED_WITH_CONTENT:
            self.discard_depth += 1
            return
        if self.discard_depth or tag not in ALLOWED_TAGS:
            return
        rendered_attrs = ""
        if tag == "a":
            attributes = dict(attrs)
            href = _safe_href(attributes.get("href") or "")
            if href:
                title = attributes.get("title")
                rendered_attrs = f' href="{escape(href, quote=True)}"'
                if title:
                    rendered_attrs += f' title="{escape(title, quote=True)}"'
                rendered_attrs += ' rel="noopener noreferrer"'
        self.output.append(f"<{tag}{rendered_attrs}>")

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in DISCARDED_WITH_CONTENT:
            self.discard_depth = max(0, self.discard_depth - 1)
            return
        if not self.discard_depth and tag in ALLOWED_TAGS and tag not in VOID_TAGS:
            self.output.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if not self.discard_depth:
            self.output.append(escape(data))


def sanitize_rich_text(value: str) -> str:
    parser = _RichTextSanitizer()
    parser.feed(value)
    parser.close()
    return "".join(parser.output).strip()
