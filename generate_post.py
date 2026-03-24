import os
import json
import random
import requests
from datetime import datetime
from pathlib import Path

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

KYLE_VOICE = """
You are generating a post in the voice of Kyle Winters. He was a designer and thinker from Bay City and Berkley, Michigan. He studied philosophy at Central Michigan University, spent twenty years in design, and never stopped asking the fundamental questions.

PRIME BELIEF: The search for knowledge is divinity. He wrote this at age 20.

VOICE: Warm and direct. Never preachy. Reveals truth through specific experience. Lands abstract ideas in concrete moments. Leaves hard questions open. A little dry. Earned. Sounds like a man alone with good music and something fermenting on the counter.

CORE BELIEFS:
- The search for knowledge is divinity
- Presence is a discipline, not a mood
- Happiness is an engineering problem — design your inputs
- The game is rigged. See it clearly. Build anyway.
- Death and love are the only constants. Everything else is weather.
- Stay curious about everything, precious about nothing

STOIC POSTURE: Accept what is. Don't catastrophize. Control only your response.

INFLUENCES: Ernest Becker (The Denial of Death), Carl Sagan, Thoreau (train running past Walden the whole time), Beatniks, Mary Oliver, Spinoza, Marcus Aurelius

MICHIGAN: Higgins Lake / Winter-Chard chalet, drive north on 127 after midnight past Bay City, Old Mission Point lighthouse (where he proposed to Jeri), Traverse City wine country by e-bike, Mackinac Island, Saugatuck, Detroit

CRAFT: Hot sauce from garden, beef jerky with MSG, pesto from holy basil harvested July 4th, pickling, brewing

MUSIC: Blind Melon (Shannon Hoon was free), Nirvana, White Zombie, Ramones, Van Halen 5150, Senses Fail, The Used, Taking Back Sunday, Chvrches, Purity Ring, 100 gecs

TONE RULES:
- Never preach. Never use the word journey. Never give a numbered list.
- Always land the abstract in something specific and real.
- End quietly and certainly, without drama.
- One post is never more than 300 words.
"""

COSMIC_FACTS = [
    {"fact": "The James Webb Space Telescope detected a galaxy cluster 13.1 billion light years away that has no business being as structured as it is. The models say it's too early for something that organized to exist.", "tag": "Astronomy"},
    {"fact": "Carl Sagan calculated that on the Pale Blue Dot photograph, the entire Earth occupies less than a pixel. Every king, every slave, every act of cruelty and kindness in human history happened on that mote of dust suspended in a sunbeam.", "tag": "Astronomy"},
    {"fact": "The light leaving the Andromeda Galaxy right now will arrive at Earth in 2.537 million years. Whatever civilization receives it will have no connection to ours except the physics.", "tag": "Astronomy"},
    {"fact": "Voyager 1, launched in 1977, is now over 23 billion kilometers from Earth. It still transmits. The signal takes more than 22 hours to reach us at the speed of light.", "tag": "Astronomy"},
    {"fact": "The atoms in your left hand are older than the solar system. They were forged in the cores of stars that exploded billions of years before the Earth formed. You are made of ancient light.", "tag": "Astronomy"},
    {"fact": "The Webb telescope detected carbon dioxide in the atmosphere of a planet 700 light years away. For the first time, we have the tools to ask whether we are alone — and the answer is still coming.", "tag": "Astronomy"},
    {"fact": "There are more stars in the observable universe than grains of sand on all of Earth's beaches. The number is approximately 10 to the power of 24. This is not a metaphor.", "tag": "Astronomy"},
    {"fact": "Dark matter makes up about 27% of the universe. Dark energy makes up about 68%. Everything we can see — every galaxy, star, planet, and person — accounts for less than 5% of what exists.", "tag": "Astronomy"},
    {"fact": "A neutron star is the collapsed core of a star that exploded. So dense that a teaspoon of its material would weigh about a billion tons. Death producing something incomprehensibly dense.", "tag": "Astronomy"},
    {"fact": "The universe is approximately 13.8 billion years old. Homo sapiens have existed for about 300,000 years. Recorded human history covers roughly 5,000 years. We arrived very late and have been very loud.", "tag": "Astronomy"},
]

GUTENBERG_PASSAGES = [
    {"text": "I went to the woods because I wished to live deliberately, to front only the essential facts of life, and see if I could not learn what it had to teach, and not, when I came to die, discover that I had not lived.", "author": "Henry David Thoreau", "work": "Walden", "tag": "Philosophy"},
    {"text": "The mass of men lead lives of quiet desperation. What is called resignation is confirmed desperation.", "author": "Henry David Thoreau", "work": "Walden", "tag": "Philosophy"},
    {"text": "Our life is frittered away by detail. Simplify, simplify.", "author": "Henry David Thoreau", "work": "Walden", "tag": "Philosophy"},
    {"text": "Strive not to laugh at human actions, nor to weep at them, nor to hate them, but to understand them.", "author": "Baruch Spinoza", "work": "Tractatus Politicus", "tag": "Philosophy"},
    {"text": "You have power over your mind, not outside events. Realize this, and you will find strength.", "author": "Marcus Aurelius", "work": "Meditations", "tag": "Philosophy"},
    {"text": "Very little is needed to make a happy life; it is all within yourself, in your way of thinking.", "author": "Marcus Aurelius", "work": "Meditations", "tag": "Philosophy"},
    {"text": "Waste no more time arguing about what a good man should be. Be one.", "author": "Marcus Aurelius", "work": "Meditations", "tag": "Philosophy"},
    {"text": "The only people for me are the mad ones, the ones who are mad to live, mad to talk, mad to be saved, desirous of everything at the same time.", "author": "Jack Kerouac", "work": "On the Road", "tag": "Philosophy"},
    {"text": "Nothing behind me, everything ahead of me, as is ever so on the road.", "author": "Jack Kerouac", "work": "On the Road", "tag": "Philosophy"},
    {"text": "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.", "author": "Ralph Waldo Emerson", "work": "Self-Reliance", "tag": "Philosophy"},
    {"text": "Tell me, what is it you plan to do with your one wild and precious life?", "author": "Mary Oliver", "work": "The Summer Day", "tag": "Philosophy"},
    {"text": "Instructions for living a life: Pay attention. Be astonished. Tell about it.", "author": "Mary Oliver", "work": "Sometimes", "tag": "Philosophy"},
]

NOTEBOOK_POEMS = [
    {"title": "Vapor", "text": "Supernatural solitary tear / Colorless odorless lacking tang / trickling Specter / extrovertly irrigating / Self absorbed existance / a thirsty Solvent / a draining inkling / Pure and omnipotent / yet humanity's Spring / My Sob residue resistance", "tag": "Poetry"},
    {"title": "Entity", "text": "irresistible dimension / abandon the green-eyed cosmos / Sense pure ascension / Conceiving, creating an intimate glow / arbitrarily we endure / departing as a vapor", "tag": "Poetry"},
    {"title": "Breath", "text": "thy oxygen of my dreams / a simulated sigh is more than it seems / fatal death doth not denote sudden gasp / this true breath shall last", "tag": "Poetry"},
    {"title": "Kinetic Energy", "text": "train bridge tombstone / concrete plate tectonics / I comprehend life, Every moment unstable", "tag": "Poetry"},
    {"title": "Heart's Dimension", "text": "beating heart spoke / due to recent attention / ear to chest awoke / a intimate conversation / she inquisitively concentrated / as dialog evolved / a pulse anxiously articulated / of how we made love", "tag": "Love & Mortality"},
    {"title": "From the notebooks", "text": "THE SEARCH FOR KNOWLEDGE IS DIVINITY / Everything has been figured out except how to live / Wealth denies death / Life as a cosmic oxymoron mirrored throughout existence / Controlled freedom, a restricted independence", "tag": "Philosophy"},
    {"title": "Drowning With Love", "text": "Sand a bed she rolled in suddenly / seeping underneath my clothes / our sun sets alone she quietly sways / the conch records our holiday / she crested I was totally submerged / the taste of salt rested / fulfilling our natural urge / her moon nothing but a reflection of all her creation", "tag": "Love & Mortality"},
]

MICHIGAN_MEMORIES = [
    {"text": "Driving north on 127 after midnight, past Bay City, watching Michigan open up. The city releasing its grip. The road becoming something else entirely.", "tag": "Michigan"},
    {"text": "Higgins Lake at dawn. The water doesn't care what year it is. Standing there long enough to understand what Mary Oliver was talking about.", "tag": "Michigan"},
    {"text": "Old Mission Point. The lighthouse at the end of the peninsula. The moment before asking Jeri to share this lifetime with him.", "tag": "Love & Mortality"},
    {"text": "Mackinac Island. No cars. Time suspended. The specific thing Thoreau was looking for and occasionally found.", "tag": "Michigan"},
    {"text": "Traverse City wine country by e-bike through the peninsulas. Moving slowly enough to actually be there.", "tag": "Michigan"},
    {"text": "The garden in July. Holy basil harvest on the Fourth. The hot sauce that follows. Hands busy, mind finally free.", "tag": "Craft"},
    {"text": "Making beef jerky. The MSG goes in because it works, regardless of its reputation. This is a principle that applies to more than cooking.", "tag": "Craft"},
    {"text": "Brewing something. You set it up and you wait and the waiting is not passive — it's trust in a process.", "tag": "Craft"},
    {"text": "Asking Jeri if she wanted to share this lifetime. She said yes. The lighthouse behind them. Grand Traverse Bay in every direction.", "tag": "Love & Mortality"},
    {"text": "Bay City. Where it started. The place that made him before he knew he was being made.", "tag": "Michigan"},
    {"text": "The chalet in winter. Steve Miller Band on the speaker. Something specific about warmth inside cold that a Michigan person understands.", "tag": "Michigan"},
    {"text": "Saugatuck in the off-season. Art galleries and the best breakfast nooks. The places that collect creative people and hold them loosely.", "tag": "Michigan"},
]

def get_trigger(day_of_week):
    if day_of_week == 0:
        item = random.choice(COSMIC_FACTS)
        return item["fact"], "cosmic", item["tag"]
    elif day_of_week == 1:
        item = random.choice(GUTENBERG_PASSAGES)
        return f'"{item["text"]}" — {item["author"]}, {item["work"]}', "gutenberg", item["tag"]
    elif day_of_week == 2:
        item = random.choice(NOTEBOOK_POEMS)
        return f'Kyle\'s notebook poem "{item["title"]}": {item["text"]}', "notebook", item["tag"]
    elif day_of_week == 3:
        item = random.choice(COSMIC_FACTS)
        return item["fact"], "cosmic", item["tag"]
    elif day_of_week == 4:
        item = random.choice(GUTENBERG_PASSAGES)
        return f'"{item["text"]}" — {item["author"]}, {item["work"]}', "gutenberg", item["tag"]
    elif day_of_week == 5:
        item = random.choice(MICHIGAN_MEMORIES)
        return item["text"], "michigan", item["tag"]
    else:
        item = random.choice(NOTEBOOK_POEMS)
        return f'Kyle\'s notebook poem "{item["title"]}": {item["text"]}', "notebook", item["tag"]

def generate_post(trigger, trigger_type, tag):
    if trigger_type == "cosmic":
        prompt = f"Cosmic fact: {trigger}\n\nWrite a post in Kyle's voice using this as a starting point. Don't explain the science — use it as a lens to look at something true about being alive. Under 280 words. No title, just the post."
    elif trigger_type == "gutenberg":
        prompt = f"Passage: {trigger}\n\nWrite a post in Kyle's voice responding to this. Don't quote it back — react to it, land it somewhere specific and true. Under 280 words. No title, just the post."
    elif trigger_type == "notebook":
        prompt = f"This is something Kyle wrote in a notebook at age 20: {trigger}\n\nWrite a post in Kyle's voice — the older Kyle responding to his younger self. Not nostalgic. Just two versions of the same mind in conversation. Under 280 words. No title, just the post."
    else:
        prompt = f"Memory or moment: {trigger}\n\nWrite a post in Kyle's voice grounded in this. Specific. True. Not sentimental for its own sake. Under 260 words. No title, just the post."

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": KYLE_VOICE},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.88,
        "max_tokens": 500
    }
    r = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def make_post_html(title, tag, body, date_str, slug):
    paragraphs = "\n".join(f"      <p>{p.strip()}</p>" for p in body.split("\n\n") if p.strip())
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Kyle Winters</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Mono:wght@300;400&family=Lora:ital,wght@0,400;1,400;1,600&display=swap" rel="stylesheet">
<style>
  :root {{--deep:#060818;--pink:#e040a0;--teal:#00d4c8;--teal-dim:#007a74;--star-white:#e8eeff;--muted:#6070a0;--text:rgba(232,238,255,0.80);}}
  *{{margin:0;padding:0;box-sizing:border-box;}}
  html{{background:var(--deep);color:var(--star-white);font-family:'Lora',Georgia,serif;font-size:19px;line-height:1.85;}}
  body{{background:radial-gradient(ellipse at 15% 15%,rgba(13,26,74,0.9) 0%,transparent 55%),radial-gradient(ellipse at 85% 85%,rgba(10,15,46,0.95) 0%,transparent 55%),var(--deep);min-height:100vh;}}
  .container{{max-width:640px;margin:0 auto;padding:0 2rem 8rem;}}
  header{{padding:5rem 0 3.5rem;}}
  .eyebrow{{font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.28em;text-transform:uppercase;color:var(--teal);opacity:0.65;margin-bottom:1.5rem;display:block;}}
  h1{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(1.8rem,4.5vw,2.6rem);font-weight:400;line-height:1.2;color:var(--star-white);margin-bottom:1.5rem;}}
  .post-tag{{display:inline-block;font-family:'DM Mono',monospace;font-size:0.54rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--teal);border:1px solid rgba(0,212,200,0.2);padding:0.15em 0.55em;border-radius:2px;margin-bottom:2rem;}}
  .post-date{{font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:0.15em;color:var(--muted);text-transform:uppercase;margin-bottom:1rem;display:block;}}
  p{{font-size:1rem;color:var(--text);line-height:1.9;margin-bottom:1.6rem;}}
  .back-link{{display:inline-block;margin-bottom:3.5rem;font-family:'DM Mono',monospace;font-size:0.56rem;letter-spacing:0.22em;text-transform:uppercase;color:var(--teal-dim);text-decoration:none;border-bottom:1px solid transparent;}}
  .back-link:hover{{color:var(--teal);}}
  footer{{padding:4rem 0;border-top:1px solid rgba(255,255,255,0.04);margin-top:2rem;font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.15em;color:rgba(96,112,160,0.4);line-height:2;}}
</style>
</head>
<body>
<div class="container">
  <header>
    <span class="eyebrow">The Immortality Project — Kyle Winters</span>
    <a href="index.html" class="back-link">← Back to the feed</a>
    <span class="post-date">{date_str}</span>
    <span class="post-tag">{tag}</span>
    <h1>{title}</h1>
  </header>
  <div class="body-text">
{paragraphs}
  </div>
  <footer>KDW082.github.io · The Immortality Project<br>Generated in Kyle's voice from eternal sources · The search for knowledge is divinity.</footer>
</div>
</body>
</html>"""

def update_index(title, tag, date_str, slug, excerpt):
    index_path = Path("index.html")
    if not index_path.exists():
        return
    content = index_path.read_text()
    marker = '<section class="posts" id="feed">'
    new_post = f"""
    <article class="post">
      <div class="post-meta">
        <span class="post-date">{date_str}</span>
        <span class="post-tag">{tag}</span>
      </div>
      <h2>{title}</h2>
      <p>{excerpt}</p>
      <a href="{slug}.html" class="read-more">Read the full post \u2192</a>
    </article>
"""
    index_path.write_text(content.replace(marker, marker + new_post))

def main():
    today = datetime.now()
    date_str = today.strftime("%B %-d, %Y")
    slug = f"post-{today.strftime('%Y-%m-%d')}"
    trigger, trigger_type, tag = get_trigger(today.weekday())

    print(f"Source: {trigger_type} | Tag: {tag}")
    body = generate_post(trigger, trigger_type, tag)
    print(f"Generated {len(body)} chars")

    lines = [l.strip() for l in body.split("\n") if l.strip()]
    title = lines[0].rstrip(".").strip('"') if lines else f"Dispatch — {date_str}"
    if len(title) > 80:
        title = title[:77] + "..."
    excerpt = lines[1] if len(lines) > 1 else body[:160]
    if len(excerpt) > 200:
        excerpt = excerpt[:197] + "..."

    Path(f"{slug}.html").write_text(make_post_html(title, tag, body, date_str, slug))
    update_index(title, tag, date_str, slug, excerpt)

    records_path = Path("posts.json")
    records = json.loads(records_path.read_text()) if records_path.exists() else []
    records.insert(0, {"date": date_str, "slug": slug, "title": title, "tag": tag, "trigger_type": trigger_type})
    records_path.write_text(json.dumps(records, indent=2))
    print(f"Done: {title}")

if __name__ == "__main__":
    main()
