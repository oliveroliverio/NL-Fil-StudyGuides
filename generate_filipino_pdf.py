from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as pdf_canvas

# ---- Design System ----
PALETTE = {
    "bg_page": colors.whitesmoke,
    "bg_light": colors.HexColor("#F3F4F6"),
    "primary": colors.HexColor("#2563EB"),  # Blue-600
    "primary_dark": colors.HexColor("#1D4ED8"),
    "accent": colors.HexColor("#F97316"),   # Orange-500
    "text_main": colors.HexColor("#111827"),
    "text_muted": colors.HexColor("#6B7280"),
    "border_subtle": colors.HexColor("#E5E7EB"),
    "table_header_bg": colors.HexColor("#111827"),
    "table_row_alt": colors.HexColor("#F9FAFB"),
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
    Draws a tinted content background, header bar, and footer on every page.
    """
    canv.saveState()

    width, height = doc.pagesize

    # Content background area
    bg_padding = 6
    x = doc.leftMargin - bg_padding
    y = doc.bottomMargin - bg_padding
    w = doc.width + bg_padding * 2
    h = height - doc.topMargin - doc.bottomMargin + bg_padding * 2

    canv.setFillColor(PALETTE["bg_light"])
    canv.setStrokeColor(PALETTE["border_subtle"])
    canv.setLineWidth(0.5)
    canv.roundRect(x, y, w, h, radius=10, stroke=1, fill=1)

    # Header bar
    header_height = 40
    canv.setFillColor(PALETTE["primary"])
    canv.setStrokeColor(PALETTE["primary"])
    canv.rect(0, height - header_height, width, header_height, stroke=0, fill=1)

    # Header text
    canv.setFont("Helvetica-Bold", 12)
    canv.setFillColor(colors.white)
    canv.drawString(50, height - 25, "Filipino Question Words Study Guide")

    canv.setFont("Helvetica", 9)
    canv.setFillColor(colors.whitesmoke)
    canv.drawRightString(width - 50, height - 25, "Essential WH-Questions")

    # Footer
    footer_y = 30
    canv.setFont("Helvetica", 9)
    canv.setFillColor(PALETTE["text_muted"])
    canv.drawString(50, footer_y, "Generated with Python & ReportLab")

    page_label = f"Page {doc.page}"
    canv.drawRightString(width - 50, footer_y, page_label)

    canv.restoreState()

def make_badge(text, bg_color=None, text_color=colors.white):
    """
    Returns a Flowable that looks like a pill/badge.
    """
    if bg_color is None:
        bg_color = PALETTE["accent"]

    badge_style = ParagraphStyle(
        name="BadgeText",
        parent=getSampleStyleSheet()["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=text_color,
        alignment=TA_LEFT,
    )

    badge_para = Paragraph(text, badge_style)

    tbl = Table([[badge_para]])

    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("TEXTCOLOR", (0, 0), (-1, -1), text_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
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
):
    """
    Generic card component.
    """
    if background is None:
        background = colors.white

    rows = []

    # Badge row
    if badge_text:
        badge = make_badge(badge_text, bg_color=badge_color or PALETTE["accent"])
        badge_row = Table([[badge]], colWidths=[width])
        badge_row.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
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
                    fontName="Helvetica-Bold",
                    fontSize=13,
                    leading=16,
                    textColor=PALETTE["primary"],
                )
            title_para = Paragraph(title, title_style)
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
                    fontName="Helvetica",
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
        ("BOX", (0, 0), (-1, -1), 1, PALETTE["border_subtle"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))

    return card

def create_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=80,
        bottomMargin=70,
    )
    
    styles = getSampleStyleSheet()
    
    # --- Styles ---
    title_style = ParagraphStyle(
        name="HeroTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=30,
        textColor=PALETTE["primary_dark"],
        alignment=TA_CENTER,
        spaceAfter=SPACING["sm"],
    )

    subtitle_style = ParagraphStyle(
        name="HeroSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=15,
        textColor=PALETTE["text_muted"],
        alignment=TA_CENTER,
        spaceAfter=SPACING["xl"],
    )

    section_heading_style = ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=PALETTE["primary"],
        spaceBefore=SPACING["lg"],
        spaceAfter=SPACING["sm"],
    )

    body_style = ParagraphStyle(
        name="BodyText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        textColor=PALETTE["text_main"],
        spaceAfter=SPACING["sm"],
    )

    table_header_style = ParagraphStyle(
        name="TableHeader",
        parent=body_style,
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=colors.white,
        alignment=TA_CENTER,
    )

    table_body_style = ParagraphStyle(
        name="TableBody",
        parent=body_style,
        fontSize=11,
        leading=14,
    )

    story = []

    # --- Hero Section ---
    story.append(Paragraph("Filipino Question Words", title_style))
    story.append(Paragraph("Essential WH-Questions with Examples and English Translations", subtitle_style))

    # Badges
    difficulty_badge = make_badge("Beginner · A1", bg_color=PALETTE["primary"])
    topic_badge = make_badge("Grammar", bg_color=PALETTE["accent"])
    language_badge = make_badge("Tagalog / Filipino", bg_color=PALETTE["table_header_bg"])

    badges_row = Table(
        [[difficulty_badge, topic_badge, language_badge]],
        colWidths=[100, 80, 130],
        hAlign="CENTER",
    )
    badges_row.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(badges_row)
    story.append(Spacer(1, SPACING["xl"]))

    # --- Introduction Card ---
    intro_text = """
    <b>Mabuhay!</b> Welcome to your essential guide to <b>Filipino Question Words</b> (mga panghalip pananong).
    Asking questions is one of the most important skills in learning a new language.
    """
    
    intro_card = make_card(
        width=480,
        title="Introduction",
        title_style=section_heading_style,
        body_paragraphs=[intro_text],
    )
    story.append(intro_card)
    story.append(Spacer(1, SPACING["lg"]))

    # --- Master Table Card ---
    master_data = [
        [Paragraph("Filipino", table_header_style), Paragraph("English", table_header_style), Paragraph("Notes", table_header_style)],
        ["Ano", "What", "Things, events, abstract concepts"],
        ["Sino", "Who", "People"],
        ["Saan", "Where", "Places, locations"],
        ["Kailan", "When", "Time, dates"],
        ["Bakit", "Why", "Reasons"],
        ["Paano", "How", "Procedures, manner"],
        ["Magkano", "How much", "Prices"],
        ["Ilan", "How many", "Quantity"],
        ["Alin", "Which", "Choices"],
        ["Kanino", "Whose", "Possession"],
        ["Kumusta", "How is/are", "Condition"],
    ]
    
    # Convert string rows to Paragraphs
    formatted_master_data = [master_data[0]]
    for row in master_data[1:]:
        formatted_master_data.append([Paragraph(cell, table_body_style) for cell in row])

    t_master = Table(formatted_master_data, colWidths=[100, 100, 250], hAlign="LEFT")
    t_master.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALETTE["table_header_bg"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        # Zebra striping
        *[("BACKGROUND", (0, i), (-1, i), PALETTE["table_row_alt"]) for i in range(2, len(master_data), 2)],
        ("BOX", (0, 0), (-1, -1), 0.5, PALETTE["border_subtle"]),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, PALETTE["border_subtle"]),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    master_card = make_card(
        width=480,
        title="Master Table",
        title_style=section_heading_style,
        badge_text="Reference",
        inner_flowables=[t_master]
    )
    story.append(master_card)
    story.append(PageBreak())

    # --- Examples Section ---
    story.append(Paragraph("Detailed Examples", section_heading_style))
    story.append(Spacer(1, SPACING["md"]))

    examples = [
        {
            "word": "Ano (What)",
            "desc": "Used to ask about things, names, or information.",
            "data": [
                ["Ano ang pangalan mo?", "What is your name?"],
                ["Ano ito?", "What is this?"]
            ]
        },
        {
            "word": "Sino (Who)",
            "desc": "Used to ask about people.",
            "data": [
                ["Sino siya?", "Who is he?"],
                ["Sino ang kasama mo?", "Who is with you?"]
            ]
        },
        {
            "word": "Saan (Where)",
            "desc": "Used to ask about locations.",
            "data": [
                ["Saan ka nakatira?", "Where do you live?"],
                ["Saan tayo kakain?", "Where shall we eat?"]
            ]
        },
         {
            "word": "Kailan (When)",
            "desc": "Used to ask about time.",
            "data": [
                ["Kailan ang birthday mo?", "When is your birthday?"],
                ["Kailan ka uuwi?", "When are you going home?"]
            ]
        },
    ]

    # Create a card for each example
    for item in examples:
        # Mini table for Q&A
        qa_data = [[Paragraph("Question / Answer", table_header_style), Paragraph("English", table_header_style)]]
        for q, e in item["data"]:
            qa_data.append([Paragraph(q, table_body_style), Paragraph(e, table_body_style)])
        
        t_qa = Table(qa_data, colWidths=[220, 220], hAlign="LEFT")
        t_qa.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PALETTE["table_header_bg"]),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("BOX", (0, 0), (-1, -1), 0.5, PALETTE["border_subtle"]),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, PALETTE["border_subtle"]),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))

        card = make_card(
            width=480,
            title=item["word"],
            title_style=ParagraphStyle(name="ExTitle", parent=section_heading_style, fontSize=12),
            body_paragraphs=[item["desc"]],
            inner_flowables=[Spacer(1, 6), t_qa],
            background=colors.white
        )
        story.append(card)
        story.append(Spacer(1, SPACING["md"]))

    story.append(PageBreak())

    # --- Practice Section ---
    practice_intro = "Fill in the blank with the correct Filipino question word."
    
    practice_items = [
        "1. __________ ang pangalan ng aso mo? (What)",
        "2. __________ ka nakatira? (Where)",
        "3. __________ ang kasama mong kumain? (Who)",
        "4. __________ ang kilo ng mangga? (How much)",
        "5. __________ ka aalis? (When)",
    ]
    
    practice_paras = [Paragraph(p, body_style) for p in practice_items]
    
    practice_card = make_card(
        width=480,
        title="Quick Practice",
        title_style=section_heading_style,
        badge_text="Quiz",
        badge_color=PALETTE["accent"],
        body_paragraphs=[practice_intro] + practice_paras
    )
    story.append(practice_card)
    story.append(Spacer(1, SPACING["lg"]))

    # --- Answer Key ---
    answers = "1. Ano, 2. Saan, 3. Sino, 4. Magkano, 5. Kailan"
    answer_card = make_card(
        width=480,
        title="Answer Key",
        title_style=section_heading_style,
        body_paragraphs=[answers],
        background=PALETTE["bg_light"]
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
