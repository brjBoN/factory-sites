"""Generate landing-page concept images for a prospect via OpenAI's Images API.

Replaces the ChatGPT-courier step: concepts are generated here, saved under
concepts/<slug>/, and shown to Braden for the mandatory approval gate
(CLAUDE.md workflow step 2 — he still approves exactly ONE).

Auth: reads OPENAI_API_KEY from the environment. NEVER hardcode or commit a
key (this repo is public); Braden sets it once with
    setx OPENAI_API_KEY "sk-proj-..."
in his own terminal, then new sessions inherit it.

Usage:
  python tools/concept_gen.py <slug> "<prompt>" [--n 3] [--size 1536x1024]
                              [--quality high] [--name concept]

Prompt-writing guidance (what worked for Quality Tooling's brief):
  * Give the business facts (name, trade, town, product types) and the mood.
  * Specify palette as literal hex values and the typography CLASS
    ("Times-class serif display caps"), not font names the model will mangle.
  * Describe the layout structurally: "full-bleed split hero, left panel X,
    right panel Y, thin tracked-caps utility bar, product strip of 4 cards".
  * Ask for "no text other than …" sparingly — baked-in text will need
    inpainting later (hard rule 8) if it survives to the build.
  * 1536x1024 for desktop landing concepts; --n 2 or 3 variants per brief.

Cost (gpt-image-1, 2026): high/1536x1024 ~$0.25/image; medium ~$0.06.
A 3-variant concept round at high quality ≈ 75 cents.
"""
import argparse, base64, json, os, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = 'https://api.openai.com/v1/images/generations'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slug')
    ap.add_argument('prompt')
    ap.add_argument('--n', type=int, default=3, help='number of variants (generated one call each)')
    ap.add_argument('--size', default='1536x1024', choices=['1024x1024', '1536x1024', '1024x1536'])
    ap.add_argument('--quality', default='high', choices=['low', 'medium', 'high'])
    ap.add_argument('--name', default='concept', help='filename stem')
    a = ap.parse_args()

    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        sys.exit('OPENAI_API_KEY is not set. Braden: run  setx OPENAI_API_KEY "sk-proj-..."  '
                 'in your own terminal (never paste the key into chat or this repo), then start a new session.')

    outdir = ROOT / 'concepts' / a.slug
    outdir.mkdir(parents=True, exist_ok=True)

    for i in range(1, a.n + 1):
        body = json.dumps({
            'model': 'gpt-image-1',
            'prompt': a.prompt,
            'size': a.size,
            'quality': a.quality,
            'n': 1,
        }).encode()
        req = urllib.request.Request(API, data=body, method='POST', headers={
            'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
        print(f'[{i}/{a.n}] generating ({a.quality}, {a.size}) ...', flush=True)
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors='replace')[:500]
            sys.exit(f'OpenAI API error {e.code}: {detail}\n'
                     '(403/verification errors: the OpenAI org may need to complete '
                     'organization verification for gpt-image-1 at platform.openai.com.)')
        img = base64.b64decode(data['data'][0]['b64_json'])
        out = outdir / f'{a.name}-{i}.png'
        out.write_bytes(img)
        print(f'  -> {out.relative_to(ROOT)} ({len(img) // 1024} KB)')

    print('\nDone. Review the variants, then Braden approves exactly ONE (mandatory gate).')

if __name__ == '__main__':
    main()
