#!/usr/bin/env python3
"""편집점검보고서 Markdown → Word(.docx) 변환기.

사용법: python3 report_to_docx.py 보고서.md 출력.docx

지원: # 제목(1~4단계), 표(| 구분), 글머리·번호 목록, 체크리스트(- [ ]),
      **굵게**, *기울임*, `코드`, 구분선(---). 그 밖의 줄은 일반 문단.
"""
import re
import sys

try:
    from docx import Document
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from docx.shared import Pt, Mm, RGBColor
except ImportError:
    sys.exit("python-docx가 필요합니다: pip install python-docx")

FONT = "맑은 고딕"
GRADE_COLORS = {
    "[필수수정]": RGBColor(0xB0, 0x1E, 0x1E),
    "[강력권고]": RGBColor(0xC2, 0x5B, 0x00),
    "[권고]": RGBColor(0x1F, 0x5F, 0x99),
    "[확인필요]": RGBColor(0x6B, 0x3F, 0xA0),
}
INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`)")


def set_font(run, size=None, bold=None, italic=None, color=None):
    run.font.name = FONT
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.append(fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        fonts.set(qn(attr), FONT)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def add_inline(par, text, size=None, bold=False):
    for part in INLINE.split(text):
        if not part:
            continue
        b, i, t = bold, False, part
        if part.startswith("**") and part.endswith("**"):
            b, t = True, part[2:-2]
        elif part.startswith("`") and part.endswith("`"):
            t = part[1:-1]
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            i, t = True, part[1:-1]
        color = None
        for grade, c in GRADE_COLORS.items():
            if t.strip() == grade:
                color, b = c, True
        set_font(par.add_run(t), size=size, bold=b, italic=i, color=color)


def shade(cell, hex_color):
    tcpr = cell._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcpr.append(shd)


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells = re.split(r"(?<!\\)\|", line)
    return [c.strip().replace("\\|", "|") for c in cells]


def is_sep(line):
    return bool(re.match(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$", line))


def add_table(doc, rows):
    header, body = rows[0], rows[1:]
    ncol = max(len(r) for r in rows)
    table = doc.add_table(rows=0, cols=ncol)
    table.style = "Table Grid"
    for ri, row in enumerate([header] + body):
        cells = table.add_row().cells
        for ci in range(ncol):
            text = row[ci] if ci < len(row) else ""
            p = cells[ci].paragraphs[0]
            add_inline(p, text, size=8.5, bold=(ri == 0))
            if ri == 0:
                shade(cells[ci], "E8E4DA")
    # 머리행 반복
    trpr = table.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trpr.append(th)
    doc.add_paragraph()


def convert(md_path, out_path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    for side in ("left_margin", "right_margin"):
        setattr(sec, side, Mm(18))
    sec.top_margin = sec.bottom_margin = Mm(20)
    normal = doc.styles["Normal"]
    normal.font.size = Pt(10.5)
    normal.font.name = FONT
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)

    lines = open(md_path, encoding="utf-8").read().splitlines()
    i, n = 0, len(lines)
    in_code = False
    title_done = False
    while i < n:
        line = lines[i]
        if line.strip().startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            p = doc.add_paragraph()
            set_font(p.add_run(line), size=9)
            i += 1
            continue
        if "|" in line and i + 1 < n and is_sep(lines[i + 1]):
            rows = [split_row(line)]
            i += 2
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            add_table(doc, rows)
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            if level == 1 and not title_done:
                h, title_done = doc.add_heading(level=0), True
            else:
                h = doc.add_heading(level=max(1, level - 1) if title_done else level)
            add_inline(h, m.group(2).strip(), size={1: 18, 2: 15, 3: 13, 4: 11.5}[level], bold=True)
            i += 1
            continue
        if re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            i += 1
            continue
        m = re.match(r"^(\s*)[-*]\s+\[( |x|X)\]\s+(.*)", line)
        if m:
            p = doc.add_paragraph(style="List Bullet")
            add_inline(p, ("☑ " if m.group(2).strip() else "☐ ") + m.group(3))
            i += 1
            continue
        m = re.match(r"^(\s*)[-*+]\s+(.*)", line)
        if m:
            style = "List Bullet 2" if len(m.group(1)) >= 2 else "List Bullet"
            add_inline(doc.add_paragraph(style=style), m.group(2))
            i += 1
            continue
        m = re.match(r"^(\s*)\d+[.)]\s+(.*)", line)
        if m:
            style = "List Number 2" if len(m.group(1)) >= 2 else "List Number"
            add_inline(doc.add_paragraph(style=style), m.group(2))
            i += 1
            continue
        if line.strip():
            text = re.sub(r"^>\s?", "", line.strip())
            add_inline(doc.add_paragraph(), text)
        i += 1
    doc.save(out_path)
    print(f"저장 완료: {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    convert(sys.argv[1], sys.argv[2])
