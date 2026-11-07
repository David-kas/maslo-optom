# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    issues = []
    titles = {}
    h1s = {}
    html_files = list(ROOT.glob("**/*.html"))
    html_files = [f for f in html_files if "legacy" not in f.parts and "vendor" not in f.parts]

    for f in html_files:
        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(ROOT).as_posix()
        t = re.search(r"<title>([^<]+)</title>", text)
        h = re.search(r"<h1[^>]*>([^<]+)</h1>", text)
        if t:
            title = t.group(1)
            if title in titles:
                issues.append(f"Duplicate title: {title} ({titles[title]}, {rel})")
            titles[title] = rel
        else:
            issues.append(f"No title: {rel}")
        if h:
            hv = h.group(1).strip()
            if hv in h1s:
                issues.append(f"Duplicate H1: {hv}")
            h1s[hv] = rel
        if 'meta name="description"' not in text:
            issues.append(f"No meta description: {rel}")
        if 'rel="canonical"' not in text:
            issues.append(f"No canonical: {rel}")

        for href in re.findall(r'href="([^"#?]+)"', text):
            if href.startswith("http") or href.startswith("mailto:") or href.startswith("tel:"):
                continue
            if href.startswith("./"):
                href = href[2:]
            target = (f.parent / href).resolve() if not href.startswith("/") else None
            if target and not target.exists() and not href.endswith("/"):
                issues.append(f"Broken link in {rel}: {href}")
            if href.endswith("/"):
                idx = (f.parent / href / "index.html").resolve()
                if not idx.exists():
                    issues.append(f"Broken dir link in {rel}: {href}")

        for src in re.findall(r'src="(\./assets/[^"]+)"', text):
            p = (f.parent / src[2:]).resolve()
            if not p.exists():
                issues.append(f"Missing image in {rel}: {src}")

    print(f"Scanned {len(html_files)} HTML files. Issues: {len(issues)}")
    for i in issues[:40]:
        print("-", i)
    if len(issues) > 40:
        print(f"... and {len(issues)-40} more")


if __name__ == "__main__":
    main()
