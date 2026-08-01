"""Generate three print-size Q.bizcard Founder business-card concepts.

Final PDFs use a 96 x 56 mm media box with 3 mm bleed on every side and a
90 x 50 mm trim box. Each concept contains front and back pages.
"""

from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, FloatObject
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.colors import CMYKColor, HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "output" / "pdf"
PREVIEW_DIR = ROOT / "output" / "pdf" / "previews"
TEMP_DIR = ROOT / "tmp" / "pdfs" / "qbizcard_founder"

OUTFIT_FONT = Path("C:/tmp/qbizcard-fonts/Outfit-VF.ttf")
NOTO_REGULAR = Path("C:/Windows/Fonts/NotoSansKR-Regular.ttf")
NOTO_MEDIUM = Path("C:/Windows/Fonts/NotoSansKR-Medium.ttf")
NOTO_BOLD = Path("C:/Windows/Fonts/NotoSansKR-Bold.ttf")

PERSON = {
    "name_ko": "서대원",
    "name_en": "SEO DAEWON",
    "role_ko": "큐닷 파운더",
    "role_en": "Q. FOUNDER",
    "qid": "SDW00000007",
    "phone": "010 5029 2000",
    "email": "50292000@Q.co.kr",
    "site": "Q.co.kr",
    "profile_url": "https://010.q.co.kr/p?id=SDW00000007",
}

MEDIA_W = 96 * mm
MEDIA_H = 56 * mm
TRIM_X = 3 * mm
TRIM_Y = 3 * mm
TRIM_W = 90 * mm
TRIM_H = 50 * mm

BLACK = CMYKColor(0.70, 0.62, 0.55, 0.92)
BLACK_SOFT = CMYKColor(0.66, 0.58, 0.50, 0.86)
GOLD = CMYKColor(0.12, 0.26, 0.74, 0.12)
GOLD_LIGHT = CMYKColor(0.06, 0.16, 0.54, 0.04)
ORANGE = CMYKColor(0.00, 0.78, 1.00, 0.00)
BLUE = CMYKColor(0.78, 0.48, 0.00, 0.00)
IVORY = CMYKColor(0.02, 0.04, 0.11, 0.00)
IVORY_DEEP = CMYKColor(0.04, 0.07, 0.16, 0.01)
WHITE = CMYKColor(0.00, 0.00, 0.00, 0.00)
GRAY = CMYKColor(0.00, 0.00, 0.00, 0.52)
GRAY_LIGHT = CMYKColor(0.00, 0.00, 0.00, 0.22)


def register_fonts():
    required = [OUTFIT_FONT, NOTO_REGULAR, NOTO_MEDIUM, NOTO_BOLD]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Required fonts missing: {missing}")

    pdfmetrics.registerFont(TTFont("Outfit", str(OUTFIT_FONT)))
    pdfmetrics.registerFont(TTFont("NotoKR", str(NOTO_REGULAR)))
    pdfmetrics.registerFont(TTFont("NotoKR-Medium", str(NOTO_MEDIUM)))
    pdfmetrics.registerFont(TTFont("NotoKR-Bold", str(NOTO_BOLD)))


def fill_page(c, color):
    c.saveState()
    c.setFillColor(color)
    c.rect(0, 0, MEDIA_W, MEDIA_H, fill=1, stroke=0)
    c.restoreState()


def text(c, x, y, value, font="NotoKR", size=8, color=BLACK,
         align="left", char_space=0, render_mode=0, stroke_color=None,
         line_width=0.15 * mm):
    c.saveState()
    c.setFillColor(color)
    if stroke_color is not None:
        c.setStrokeColor(stroke_color)
    c.setLineWidth(line_width)
    t = c.beginText()
    t.setTextOrigin(x, y)
    t.setFont(font, size)
    t.setCharSpace(char_space)
    t.setTextRenderMode(render_mode)
    width = pdfmetrics.stringWidth(value, font, size)
    if align == "center":
        t.setTextOrigin(x - width / 2, y)
    elif align == "right":
        t.setTextOrigin(x - width, y)
    t.textOut(value)
    c.drawText(t)
    c.restoreState()


def multiline(c, x, y, lines, font="NotoKR", size=8, leading=None,
              color=BLACK, align="left"):
    if leading is None:
        leading = size * 1.35
    for index, line in enumerate(lines):
        text(c, x, y - index * leading, line, font=font, size=size,
             color=color, align=align)


def line(c, x1, y1, x2, y2, color=BLACK, width=0.25 * mm):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)
    c.restoreState()


def q_mark(c, x, y, size=14, main_color=GOLD, dot_color=ORANGE):
    text(c, x, y, "Q", font="Outfit", size=size, color=main_color,
         render_mode=2, stroke_color=main_color, line_width=0.18 * mm)
    q_width = pdfmetrics.stringWidth("Q", "Outfit", size)
    dot_radius = max(0.65 * mm, size * 0.047 * mm)
    c.saveState()
    c.setFillColor(dot_color)
    c.circle(x + q_width + dot_radius * 0.85, y + size * 0.12,
             dot_radius, fill=1, stroke=0)
    c.restoreState()


def draw_qr(c, x, y, outer=18 * mm, dark=BLACK, frame=None):
    c.saveState()
    c.setFillColor(WHITE)
    c.roundRect(x, y, outer, outer, 1.2 * mm, fill=1, stroke=0)
    if frame is not None:
        c.setStrokeColor(frame)
        c.setLineWidth(0.35 * mm)
        c.roundRect(x, y, outer, outer, 1.2 * mm, fill=0, stroke=1)

    quiet = 1.6 * mm
    qr_size = outer - quiet * 2
    qr = QrCodeWidget(PERSON["profile_url"])
    qr.barFillColor = dark
    qr.barStrokeColor = dark
    bounds = qr.getBounds()
    qr_w = bounds[2] - bounds[0]
    qr_h = bounds[3] - bounds[1]
    drawing = Drawing(
        qr_size,
        qr_size,
        transform=[qr_size / qr_w, 0, 0, qr_size / qr_h, 0, 0],
    )
    drawing.add(qr)
    renderPDF.draw(drawing, c, x + quiet, y + quiet)
    c.restoreState()


def crop_marks(c):
    """Tiny non-printing-area trim reference marks for proof output."""
    c.saveState()
    c.setStrokeColor(CMYKColor(0, 0, 0, 1))
    c.setLineWidth(0.1 * mm)
    gap = 0.7 * mm
    length = 1.3 * mm
    for x in (TRIM_X, TRIM_X + TRIM_W):
        c.line(x, gap, x, gap + length)
        c.line(x, MEDIA_H - gap, x, MEDIA_H - gap - length)
    for y in (TRIM_Y, TRIM_Y + TRIM_H):
        c.line(gap, y, gap + length, y)
        c.line(MEDIA_W - gap, y, MEDIA_W - gap - length, y)
    c.restoreState()


def origin_front(c):
    fill_page(c, BLACK)
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.25 * mm)
    c.roundRect(TRIM_X + 2.2 * mm, TRIM_Y + 2.2 * mm,
                TRIM_W - 4.4 * mm, TRIM_H - 4.4 * mm,
                2.4 * mm, fill=0, stroke=1)
    c.restoreState()

    q_mark(c, TRIM_X + 6 * mm, TRIM_Y + 35.5 * mm, 17)
    text(c, TRIM_X + TRIM_W - 6 * mm, TRIM_Y + 40.4 * mm,
         "ORIGIN 1996", font="Outfit", size=6.2, color=GOLD_LIGHT,
         align="right", char_space=1.0)
    text(c, TRIM_X + 6 * mm, TRIM_Y + 23 * mm, PERSON["name_ko"],
         font="NotoKR-Bold", size=15, color=WHITE, char_space=2.5)
    text(c, TRIM_X + 6.2 * mm, TRIM_Y + 18.4 * mm, PERSON["name_en"],
         font="Outfit", size=6.8, color=GOLD_LIGHT, char_space=1.2)
    text(c, TRIM_X + 6.2 * mm, TRIM_Y + 9.8 * mm, PERSON["role_en"],
         font="Outfit", size=7.2, color=GOLD, char_space=1.1)
    text(c, TRIM_X + 6.2 * mm, TRIM_Y + 6.8 * mm,
         "A NEW PROFESSION BEGINS", font="Outfit", size=4.7,
         color=GRAY_LIGHT, char_space=0.7)
    crop_marks(c)


def origin_back(c):
    fill_page(c, BLACK_SOFT)
    c.saveState()
    c.setFillColor(GOLD)
    c.rect(0, 0, 2.3 * mm, MEDIA_H, fill=1, stroke=0)
    c.restoreState()
    q_mark(c, TRIM_X + 6 * mm, TRIM_Y + 37 * mm, 10)
    text(c, TRIM_X + 6 * mm, TRIM_Y + 28 * mm, PERSON["email"],
         font="Outfit", size=8.4, color=WHITE)
    text(c, TRIM_X + 6 * mm, TRIM_Y + 22.7 * mm, PERSON["phone"],
         font="Outfit", size=6.5, color=GOLD_LIGHT, char_space=0.4)
    text(c, TRIM_X + 6 * mm, TRIM_Y + 16.4 * mm,
         f"Q-ID  {PERSON['qid']}", font="Outfit", size=6.1,
         color=GOLD, char_space=0.45)
    text(c, TRIM_X + 6 * mm, TRIM_Y + 10.8 * mm, PERSON["site"],
         font="Outfit", size=6.2, color=WHITE)
    text(c, TRIM_X + 6 * mm, TRIM_Y + 6.8 * mm, "신원은 하나 - Q-ID",
         font="NotoKR-Medium", size=5.3, color=GRAY_LIGHT)
    draw_qr(c, TRIM_X + TRIM_W - 24 * mm, TRIM_Y + 16 * mm,
            18 * mm, dark=BLACK, frame=GOLD)
    text(c, TRIM_X + TRIM_W - 15 * mm, TRIM_Y + 11.5 * mm,
         "SCAN MY Q-ID", font="Outfit", size=4.7, color=GOLD_LIGHT,
         align="center", char_space=0.7)
    crop_marks(c)


def declaration_front(c):
    fill_page(c, IVORY)
    c.saveState()
    c.setFillColor(ORANGE)
    c.rect(0, 0, 8.2 * mm, MEDIA_H, fill=1, stroke=0)
    c.setFillColor(BLACK)
    c.circle(TRIM_X + TRIM_W - 8 * mm, TRIM_Y + 39 * mm,
             2.2 * mm, fill=1, stroke=0)
    c.restoreState()

    text(c, TRIM_X + 9 * mm, TRIM_Y + 41 * mm,
         "OCCUPATION 01", font="Outfit", size=5.7, color=ORANGE,
         char_space=1.0)
    text(c, TRIM_X + 9 * mm, TRIM_Y + 29.5 * mm, PERSON["role_ko"],
         font="NotoKR-Bold", size=15.2, color=BLACK, char_space=0.8)
    text(c, TRIM_X + 9 * mm, TRIM_Y + 23.8 * mm,
         "Q. FOUNDER", font="Outfit", size=7.4, color=BLACK,
         char_space=1.4)
    line(c, TRIM_X + 9 * mm, TRIM_Y + 18.5 * mm,
         TRIM_X + 48 * mm, TRIM_Y + 18.5 * mm,
         color=ORANGE, width=0.45 * mm)
    text(c, TRIM_X + 9 * mm, TRIM_Y + 11.5 * mm, PERSON["name_ko"],
         font="NotoKR-Bold", size=10.5, color=BLACK, char_space=1.2)
    text(c, TRIM_X + 34 * mm, TRIM_Y + 12.1 * mm, PERSON["name_en"],
         font="Outfit", size=5.8, color=GRAY, char_space=0.8)
    text(c, TRIM_X + 9 * mm, TRIM_Y + 6.8 * mm,
         "새로운 직업의 첫 명함", font="NotoKR-Medium", size=5.3,
         color=GRAY)
    crop_marks(c)


def declaration_back(c):
    fill_page(c, IVORY_DEEP)
    q_mark(c, TRIM_X + 7 * mm, TRIM_Y + 38.5 * mm, 10,
           main_color=BLACK, dot_color=ORANGE)
    multiline(
        c,
        TRIM_X + 7 * mm,
        TRIM_Y + 29.8 * mm,
        ["나는 큐닷 파운더를", "하나의 새로운 직업으로", "정의한다."],
        font="NotoKR-Bold",
        size=7.4,
        leading=10.2,
        color=BLACK,
    )
    text(c, TRIM_X + 7 * mm, TRIM_Y + 7.2 * mm,
         f"{PERSON['name_ko']}  /  {PERSON['qid']}",
         font="NotoKR-Medium", size=5.3, color=GRAY)

    draw_qr(c, TRIM_X + TRIM_W - 25 * mm, TRIM_Y + 24 * mm,
            18 * mm, dark=BLACK, frame=ORANGE)
    text(c, TRIM_X + TRIM_W - 25 * mm, TRIM_Y + 17.7 * mm,
         PERSON["email"], font="Outfit", size=6.3, color=BLACK)
    text(c, TRIM_X + TRIM_W - 25 * mm, TRIM_Y + 13.3 * mm,
         PERSON["phone"], font="Outfit", size=5.6, color=GRAY,
         char_space=0.3)
    text(c, TRIM_X + TRIM_W - 25 * mm, TRIM_Y + 8.9 * mm,
         PERSON["site"], font="Outfit", size=5.8, color=BLACK)
    crop_marks(c)


def identity_front(c):
    fill_page(c, WHITE)
    c.saveState()
    c.setFillColor(ORANGE)
    c.rect(MEDIA_W - 11.5 * mm, 0, 11.5 * mm, MEDIA_H, fill=1, stroke=0)
    c.setFillColor(CMYKColor(0, 0, 0, 0.045))
    c.rotate(90)
    c.setFont("Outfit", 41)
    c.drawString(11 * mm, -33 * mm, "SDW")
    c.restoreState()

    q_mark(c, TRIM_X + 7 * mm, TRIM_Y + 37.8 * mm, 12,
           main_color=BLACK, dot_color=ORANGE)
    text(c, TRIM_X + 7 * mm, TRIM_Y + 25.5 * mm, PERSON["name_ko"],
         font="NotoKR-Bold", size=13.5, color=BLACK, char_space=1.5)
    text(c, TRIM_X + 7.2 * mm, TRIM_Y + 20.9 * mm, PERSON["name_en"],
         font="Outfit", size=6.7, color=GRAY, char_space=1.1)
    text(c, TRIM_X + 7.2 * mm, TRIM_Y + 14.4 * mm, PERSON["role_en"],
         font="Outfit", size=7.1, color=ORANGE, char_space=1.0)
    text(c, TRIM_X + 7.2 * mm, TRIM_Y + 8.9 * mm,
         f"Q-ID  {PERSON['qid']}", font="Outfit", size=5.8,
         color=BLACK, char_space=0.45)
    text(c, TRIM_X + 7.2 * mm, TRIM_Y + 5.4 * mm, PERSON["email"],
         font="Outfit", size=5.6, color=GRAY)
    crop_marks(c)


def identity_back(c):
    fill_page(c, WHITE)
    c.saveState()
    c.setFillColor(ORANGE)
    c.rect(0, 0, 34 * mm, MEDIA_H, fill=1, stroke=0)
    c.restoreState()

    q_mark(c, TRIM_X + 7 * mm, TRIM_Y + 34.5 * mm, 18,
           main_color=WHITE, dot_color=BLACK)
    text(c, TRIM_X + 7 * mm, TRIM_Y + 24.4 * mm, "YOUR IDENTITY.",
         font="Outfit", size=7, color=WHITE, char_space=1.0)
    text(c, TRIM_X + 7 * mm, TRIM_Y + 20 * mm, "YOUR Q-ID.",
         font="Outfit", size=7, color=WHITE, char_space=1.0)
    text(c, TRIM_X + 7 * mm, TRIM_Y + 9.5 * mm, PERSON["site"],
         font="Outfit", size=6.2, color=BLACK)

    draw_qr(c, TRIM_X + 42 * mm, TRIM_Y + 21.5 * mm,
            20 * mm, dark=BLACK, frame=ORANGE)
    text(c, TRIM_X + 42 * mm, TRIM_Y + 15.4 * mm,
         PERSON["qid"], font="Outfit", size=6.8, color=BLACK,
         char_space=0.7)
    text(c, TRIM_X + 42 * mm, TRIM_Y + 10.4 * mm,
         PERSON["email"], font="Outfit", size=5.8, color=GRAY)
    text(c, TRIM_X + 42 * mm, TRIM_Y + 6.7 * mm,
         PERSON["phone"], font="Outfit", size=5.4, color=GRAY,
         char_space=0.25)
    crop_marks(c)


CONCEPTS = {
    "01_ORIGIN": {
        "front": origin_front,
        "back": origin_back,
        "title": "01 ORIGIN - 시작의 권위",
        "paper": "코팅스노우 300g + 무광코팅 / 선택 금박",
    },
    "02_DECLARATION": {
        "front": declaration_front,
        "back": declaration_back,
        "title": "02 DECLARATION - 새로운 직업의 선언",
        "paper": "아르떼 310g 또는 엑스트라누보 350g / 무코팅",
    },
    "03_IDENTITY": {
        "front": identity_front,
        "back": identity_back,
        "title": "03 IDENTITY - Q-ID 중심 기능형",
        "paper": "반누보 250g 또는 무코팅스노우 300g",
    },
}


def set_pdf_boxes(source, destination):
    reader = PdfReader(str(source))
    writer = PdfWriter()
    trim = ArrayObject([
        FloatObject(TRIM_X),
        FloatObject(TRIM_Y),
        FloatObject(TRIM_X + TRIM_W),
        FloatObject(TRIM_Y + TRIM_H),
    ])
    bleed = ArrayObject([
        FloatObject(0),
        FloatObject(0),
        FloatObject(MEDIA_W),
        FloatObject(MEDIA_H),
    ])
    for page in reader.pages:
        page.trimbox = trim
        page.bleedbox = bleed
        page.cropbox = bleed
        page.artbox = trim
        writer.add_page(page)
    with open(destination, "wb") as stream:
        writer.write(stream)


def generate_concept_pdf(code, spec):
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    raw = TEMP_DIR / f"{code}_raw.pdf"
    final = OUTPUT_DIR / f"Qbizcard_Founder_서대원_{code}_인쇄용.pdf"
    c = canvas.Canvas(str(raw), pagesize=(MEDIA_W, MEDIA_H), pageCompression=1)
    c.setTitle(f"Q.bizcard Founder - {PERSON['name_ko']} - {code}")
    c.setAuthor("Q.")
    spec["front"](c)
    c.showPage()
    spec["back"](c)
    c.showPage()
    c.save()
    set_pdf_boxes(raw, final)
    return final


def draw_preview_card(c, draw_fn, x, y, scale):
    c.saveState()
    c.translate(x, y)
    c.scale(scale, scale)
    draw_fn(c)
    c.restoreState()


def generate_preview_sheet():
    """A4 portrait sheet showing front and back at 88% of trim size."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "Qbizcard_Founder_서대원_3종_비교시안_A4.pdf"
    page_w, page_h = A4
    c = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
    c.setTitle("Q.bizcard Founder - 서대원 - 3종 비교시안")
    c.setAuthor("Q.")

    c.setFillColor(HexColor("#F2F0EB"))
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    q_mark(c, 12 * mm, page_h - 18 * mm, 17,
           main_color=HexColor("#111111"), dot_color=HexColor("#FF5A1F"))
    text(c, 29 * mm, page_h - 14.5 * mm, "Q.bizcard FOUNDER",
         font="Outfit", size=15, color=HexColor("#111111"), char_space=1.2)
    text(c, 29 * mm, page_h - 20 * mm,
         "서대원 파운더 명함 - 기본 디자인 3종",
         font="NotoKR-Medium", size=7.5, color=HexColor("#555555"))
    text(c, page_w - 12 * mm, page_h - 14.5 * mm, "2026.07.30",
         font="Outfit", size=6, color=HexColor("#777777"), align="right")

    scale = 0.94
    card_w = MEDIA_W * scale
    card_h = MEDIA_H * scale
    x_front = 9 * mm
    x_back = page_w - 9 * mm - card_w
    row_tops = [page_h - 38 * mm, page_h - 119 * mm, page_h - 200 * mm]

    for index, (_, spec) in enumerate(CONCEPTS.items()):
        top = row_tops[index]
        text(c, 10 * mm, top + 3 * mm, spec["title"],
             font="NotoKR-Bold", size=8, color=HexColor("#111111"))
        text(c, page_w - 10 * mm, top + 3 * mm, spec["paper"],
             font="NotoKR", size=5.5, color=HexColor("#666666"),
             align="right")

        y = top - card_h
        c.saveState()
        c.setFillColor(HexColor("#D7D4CD"))
        c.roundRect(x_front + 1.2 * mm, y - 1.2 * mm, card_w, card_h,
                    2 * mm, fill=1, stroke=0)
        c.roundRect(x_back + 1.2 * mm, y - 1.2 * mm, card_w, card_h,
                    2 * mm, fill=1, stroke=0)
        c.restoreState()
        draw_preview_card(c, spec["front"], x_front, y, scale)
        draw_preview_card(c, spec["back"], x_back, y, scale)
        text(c, x_front, y - 4 * mm, "FRONT", font="Outfit", size=4.8,
             color=HexColor("#777777"), char_space=0.8)
        text(c, x_back, y - 4 * mm, "BACK", font="Outfit", size=4.8,
             color=HexColor("#777777"), char_space=0.8)

    text(c, 10 * mm, 10 * mm,
         "추천 첫 주문: 02 DECLARATION / 아르떼 310g / 무코팅 / 100매",
         font="NotoKR-Bold", size=7.2, color=HexColor("#111111"))
    text(c, page_w - 10 * mm, 10 * mm,
         "실제 주문 전 인쇄사 템플릿으로 최종 도련 재확인",
         font="NotoKR", size=5.5, color=HexColor("#666666"), align="right")
    c.showPage()
    c.save()
    return path


def generate_combined_pdf(concept_paths):
    destination = OUTPUT_DIR / "Qbizcard_Founder_서대원_3종_인쇄용_합본.pdf"
    writer = PdfWriter()
    for path in concept_paths:
        reader = PdfReader(str(path))
        for page in reader.pages:
            writer.add_page(page)
    writer.add_metadata({
        "/Title": "Q.bizcard Founder - 서대원 - 3종 인쇄용 합본",
        "/Author": "Q.",
    })
    with open(destination, "wb") as stream:
        writer.write(stream)
    return destination


def validate_pdf(path, expected_pages):
    reader = PdfReader(str(path))
    if len(reader.pages) != expected_pages:
        raise ValueError(f"{path.name}: expected {expected_pages} pages")
    for index, page in enumerate(reader.pages, start=1):
        media = [float(v) for v in page.mediabox]
        if abs(media[2] - MEDIA_W) > 0.5 or abs(media[3] - MEDIA_H) > 0.5:
            if path.name.endswith("_A4.pdf"):
                continue
            raise ValueError(f"{path.name} page {index}: media box mismatch")
        if not path.name.endswith("_A4.pdf"):
            trim = [float(v) for v in page.trimbox]
            expected = [TRIM_X, TRIM_Y, TRIM_X + TRIM_W, TRIM_Y + TRIM_H]
            if any(abs(a - b) > 0.5 for a, b in zip(trim, expected)):
                raise ValueError(f"{path.name} page {index}: trim box mismatch")


def main():
    register_fonts()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    concept_paths = [
        generate_concept_pdf(code, spec) for code, spec in CONCEPTS.items()
    ]
    combined = generate_combined_pdf(concept_paths)
    preview = generate_preview_sheet()

    for path in concept_paths:
        validate_pdf(path, 2)
    validate_pdf(combined, 6)
    if len(PdfReader(str(preview)).pages) != 1:
        raise ValueError("Preview PDF must contain one A4 page")

    print("Generated:")
    for path in [*concept_paths, combined, preview]:
        print(path)


if __name__ == "__main__":
    main()

