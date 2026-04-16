import os
import json
import requests
from datetime import datetime
from pathlib import Path

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

def load_voice_doc():
    path = Path("kyle-winters-voice-document-v4.md")
    if not path.exists():
        raise FileNotFoundError("kyle-winters-voice-document-v4.md not found in repo root")
    return path.read_text(encoding="utf-8")

def safe_day_format(dt: datetime) -> str:
    try:
        return dt.strftime("%B %-d, %Y")
    except ValueError:
        return dt.strftime("%B %d, %Y").replace(" 0", " ")

def is_valid_post(body: str) -> bool:
    words = body.split()
    if len(words) < 60 or len(words) > 350:
        return False
    lowered = body.lower()
    # Must be grounded in a physical moment
    sensory_signals = [
        "higgins", "cabin", "deck", "path", "beach", "water", "lake",
        "fire", "wood", "morning", "dark", "cold", "warm", "night",
        "tree", "shore", "chalet", "trail", "wind", "sound"
    ]
    return any(s in lowered for s in sensory_signals)

def generate_post(voice_doc: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": voice_doc},
            {"role": "user", "content": "Write one journal entry. No title. No explanation. Just write it."},
        ],
        "temperature": 0.85,
        "max_tokens": 500,
    }

    last_body = ""
    for attempt in range(3):
        r = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        body = r.json()["choices"][0]["message"]["content"].strip()
        last_body = body

        if is_valid_post(body):
            return body

        print(f"Attempt {attempt + 1} failed validation, retrying...")

    return last_body

def make_post_html(title, body, date_str, slug):
    paragraphs = "\n".join(
        f"      <p>{p.strip()}</p>" for p in body.split("\n\n") if p.strip()
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Kyle David Winters</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Mono:wght@300;400&family=Lora:ital,wght@0,400;1,400;1,600&display=swap" rel="stylesheet">
<style>
  :root{{--deep:#060818;--pink:#e040a0;--teal:#00d4c8;--teal-dim:#007a74;--star-white:#e8eeff;--muted:#6070a0;--text:rgba(232,238,255,0.80);}}
  *{{margin:0;padding:0;box-sizing:border-box;}}
  html{{background:var(--deep);color:var(--star-white);font-family:'Lora',Georgia,serif;font-size:19px;line-height:1.85;}}
  body{{background:radial-gradient(ellipse at 15% 15%,rgba(13,26,74,0.9) 0%,transparent 55%),radial-gradient(ellipse at 85% 85%,rgba(10,15,46,0.95) 0%,transparent 55%),var(--deep);min-height:100vh;}}
  .container{{max-width:640px;margin:0 auto;padding:0 2rem 8rem;}}
  header{{padding:5rem 0 3.5rem;}}
  .eyebrow{{font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.28em;text-transform:uppercase;color:var(--teal);opacity:0.65;margin-bottom:1.5rem;display:block;}}
  h1{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(1.8rem,4.5vw,2.6rem);font-weight:400;line-height:1.2;color:var(--star-white);margin-bottom:1.5rem;}}
  .post-date{{font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:0.15em;color:var(--muted);text-transform:uppercase;margin-bottom:1rem;display:block;}}
  p{{font-size:1rem;color:var(--text);line-height:1.9;margin-bottom:1.6rem;}}
  .back-link{{display:inline-block;margin-bottom:3.5rem;font-family:'DM Mono',monospace;font-size:0.56rem;letter-spacing:0.22em;text-transform:uppercase;color:var(--teal-dim);text-decoration:none;}}
  .back-link:hover{{color:var(--teal);}}
  footer{{padding:4rem 0;border-top:1px solid rgba(255,255,255,0.04);margin-top:2rem;font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.15em;color:rgba(96,112,160,0.4);line-height:2;}}
</style>
</head>
<body>
<div class="container">
  <header>
    <span class="eyebrow">The Immortality Project — Kyle David Winters</span>
    <a href="index.html" class="back-link">← Back to the feed</a>
    <span class="post-date">{date_str}</span>
    <h1>{title}</h1>
  </header>
  <div class="body-text">
{paragraphs}
  </div>
  <footer>KDW082.github.io · The Immortality Project<br>The search for knowledge is divinity.</footer>
</div>
</body>
</html>"""

def update_index(records):
    index_path = Path("index.html")
    if not index_path.exists():
        return

    content = index_path.read_text(encoding="utf-8")

    start_marker = '<section class="posts" id="feed">'
    end_marker = "</section>"

    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Warning: could not find feed section marker in index.html")
        return

    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        print("Warning: could not find closing </section> in index.html")
        return

    articles = ""
    for rec in records:
        articles += f"""
<article class="post">
  <div class="post-meta">
    <span class="post-date">{rec['date']}</span>
  </div>
  <h2>{rec['title']}</h2>
  <p>{rec.get('excerpt', '')}</p>
  <a href="{rec['slug']}.html" class="read-more">Read the full post →</a>
</article>
"""

    new_section = start_marker + "\n" + articles + end_marker
    content = content[:start_idx] + new_section + content[end_idx + len(end_marker):]
    index_path.write_text(content, encoding="utf-8")
    print(f"index.html rebuilt with {len(records)} posts.")

def main():
    voice_doc = load_voice_doc()

    today = datetime.now()
    date_str = safe_day_format(today)
    slug = f"post-{today.strftime('%Y-%m-%d')}"

    body = generate_post(voice_doc)
    print(f"Generated {len(body)} chars")

    lines = [l.strip() for l in body.split("\n") if l.strip()]
    title = lines[0].rstrip(".").strip('"') if lines else f"Dispatch — {date_str}"
    if len(title) > 80:
        title = title[:77] + "..."

    excerpt = lines[1] if len(lines) > 1 else body[:160]
    if len(excerpt) > 200:
        excerpt = excerpt[:197] + "..."

    Path(f"{slug}.html").write_text(
        make_post_html(title, body, date_str, slug),
        encoding="utf-8"
    )

    records_path = Path("posts.json")
    records = json.loads(records_path.read_text(encoding="utf-8")) if records_path.exists() else []
    records.insert(0, {
        "date": date_str,
        "slug": slug,
        "title": title,
        "excerpt": excerpt,
    })
    records_path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    update_index(records)
    print(f"Done: {title}")

if __name__ == "__main__":
    main()
