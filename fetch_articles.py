#!/usr/bin/env python3
"""
正确抓取博客文章：保留完整HTML结构 -> Markdown
支持: Anthropic Engineering, OpenAI Developers, Claude AI Dev

每篇文章一个文件夹：
  <blog>/
    <slug>/
      raw.html      — 原始 HTML
      original.md   — 英文 Markdown
      images/       — 该篇文章的图片
"""
import os, re, time, urllib.request, html2text, sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
BASE_HEADERS = {"User-Agent": UA}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ANTHROPIC_ARTICLES = [
    ("infrastructure-noise", "https://www.anthropic.com/engineering/infrastructure-noise"),
    ("managed-agents", "https://www.anthropic.com/engineering/managed-agents"),
    ("claude-code-auto-mode", "https://www.anthropic.com/engineering/claude-code-auto-mode"),
    ("harness-design-long-running-apps", "https://www.anthropic.com/engineering/harness-design-long-running-apps"),
    ("eval-awareness-browsecomp", "https://www.anthropic.com/engineering/eval-awareness-browsecomp"),
    ("building-c-compiler", "https://www.anthropic.com/engineering/building-c-compiler"),
    ("AI-resistant-technical-evaluations", "https://www.anthropic.com/engineering/AI-resistant-technical-evaluations"),
    ("demystifying-evals-for-ai-agents", "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents"),
    ("effective-harnesses-for-long-running-agents", "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents"),
    ("advanced-tool-use", "https://www.anthropic.com/engineering/advanced-tool-use"),
    ("code-execution-with-mcp", "https://www.anthropic.com/engineering/code-execution-with-mcp"),
    ("claude-code-sandboxing", "https://www.anthropic.com/engineering/claude-code-sandboxing"),
    ("equipping-agents-for-the-real-world-with-agent-skills", "https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills"),
    ("effective-context-engineering-for-ai-agents", "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"),
    ("a-postmortem-of-three-recent-issues", "https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues"),
    ("writing-tools-for-agents", "https://www.anthropic.com/engineering/writing-tools-for-agents"),
    ("desktop-extensions", "https://www.anthropic.com/engineering/desktop-extensions"),
    ("multi-agent-research-system", "https://www.anthropic.com/engineering/multi-agent-research-system"),
    ("claude-code-best-practices", "https://www.anthropic.com/engineering/claude-code-best-practices"),
    ("claude-think-tool", "https://www.anthropic.com/engineering/claude-think-tool"),
    ("swe-bench-sonnet", "https://www.anthropic.com/engineering/swe-bench-sonnet"),
    ("building-effective-agents", "https://www.anthropic.com/engineering/building-effective-agents"),
    ("contextual-retrieval", "https://www.anthropic.com/engineering/contextual-retrieval"),
]

OPENAI_ARTICLES = [
    ("realtime-perplexity-computer", "https://developers.openai.com/blog/realtime-perplexity-computer"),
    ("designing-delightful-frontends-with-gpt-5-4", "https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4"),
    ("one-year-of-responses", "https://developers.openai.com/blog/one-year-of-responses"),
    ("skills-agents-sdk", "https://developers.openai.com/blog/skills-agents-sdk"),
    ("building-frontend-uis-with-codex-and-figma", "https://developers.openai.com/blog/building-frontend-uis-with-codex-and-figma"),
    ("run-long-horizon-tasks-with-codex", "https://developers.openai.com/blog/run-long-horizon-tasks-with-codex"),
    ("skills-shell-tips", "https://developers.openai.com/blog/skills-shell-tips"),
    ("15-lessons-building-chatgpt-apps", "https://developers.openai.com/blog/15-lessons-building-chatgpt-apps"),
    ("eval-skills", "https://developers.openai.com/blog/eval-skills"),
    ("skyscanner-codex-jetbrains-mcp", "https://developers.openai.com/blog/skyscanner-codex-jetbrains-mcp"),
    ("openai-for-developers-2025", "https://developers.openai.com/blog/openai-for-developers-2025"),
    ("updates-audio-models", "https://developers.openai.com/blog/updates-audio-models"),
    ("what-makes-a-great-chatgpt-app", "https://developers.openai.com/blog/what-makes-a-great-chatgpt-app"),
    ("responses-api", "https://developers.openai.com/blog/responses-api"),
    ("intro", "https://developers.openai.com/blog/intro"),
    ("codex-at-devday", "https://developers.openai.com/blog/codex-at-devday"),
    ("codex-for-documentation-dagster", "https://developers.openai.com/blog/codex-for-documentation-dagster"),
    ("realtime-api", "https://developers.openai.com/blog/realtime-api"),
]

CLAUDEAI_ARTICLES = [
    ("claude-managed-agents-what-just-launched", "https://claudeai.dev/blog/claude-managed-agents-what-just-launched"),
    ("conway-timeline-how-anthropic-is-building-always-on-agents", "https://claudeai.dev/blog/conway-timeline-how-anthropic-is-building-always-on-agents"),
    ("what-actually-leaked-around-claude-code", "https://claudeai.dev/blog/what-actually-leaked-around-claude-code"),
    ("did-claude-ship-auto-fix-in-the-cloud", "https://claudeai.dev/blog/did-claude-ship-auto-fix-in-the-cloud"),
    ("claudes-march-2026-shipping-sprint", "https://claudeai.dev/blog/claudes-march-2026-shipping-sprint"),
    ("anthropic-skill-creator-update-practical-guide", "https://claudeai.dev/blog/anthropic-skill-creator-update-practical-guide"),
    ("build-better-agent-skills-with-tests", "https://claudeai.dev/blog/build-better-agent-skills-with-tests"),
    ("build-cowork-plugin-from-scratch", "https://claudeai.dev/blog/build-cowork-plugin-from-scratch"),
    ("choosing-ai-agent-workflow-patterns-that-ship", "https://claudeai.dev/blog/choosing-ai-agent-workflow-patterns-that-ship"),
    ("claude-1m-context-practical-rollout-guide", "https://claudeai.dev/blog/claude-1m-context-practical-rollout-guide"),
]

BLOGS = {
    "anthropic": ANTHROPIC_ARTICLES,
    "openai": OPENAI_ARTICLES,
    "claudeai-dev": CLAUDEAI_ARTICLES,
}


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers=BASE_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def resolve_img_url(img_url, page_url):
    if not img_url or img_url.startswith("data:"):
        return None
    if img_url.startswith("/"):
        return urljoin(page_url, img_url)
    if "=_next/image" in img_url and "url=" in img_url:
        parsed = urlparse(img_url)
        qs = parse_qs(parsed.query)
        real_url = qs.get("url", [""])[0]
        if real_url:
            return real_url
        return None
    return img_url


def download_img(img_url, save_dir, slug, idx):
    if not img_url:
        return None, None
    try:
        req = urllib.request.Request(img_url, headers=BASE_HEADERS)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
            content_type = r.headers.get("Content-Type", "")
        path = urlparse(img_url).path
        ext = os.path.splitext(path.split("/")[-1])[1]
        if not ext or len(ext) > 5:
            ext = ".png" if "png" in content_type else ".jpg"
        fname = f"{slug}_{idx:02d}{ext}"
        fpath = os.path.join(save_dir, fname)
        with open(fpath, "wb") as f:
            f.write(data)
        return fname, content_type
    except Exception as e:
        print(f"    [IMG ERR] {img_url[:80]}: {e}")
        return None, None


def html_to_md(html_content, page_url, blog_type):
    soup = BeautifulSoup(html_content, "lxml")
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else ""
    article = soup.find("article") or soup.find("main") or soup
    for tag in article.find_all(["nav", "header", "footer", "aside",
                                 "script", "style", "noscript"]):
        tag.decompose()
    for tag in article.find_all(["nav", "header", "footer"]):
        for child in tag.children:
            if hasattr(child, 'name') and child.name:
                tag.insert_before(child)
        tag.decompose()

    image_refs = []
    for idx, img in enumerate(article.find_all("img")):
        raw_src = img.get("src", "") or img.get("data-src", "")
        alt = img.get("alt", "")
        resolved = resolve_img_url(raw_src, page_url)
        if resolved:
            image_refs.append((raw_src, resolved, alt, idx))

    h = html2text.HTML2Text()
    h.body_width = 0
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.ignore_tables = False
    h.unicode_snob = True
    h.absolute_links = False
    h.default_image_alt = "image"

    md_raw = h.handle(str(article))

    lines = md_raw.split("\n")
    cleaned = []
    prev_empty = False
    for line in lines:
        is_empty = (line.strip() == "")
        if is_empty:
            if not prev_empty:
                cleaned.append("")
            prev_empty = True
        else:
            cleaned.append(line.rstrip())
            prev_empty = False
    md = "\n".join(cleaned).strip()
    md = re.sub(r'^##?\s*\*\*([^*]+)\*\*$', r'## \1', md, flags=re.MULTILINE)
    md = re.sub(r'^###?\s*\*\*([^*]+)\*\*$', r'### \1', md, flags=re.MULTILINE)
    md = re.sub(r'^(#{2,})\s*\*(.+?)\*\*$', r'\1 \2', md, flags=re.MULTILINE)
    md = re.sub(r'\n{3,}', '\n\n', md)

    return md, title, image_refs


def fetch_and_save(url, blog_type, slug):
    """每篇文章一个文件夹：raw.html / original.md / images/"""
    article_dir = os.path.join(BASE_DIR, blog_type, slug)
    os.makedirs(article_dir, exist_ok=True)
    img_dir = os.path.join(article_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    print(f"  Fetching: {url}")
    html = fetch(url)

    with open(os.path.join(article_dir, "raw.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Converting...")
    md, title, image_refs = html_to_md(html, url, blog_type)

    print(f"  Downloading {len(image_refs)} images...")
    local_map = {}
    for idx, (raw_src, resolved_url, alt, orig_idx) in enumerate(image_refs):
        fname, ctype = download_img(resolved_url, img_dir, slug, idx)
        if fname:
            local_map[raw_src] = fname
            print(f"    [{idx+1}] {fname}")

    md_img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    def replace_img_ref(m):
        alt_text, url = m.group(1), m.group(2)
        if url in local_map:
            return f"![{alt_text}]({local_map[url]})"
        url_no_qs = url.split("?")[0]
        for raw_src, fname in local_map.items():
            raw_no_qs = raw_src.split("?")[0]
            if url_no_qs == raw_no_qs or url in raw_src or raw_src in url:
                return f"![{alt_text}]({fname})"
        return m.group(0)

    md = md_img_pattern.sub(replace_img_ref, md)

    out_path = os.path.join(article_dir, "original.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\nSource: {url}\n\n---\n\n")
        f.write(md)

    img_count = len(local_map)
    print(f"  [OK] {slug} | title: {title[:50]} | imgs: {img_count}")
    return True, title, img_count


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    blog = sys.argv[2] if len(sys.argv) > 2 else None

    if mode == "single" and len(sys.argv) >= 4:
        slug = sys.argv[2]
        blog_type = sys.argv[3]
        articles = BLOGS.get(blog_type, [])
        url = next((u for s, u in articles if s == slug), None)
        if not url:
            print(f"URL not found for slug: {slug}")
            sys.exit(1)
        fetch_and_save(url, blog_type, slug)

    elif mode in ("all", "blog") and blog:
        articles = BLOGS.get(blog, [])
        if not articles:
            print(f"Unknown blog: {blog}")
            sys.exit(1)
        print(f"\n=== {blog} ({len(articles)} articles) ===")
        for slug, url in articles:
            try:
                fetch_and_save(url, blog, slug)
                time.sleep(1)
            except Exception as e:
                print(f"  [ERROR] {slug}: {e}")

    elif mode == "all":
        for blog_name, articles in BLOGS.items():
            print(f"\n=== {blog_name} ({len(articles)} articles) ===")
            for slug, url in articles:
                try:
                    fetch_and_save(url, blog_name, slug)
                    time.sleep(1)
                except Exception as e:
                    print(f"  [ERROR] {slug}: {e}")

    else:
        print("Usage:")
        print("  python fetch_articles.py all                          # 抓取全部 51 篇")
        print("  python fetch_articles.py blog anthropic              # 只抓 anthropic 23 篇")
        print("  python fetch_articles.py blog openai                  # 只抓 openai 18 篇")
        print("  python fetch_articles.py blog claudeai-dev            # 只抓 claudeai-dev 10 篇")
        print("  python fetch_articles.py single <slug> <blog_type>   # 抓单篇测试")


if __name__ == "__main__":
    main()
