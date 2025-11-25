from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---- Neo-Punk Design System ----
PALETTE = {
    "bg_page": colors.HexColor("#121212"),      # Deep Charcoal / Black
    "bg_card": colors.HexColor("#1E1E2E"),      # Dark Blue-Grey
    "primary": colors.HexColor("#00F0FF"),      # Neon Cyan
    "secondary": colors.HexColor("#FF0099"),    # Hot Pink
    "tertiary": colors.HexColor("#39FF14"),     # Electric Lime
    "text_main": colors.HexColor("#FFFFFF"),    # White
    "text_muted": colors.HexColor("#A0A0A0"),   # Light Grey
    "border_focus": colors.HexColor("#00F0FF"), # Cyan Border
    "table_header_bg": colors.HexColor("#2A2A35"), # Slightly lighter dark
    "table_row_even": colors.HexColor("#1E1E2E"),
    "table_row_odd": colors.HexColor("#252530"),
}

SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 20,
    "xl": 32,
}

# ---- Helper Functions ----

def draw_page_frame(canv, doc):
    """
    Draws a Neo-Punk page frame: Dark background, Neon header strip.
    """
    canv.saveState()

    width, height = doc.pagesize

    # 1. Full Page Background (Dark)
    canv.setFillColor(PALETTE["bg_page"])
    canv.rect(0, 0, width, height, stroke=0, fill=1)

    # 2. Content Area Background (Card-like container)
    # We'll make this a large rounded rect to frame the content
    bg_padding = 10
    x = doc.leftMargin - bg_padding
    y = doc.bottomMargin - bg_padding
    w = doc.width + bg_padding * 2
    h = height - doc.topMargin - doc.bottomMargin + bg_padding * 2

    canv.setFillColor(PALETTE["bg_page"]) # Keep it same as page or slightly lighter? Let's keep it clean dark.
    # Actually, let's make the "Page" look like a high-tech slate.
    # We will draw a neon border around the content area.
    canv.setStrokeColor(PALETTE["primary"])
    canv.setLineWidth(2)
    canv.roundRect(x, y, w, h, radius=15, stroke=1, fill=0)

    # 3. Header Bar (Neon Strip)
    header_height = 50
    # Gradient-like effect or solid neon? Let's go solid Pink for contrast with Cyan border
    canv.setFillColor(PALETTE["secondary"])
    canv.setStrokeColor(PALETTE["secondary"])
    # Draw a top bar that goes edge-to-edge
    canv.rect(0, height - header_height, width, header_height, stroke=0, fill=1)

    # Header Text
    canv.setFont("Impact", 20) # Updated Font
    canv.setFillColor(colors.white)
    canv.drawString(doc.leftMargin, height - 35, "FILIPINO QUESTION WORDS")

    canv.setFont("Verdana-Bold", 10) # Updated Font
    canv.setFillColor(colors.black) # Black text on Pink background for punk vibe
    canv.drawRightString(width - doc.rightMargin, height - 32, "QUICK STUDY GUIDE")

    # 4. Footer
    footer_y = 20
    canv.setFont("Verdana", 8) # Updated Font
    canv.setFillColor(PALETTE["text_muted"])
    canv.drawString(doc.leftMargin, footer_y, "NEO-PUNK EDITION · v2.0")

    page_label = f"PAGE {doc.page}"
    canv.drawRightString(width - doc.rightMargin, footer_y, page_label)

    canv.restoreState()

def make_badge(text, bg_color=None, text_color=colors.black):
    """
    Returns a pill/badge. Default text color black for high contrast on neon.
    """
    if bg_color is None:
        bg_color = PALETTE["tertiary"] # Lime default

    badge_style = ParagraphStyle(
        name="BadgeText",
        parent=getSampleStyleSheet()["Normal"],
        fontName="Verdana-Bold", # Updated Font
        fontSize=8,
        leading=10,
        textColor=text_color,
        alignment=TA_CENTER,
    )

    badge_para = Paragraph(text.upper(), badge_style)

    tbl = Table([[badge_para]])

    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("TEXTCOLOR", (0, 0), (-1, -1), text_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        # We can't do real rounded corners on table cells easily, 
        # but we can simulate a "blocky" tag look which fits punk.
        ("BOX", (0, 0), (-1, -1), 0, colors.white), 
    ]))

    return tbl

def make_card(
    width,
    title=None,
    title_style=None,
    badge_text=None,
    badge_color=None,
    body_paragraphs=None,
    inner_flowables=None,
    background=None,
    border_color=None
):
    """
    Neo-Punk Card: Dark background, Neon border, Sharp edges (or simulated rounded via frame).
    """
    if background is None:
        background = PALETTE["bg_card"]
    if border_color is None:
        border_color = PALETTE["primary"]

    rows = []

    # Badge row (Floating on top right or left? Let's put it inline with title if possible, or row 0)
    # For this design, let's put badge in the first row, left aligned
    if badge_text:
        badge = make_badge(badge_text, bg_color=badge_color or PALETTE["tertiary"])
        badge_row = Table([[badge]], colWidths=[width])
        badge_row.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ]))
        rows.append([badge_row])

    # Title row
    if title:
        if isinstance(title, str):
            if title_style is None:
                title_style = ParagraphStyle(
                    name="CardTitle",
                    parent=getSampleStyleSheet()["Heading2"],
                    fontName="Impact", # Updated Font
                    fontSize=16,
                    leading=18,
                    textColor=PALETTE["primary"],
                    textTransform='uppercase', # Punk style
                )
            title_para = Paragraph(title.upper(), title_style)
        else:
            title_para = title

        rows.append([title_para])

    # Body paragraphs
    if body_paragraphs:
        for item in body_paragraphs:
            if isinstance(item, str):
                p = Paragraph(item, ParagraphStyle(
                    name="CardBody",
                    parent=getSampleStyleSheet()["Normal"],
                    fontName="Verdana", # Updated Font
                    fontSize=10,
                    leading=13,
                    textColor=PALETTE["text_main"],
                ))
            else:
                p = item
            rows.append([p])

    # Extra flowables
    if inner_flowables:
        for f in inner_flowables:
            rows.append([f])

    card = Table(rows, colWidths=[width])

    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 1.5, border_color), # Thicker neon border
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))

    return card

def create_pdf(filename):
    # --- Register Fonts ---
    pdfmetrics.registerFont(TTFont('Impact', '/System/Library/Fonts/Supplemental/Impact.ttf'))
    pdfmetrics.registerFont(TTFont('Verdana', '/System/Library/Fonts/Supplemental/Verdana.ttf'))
    pdfmetrics.registerFont(TTFont('Verdana-Bold', '/System/Library/Fonts/Supplemental/Verdana Bold.ttf'))

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=30, # Narrower margins for "Chart" feel
        rightMargin=30,
        topMargin=70,
        bottomMargin=50,
    )
    
    styles = getSampleStyleSheet()
    
    # --- Styles ---
    # Hero Title - Big, Neon
    hero_title_style = ParagraphStyle(
        name="HeroTitle",
        parent=styles["Title"],
        fontName="Impact", # Updated Font
        fontSize=42, # Bigger for Impact
        leading=44,
        textColor=PALETTE["primary"],
        alignment=TA_CENTER,
        spaceAfter=SPACING["xs"],
    )

    hero_subtitle_style = ParagraphStyle(
        name="HeroSubtitle",
        parent=styles["Normal"],
        fontName="Verdana-Bold", # Updated Font
        fontSize=12,
        leading=14,
        textColor=PALETTE["text_main"],
        alignment=TA_CENTER,
        spaceAfter=SPACING["lg"],
    )

    section_heading_style = ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontName="Impact", # Updated Font
        fontSize=20,
        leading=22,
        textColor=PALETTE["secondary"], # Pink headings
        spaceBefore=SPACING["md"],
        spaceAfter=SPACING["sm"],
        textTransform='uppercase',
    )

    body_style = ParagraphStyle(
        name="BodyText",
        parent=styles["Normal"],
        fontName="Verdana", # Updated Font
        fontSize=10,
        leading=13,
        textColor=PALETTE["text_main"],
        spaceAfter=SPACING["sm"],
    )

    table_header_style = ParagraphStyle(
        name="TableHeader",
        parent=body_style,
        fontName="Verdana-Bold", # Updated Font
        fontSize=10,
        textColor=PALETTE["primary"], # Neon Cyan text on dark header
        alignment=TA_LEFT,
    )

    table_body_style = ParagraphStyle(
        name="TableBody",
        parent=body_style,
        fontSize=10,
        leading=12,
        textColor=PALETTE["text_main"],
    )

    story = []

    # --- Hero Section ---
    story.append(Paragraph("MGA PANGHALIP PANANONG", hero_title_style))
    story.append(Paragraph("FILIPINO QUESTION WORDS CHEAT SHEET", hero_subtitle_style))

    # Badges Row
    b1 = make_badge("BEGINNER", bg_color=PALETTE["secondary"])
    b2 = make_badge("GRAMMAR", bg_color=PALETTE["tertiary"])
    b3 = make_badge("TAGALOG", bg_color=PALETTE["primary"])

    badges_row = Table(
        [[b1, b2, b3]],
        colWidths=[80, 80, 80],
        hAlign="CENTER",
    )
    badges_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(badges_row)
    story.append(Spacer(1, SPACING["lg"]))

    # --- Introduction (Full Width) ---
    intro_text = """
    <b>MABUHAY!</b> Asking questions is key to connection. Use this chart to master the essential WH-questions in Filipino.
    """
    intro_card = make_card(
        width=530, # Full width roughly
        title="INTRODUCTION",
        title_style=section_heading_style,
        body_paragraphs=[intro_text],
        border_color=PALETTE["text_muted"] # Subtle border for intro
    )
    story.append(intro_card)
    story.append(Spacer(1, SPACING["md"]))

    # --- Master Table (Full Width) ---
    master_data = [
        [Paragraph("FILIPINO", table_header_style), Paragraph("ENGLISH", table_header_style), Paragraph("USAGE", table_header_style)],
        ["Ano", "What", "Things, events, ideas"],
        ["Sino", "Who", "People"],
        ["Saan", "Where", "Places, locations"],
        ["Kailan", "When", "Time, dates"],
        ["Bakit", "Why", "Reasons"],
        ["Paano", "How", "Procedures"],
        ["Magkano", "How much", "Prices"],
        ["Ilan", "How many", "Quantity"],
        ["Alin", "Which", "Choices"],
        ["Kanino", "Whose", "Possession"],
        ["Kumusta", "How is/are", "Condition"],
    ]
    
    formatted_master_data = [master_data[0]]
    for row in master_data[1:]:
        formatted_master_data.append([Paragraph(cell, table_body_style) for cell in row])

    t_master = Table(formatted_master_data, colWidths=[100, 100, 300], hAlign="LEFT")
    t_master.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALETTE["table_header_bg"]),
        ("LINEBELOW", (0, 0), (-1, 0), 1, PALETTE["primary"]), # Neon line under header
        # Zebra striping
        *[("BACKGROUND", (0, i), (-1, i), PALETTE["table_row_odd"]) for i in range(1, len(master_data), 2)],
        *[("BACKGROUND", (0, i), (-1, i), PALETTE["table_row_even"]) for i in range(2, len(master_data), 2)],
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    master_card = make_card(
        width=530,
        title="MASTER REFERENCE",
        title_style=section_heading_style,
        badge_text="CORE",
        badge_color=PALETTE["primary"],
        inner_flowables=[t_master],
        border_color=PALETTE["primary"]
    )
    story.append(master_card)
    story.append(Spacer(1, SPACING["md"]))
    story.append(PageBreak())

    # --- Examples Section (2-Column Grid) ---
    story.append(Paragraph("USAGE EXAMPLES", section_heading_style))
    story.append(Spacer(1, SPACING["sm"]))

    examples = [
        {"word": "ANO (What)", "desc": "Things / Info", "data": [["Ano ito?", "What is this?"], ["Ano ang pangalan mo?", "What is your name?"]]},
        {"word": "SINO (Who)", "desc": "People", "data": [["Sino siya?", "Who is he?"], ["Sino ang kasama mo?", "Who is with you?"]]},
        {"word": "SAAN (Where)", "desc": "Locations", "data": [["Saan ka nakatira?", "Where do you live?"], ["Saan tayo kakain?", "Where shall we eat?"]]},
        {"word": "KAILAN (When)", "desc": "Time", "data": [["Kailan ang birthday mo?", "When is your birthday?"], ["Kailan ka uuwi?", "When are you going home?"]]},
        {"word": "BAKIT (Why)", "desc": "Reasons", "data": [["Bakit ka masaya?", "Why are you happy?"], ["Bakit mahal ito?", "Why is this expensive?"]]},
        {"word": "PAANO (How)", "desc": "Manner", "data": [["Paano ito gamitin?", "How do you use this?"], ["Paano pumunta doon?", "How do you go there?"]]},
        {"word": "MAGKANO (Price)", "desc": "Cost", "data": [["Magkano ito?", "How much is this?"], ["Magkano ang pamasahe?", "How much is the fare?"]]},
        {"word": "ILAN (Count)", "desc": "Quantity", "data": [["Ilan ang kapatid mo?", "How many siblings?"], ["Ilan taon ka na?", "How old are you?"]]},
    ]

    # Process into rows of 2
    card_rows = []
    current_row = []
    
    for i, item in enumerate(examples):
        # Mini table for Q&A
        qa_data = []
        for q, e in item["data"]:
            qa_data.append([Paragraph(q, table_body_style), Paragraph(e, table_body_style)])
        
        t_qa = Table(qa_data, colWidths=[110, 110], hAlign="LEFT")
        t_qa.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -2), 0.5, PALETTE["text_muted"]),
            ("PADDING", (0, 0), (-1, -1), 4),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))

        # Alternate border colors for punk vibe
        border_c = PALETTE["secondary"] if i % 2 == 0 else PALETTE["tertiary"]

        card = make_card(
            width=260, # Half width roughly
            title=item["word"],
            title_style=ParagraphStyle(name="ExTitle", parent=section_heading_style, fontSize=12, textColor=border_c),
            badge_text=item["desc"],
            badge_color=border_c,
            inner_flowables=[t_qa],
            border_color=border_c
        )
        current_row.append(card)

        if len(current_row) == 2:
            card_rows.append(current_row)
            current_row = []
    
    if current_row: # Append leftover
        card_rows.append(current_row)

    # Add rows to story
    for row in card_rows:
        # If single item, pad it
        if len(row) == 1:
            row.append(Spacer(1, 1)) # Placeholder
        
        t_row = Table([row], colWidths=[265, 265], hAlign="CENTER")
        t_row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(t_row)
        story.append(Spacer(1, SPACING["md"]))

    story.append(PageBreak())

    # --- Practice & Answer Key (Stacked) ---
    
    practice_items = [
        "1. __________ ang pangalan ng aso mo? (What)",
        "2. __________ ka nakatira? (Where)",
        "3. __________ ang kasama mong kumain? (Who)",
        "4. __________ ang kilo ng mangga? (How much)",
        "5. __________ ka aalis? (When)",
    ]
    practice_paras = [Paragraph(p, body_style) for p in practice_items]
    
    practice_card = make_card(
        width=530,
        title="QUICK PRACTICE",
        title_style=section_heading_style,
        badge_text="QUIZ",
        badge_color=PALETTE["secondary"],
        body_paragraphs=practice_paras,
        border_color=PALETTE["secondary"]
    )
    story.append(practice_card)
    story.append(Spacer(1, SPACING["md"]))

    answers = "1. ANO, 2. SAAN, 3. SINO, 4. MAGKANO, 5. KAILAN"
    answer_card = make_card(
        width=530,
        title="ANSWER KEY",
        title_style=section_heading_style,
        body_paragraphs=[answers],
        background=PALETTE["table_header_bg"],
        border_color=PALETTE["text_muted"]
    )
    story.append(answer_card)

    # Build PDF
    doc.build(
        story,
        onFirstPage=draw_page_frame,
        onLaterPages=draw_page_frame,
    )
    print(f"PDF generated successfully: {filename}")

if __name__ == "__main__":
    create_pdf("filipino_question_words_study_guide.pdf")
