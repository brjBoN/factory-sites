"""Render an outreach handoff markdown file as a polished PDF.

The PDF is the human-facing deliverable (CLAUDE.md workflow step 5); the .md
stays the source of truth. Parses only the standardized handoff format:
H1 title, logo image line, meta line, H2 sections, paragraphs, bold, inline
code, links, blockquote warnings, pipe tables, ordered/unordered lists.

Styling uses the prospect site's design tokens (per-slug table below) so the
brief previews the concept site's identity.

Usage: python tools/handoff_pdf.py <slug>     e.g. quality-tooling
Reads  outreach/<slug>-handoff.md  ->  writes  outreach/<slug>-handoff.pdf
"""
import re, sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, Image, KeepTogether)
from reportlab.lib import utils

ROOT = Path(__file__).resolve().parents[1]

TOKENS = {
    'quality-tooling': {'bg': '#F1EDE4', 'primary': '#1E3A5C', 'accent': '#E05A2B',
                        'serif': 'Times-Roman', 'serif_b': 'Times-Bold'},
    'three-crazy-bakers': {'bg': '#F5ECDD', 'primary': '#0B2341', 'accent': '#C74632',
                           'band': '#0B2341',  # navy logo band: their logo is white-on-transparent
                           'serif': 'Times-Roman', 'serif_b': 'Times-Bold'},
    '_default':        {'bg': '#F2F2F0', 'primary': '#222222', 'accent': '#B4552D',
                        'serif': 'Times-Roman', 'serif_b': 'Times-Bold'},
}

# WinAnsi-safe replacements for glyphs the built-in fonts lack
SANITIZE = {'→': '->', '←': '<-', '″': '"', '⚠': '', '️': '',
            '★': '*', '✓': 'yes', '✗': 'no', '⭐': '*', '❤': '', '←': '<-'}

def sanitize(s):
    for k, v in SANITIZE.items():
        s = s.replace(k, v)
    return s

def md_inline(s):
    """Markdown inline -> reportlab paragraph XML."""
    s = sanitize(s)
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<i>\1</i>', s)
    s = re.sub(r'`([^`]+)`', r'<font face="Courier" size="8.5">\1</font>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<link href="\2" color="#1155CC"><u>\1</u></link>', s)
    s = re.sub(r'(?<![\w>])(https?://[^\s<,)]+)', r'<link href="\1" color="#1155CC"><u>\1</u></link>', s)
    return s

def parse(md):
    """Very small block parser for the standardized handoff format."""
    blocks, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith('# '):
            blocks.append(('h1', ln[2:].strip()))
        elif ln.startswith('## '):
            blocks.append(('h2', ln[3:].strip()))
        elif m := re.match(r'!\[([^\]]*)\]\(([^)]+)\)', ln.strip()):
            blocks.append(('img', m.group(2)))
        elif ln.lstrip().startswith('>'):
            quote = []
            while i < len(lines) and lines[i].lstrip().startswith('>'):
                quote.append(lines[i].lstrip()[1:].strip()); i += 1
            blocks.append(('quote', ' '.join(q for q in quote if q))); continue
        elif ln.strip().startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(('table', rows)); continue
        elif re.match(r'\s*(\d+\.|[-*])\s', ln):
            items = []
            while i < len(lines) and (m := re.match(r'(\s*)(\d+\.|[-*])\s+(.*)', lines[i])):
                indent, marker, text = len(m.group(1)), m.group(2), m.group(3)
                # absorb hanging continuation lines
                j = i + 1
                while j < len(lines) and lines[j].strip() and not re.match(r'\s*(\d+\.|[-*])\s', lines[j]) \
                        and not lines[j].startswith(('#', '>', '|', '!')):
                    text += ' ' + lines[j].strip(); j += 1
                items.append((indent > 1, marker.rstrip('.'), text))
                i = j
            blocks.append(('list', items)); continue
        else:
            text = ln.strip()
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].startswith(('#', '>', '|', '!', '-', '*')) \
                    and not re.match(r'\s*\d+\.\s', lines[j]):
                text += ' ' + lines[j].strip(); j += 1
            blocks.append(('p', text)); i = j; continue
        i += 1
    return blocks

def build(slug):
    src = ROOT / 'outreach' / f'{slug}-handoff.md'
    out = ROOT / 'outreach' / f'{slug}-handoff.pdf'
    tok = TOKENS.get(slug, TOKENS['_default'])
    BG, PRIMARY, ACCENT = HexColor(tok['bg']), HexColor(tok['primary']), HexColor(tok['accent'])
    md = src.read_text(encoding='utf-8')
    blocks = parse(md)

    S = {
        'h1':    ParagraphStyle('h1', fontName=tok['serif_b'], fontSize=21, leading=25,
                                textColor=PRIMARY, spaceAfter=2),
        'meta':  ParagraphStyle('meta', fontName='Helvetica', fontSize=8.5, leading=12,
                                textColor=HexColor('#6b6459'), spaceAfter=10),
        'h2':    ParagraphStyle('h2', fontName=tok['serif_b'], fontSize=13.5, leading=17,
                                textColor=PRIMARY, spaceBefore=13, spaceAfter=5),
        'p':     ParagraphStyle('p', fontName='Helvetica', fontSize=9.5, leading=13.5,
                                textColor=HexColor('#26221c'), spaceAfter=5, alignment=TA_LEFT),
        'li':    ParagraphStyle('li', fontName='Helvetica', fontSize=9.5, leading=13.5,
                                textColor=HexColor('#26221c'), spaceAfter=3.5),
        'quote': ParagraphStyle('quote', fontName='Helvetica-Bold', fontSize=9.5, leading=13.5,
                                textColor=PRIMARY),
        'th':    ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=white),
        'td':    ParagraphStyle('td', fontName='Helvetica', fontSize=9, leading=12.5,
                                textColor=HexColor('#26221c')),
    }

    story, first_h2_seen = [], False
    W = letter[0] - 1.44 * inch  # usable width

    def bullet_table(items):
        data, style = [], [
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 1.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5)]
        for r, (sub, marker, text) in enumerate(items):
            mk = ('&bull;' if marker in '-*' else f'<b>{marker}.</b>')
            data.append([
                '', Paragraph(f'<font color="{tok["accent"]}">{mk}</font>', S['li']),
                Paragraph(md_inline(text), S['li'])])
            if sub:  # indent sub-bullets via per-row padding
                style.append(('LEFTPADDING', (1, r), (2, r), 14))
        t = Table(data, colWidths=[2, 18, W - 20])
        t.setStyle(TableStyle(style))
        return t

    i = 0
    while i < len(blocks):
        kind, val = blocks[i]
        if kind == 'h1':
            story.append(Paragraph(md_inline(val), S['h1']))
        elif kind == 'img':
            img_path = (ROOT / 'outreach' / val).resolve()
            if img_path.exists():
                ir = utils.ImageReader(str(img_path))
                iw, ih = ir.getSize()
                h = 0.72 * inch
                w = iw * h / ih
                logo = Image(str(img_path), width=w, height=h)
                band = Table([[logo]], colWidths=[W], rowHeights=[h + 18])
                band_color = HexColor(tok['band']) if 'band' in tok else BG
                band.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), band_color),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LINEBELOW', (0, 0), (-1, -1), 2, ACCENT)]))
                story.append(Spacer(1, 4)); story.append(band); story.append(Spacer(1, 8))
        elif kind == 'h2':
            first_h2_seen = True
            story.append(Paragraph(md_inline(val), S['h2']))
        elif kind == 'p':
            style = S['p'] if first_h2_seen else S['meta']
            story.append(Paragraph(md_inline(val), style))
        elif kind == 'quote':
            q = Table([[Paragraph(md_inline(val), S['quote'])]], colWidths=[W])
            q.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), BG),
                ('LINEBEFORE', (0, 0), (0, -1), 3, ACCENT),
                ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
            story.append(Spacer(1, 3)); story.append(q); story.append(Spacer(1, 5))
        elif kind == 'table':
            head, *body = val
            data = [[Paragraph(md_inline(c), S['th']) for c in head]] + \
                   [[Paragraph(md_inline(c), S['td']) for c in r] for r in body]
            first_col = 1.35 * inch if len(head) > 2 else W / len(head)
            widths = [first_col] + [(W - first_col) / (len(head) - 1)] * (len(head) - 1) if len(head) > 2 \
                     else [W / len(head)] * len(head)
            t = Table(data, colWidths=widths, repeatRows=1)
            style = [('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
                     ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                     ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#d8d2c6')),
                     ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                     ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]
            for r in range(1, len(data)):
                if r % 2 == 0:
                    style.append(('BACKGROUND', (0, r), (-1, r), BG))
            t.setStyle(TableStyle(style))
            story.append(Spacer(1, 2)); story.append(t); story.append(Spacer(1, 4))
        elif kind == 'list':
            story.append(bullet_table(val)); story.append(Spacer(1, 3))
        i += 1

    def decorate(canvas, doc_):
        canvas.saveState()
        canvas.setFillColor(ACCENT)
        canvas.rect(0, letter[1] - 0.18 * inch, letter[0], 0.18 * inch, stroke=0, fill=1)
        canvas.setFont('Helvetica', 7.5)
        canvas.setFillColor(HexColor('#8a8272'))
        canvas.drawString(0.72 * inch, 0.45 * inch, 'Internal — outreach use only. Do not leave with the prospect.')
        canvas.drawRightString(letter[0] - 0.72 * inch, 0.45 * inch, f'Page {doc_.page}')
        canvas.restoreState()

    doc = BaseDocTemplate(str(out), pagesize=letter,
                          leftMargin=0.72 * inch, rightMargin=0.72 * inch,
                          topMargin=0.55 * inch, bottomMargin=0.7 * inch,
                          title=f'Outreach Handoff — {slug}', author='factory-sites')
    frame = Frame(0.72 * inch, 0.7 * inch, W, letter[1] - 1.25 * inch, id='main')
    doc.addPageTemplates([PageTemplate(id='page', frames=[frame], onPage=decorate)])
    doc.build(story)
    print(f'wrote {out} ({out.stat().st_size // 1024} KB)')

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'quality-tooling')
