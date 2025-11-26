import argparse
import re
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, ListFlowable, ListItem
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
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

# Global variable for the document title to be used in the page frame
DOC_TITLE = "FILIPINO STUDY GUIDE"

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
    bg_padding = 10
    x = doc.leftMargin - bg_padding
    y = doc.bottomMargin - bg_padding
    w = doc.width + bg_padding * 2
    h = height - doc.topMargin - doc.bottomMargin + bg_padding * 2

    canv.setStrokeColor(PALETTE["primary"])
    canv.setLineWidth(2)
    canv.roundRect(x, y, w, h, radius=15, stroke=1, fill=0)

    # 3. Header Bar (Neon Strip)
    header_height = 50
    canv.setFillColor(PALETTE["secondary"])
    canv.setStrokeColor(PALETTE["secondary"])
    canv.rect(0, height - header_height, width, header_height, stroke=0, fill=1)

    # Header Text
    canv.setFont("Impact", 20)
    canv.setFillColor(colors.white)
    # Use the global DOC_TITLE
    canv.drawString(doc.leftMargin, height - 35, DOC_TITLE.upper())

    canv.setFont("Verdana-Bold", 10)
    canv.setFillColor(colors.black)
    canv.drawRightString(width - doc.rightMargin, height - 32, "QUICK STUDY GUIDE")

    # 4. Footer
    footer_y = 20
    canv.setFont("Verdana", 8)
    canv.setFillColor(PALETTE["text_muted"])
    canv.drawString(doc.leftMargin, footer_y, "NEO-PUNK EDITION · v2.0")

    page_label = f"PAGE {doc.page}"
    canv.drawRightString(width - doc.rightMargin, footer_y, page_label)

    canv.restoreState()

def make_badge(text, bg_color=None, text_color=colors.black):
    """
    Returns a pill/badge.
    """
    if bg_color is None:
        bg_color = PALETTE["tertiary"]

    badge_style = ParagraphStyle(
        name="BadgeText",
        parent=getSampleStyleSheet()["Normal"],
        fontName="Verdana-Bold",
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
        ("BOX", (0, 0), (-1, -1), 0, colors.white),
    ]))
    return tbl

def make_card(width, title=None, title_style=None, body_flowables=None, background=None, border_color=None):
    """
    Generic Card container.
    """
    if background is None:
        background = PALETTE["bg_card"]
    if border_color is None:
        border_color = PALETTE["primary"]

    rows = []

    # Title row
    if title:
        if isinstance(title, str):
            if title_style is None:
                # Default title style if not provided
                title_style = ParagraphStyle(
                    name="CardTitle",
                    parent=getSampleStyleSheet()["Heading2"],
                    fontName="Impact",
                    fontSize=16,
                    leading=18,
                    textColor=PALETTE["primary"],
                    textTransform='uppercase',
                )
            title_para = Paragraph(title.upper(), title_style)
        else:
            title_para = title
        rows.append([title_para])

    # Body flowables
    if body_flowables:
        for item in body_flowables:
            rows.append([item])

    if not rows:
        return Spacer(1, 1)

    card = Table(rows, colWidths=[width])
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 1.5, border_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))

    return card

# ---- Markdown Parsing ----

def parse_markdown_text(text):
    """
    Converts basic markdown formatting to ReportLab XML tags.
    **bold** -> <b>bold</b>
    *italic* -> <i>italic</i>
    <br> -> <br/>
    """
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Line breaks
    text = text.replace('<br>', '<br/>')
    return text

def parse_markdown_file(file_path, styles):
    """
    Parses a markdown file and returns a list of ReportLab Flowables.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    flowables = []
    
    # Styles
    h1_style = styles['HeroTitle']
    h2_style = styles['SectionHeading']
    h3_style = styles['SubHeading']
    body_style = styles['NeoBodyText']
    bullet_style = styles['NeoBulletText']
    quote_style = styles['NeoQuoteText']
    
    # Table parsing state
    in_table = False
    table_header = []
    table_rows = []
    table_alignments = []

    for line in lines:
        line = line.strip()
        
        # Skip empty lines unless we are in a table (end of table)
        if not line:
            if in_table:
                # Render the table
                flowables.append(create_table(table_header, table_rows, styles))
                in_table = False
                table_header = []
                table_rows = []
            continue

        # --- Table Handling ---
        if line.startswith('|'):
            if not in_table:
                in_table = True
                # Check if it's a separator line (e.g. |---|---|)
                if '---' in line:
                    continue # Skip separator for now
                
                # Assume first row is header if we just started
                # But wait, markdown tables usually have header, then separator, then body.
                # We need to buffer.
                
            # Process row
            # Remove leading/trailing pipes and split
            content = line.strip('|').split('|')
            row_data = [parse_markdown_text(c.strip()) for c in content]
            
            if '---' in line:
                # This is the separator line, ignore it but maybe parse alignment later
                continue
            
            if not table_header:
                table_header = row_data
            else:
                table_rows.append(row_data)
            continue
        
        # If we were in a table and hit a non-table line
        if in_table:
            flowables.append(create_table(table_header, table_rows, styles))
            in_table = False
            table_header = []
            table_rows = []

        # --- Headers ---
        if line.startswith('# '):
            text = parse_markdown_text(line[2:])
            # Update global title if it's the first H1? 
            # For now just add as H1
            flowables.append(Paragraph(text.upper(), h1_style))
            flowables.append(Spacer(1, SPACING['lg']))
        elif line.startswith('## '):
            text = parse_markdown_text(line[3:])
            flowables.append(Paragraph(text.upper(), h2_style))
        elif line.startswith('### '):
            text = parse_markdown_text(line[4:])
            flowables.append(Paragraph(text, h3_style))
        
        # --- Lists ---
        elif line.startswith('* ') or line.startswith('- '):
            text = parse_markdown_text(line[2:])
            # Create a list item
            # For simplicity, using a Paragraph with a bullet char for now, 
            # or we could use ListFlowable if we grouped them.
            # Let's use a Paragraph with bullet style.
            p = Paragraph(f"• {text}", bullet_style)
            flowables.append(p)
            
        # --- Blockquotes ---
        elif line.startswith('> '):
            text = parse_markdown_text(line[2:])
            p = Paragraph(text, quote_style)
            flowables.append(p)
            
        # --- Normal Paragraph ---
        else:
            text = parse_markdown_text(line)
            flowables.append(Paragraph(text, body_style))

    # End of file, check if table pending
    if in_table:
        flowables.append(create_table(table_header, table_rows, styles))

    return flowables

def create_table(header, rows, styles):
    """
    Creates a styled ReportLab Table from parsed data.
    """
    if not header and not rows:
        return Spacer(1, 1)

    data = []
    
    # Header
    if header:
        data.append([Paragraph(h, styles['NeoTableHeader']) for h in header])
    
    # Rows
    for row in rows:
        data.append([Paragraph(c, styles['NeoTableBody']) for c in row])

    # Calculate col widths dynamically or fixed?
    # Let's try to be smart or just even.
    # A4 width is ~595 pts. Margins 30+30=60. Content ~535.
    # If 3 cols, ~178 each.
    num_cols = len(header) if header else len(rows[0])
    col_width = 530 / num_cols if num_cols > 0 else 530
    
    t = Table(data, colWidths=[col_width] * num_cols)
    
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALETTE["table_header_bg"]),
        ("LINEBELOW", (0, 0), (-1, 0), 1, PALETTE["primary"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), PALETTE["primary"]),
        
        # Zebra striping for rows
        *[("BACKGROUND", (0, i), (-1, i), PALETTE["table_row_odd"]) for i in range(1, len(data), 2)],
        *[("BACKGROUND", (0, i), (-1, i), PALETTE["table_row_even"]) for i in range(2, len(data), 2)],
        
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 1, PALETTE["text_muted"]),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    
    return t

def create_styles():
    """
    Defines the ReportLab styles.
    """
    styles = getSampleStyleSheet()
    
    # Hero Title
    styles.add(ParagraphStyle(
        name="HeroTitle",
        parent=styles["Title"],
        fontName="Impact",
        fontSize=36,
        leading=40,
        textColor=PALETTE["primary"],
        alignment=TA_CENTER,
        spaceAfter=SPACING["lg"],
    ))

    # Section Heading (H2)
    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontName="Impact",
        fontSize=20,
        leading=24,
        textColor=PALETTE["secondary"],
        spaceBefore=SPACING["lg"],
        spaceAfter=SPACING["sm"],
        textTransform='uppercase',
    ))

    # Sub Heading (H3)
    styles.add(ParagraphStyle(
        name="SubHeading",
        parent=styles["Heading3"],
        fontName="Verdana-Bold",
        fontSize=14,
        leading=16,
        textColor=PALETTE["tertiary"],
        spaceBefore=SPACING["md"],
        spaceAfter=SPACING["xs"],
    ))

    # Body Text
    styles.add(ParagraphStyle(
        name="NeoBodyText",
        parent=styles["Normal"],
        fontName="Verdana",
        fontSize=10,
        leading=14,
        textColor=PALETTE["text_main"],
        spaceAfter=SPACING["sm"],
        alignment=TA_JUSTIFY,
    ))

    # Bullet Text
    styles.add(ParagraphStyle(
        name="NeoBulletText",
        parent=styles["Normal"],
        fontName="Verdana",
        fontSize=10,
        leading=14,
        textColor=PALETTE["text_main"],
        leftIndent=20,
        spaceAfter=SPACING["xs"],
    ))

    # Quote Text
    styles.add(ParagraphStyle(
        name="NeoQuoteText",
        parent=styles["Normal"],
        fontName="Verdana", # Italic not available in base Verdana, using normal for now or simulated
        fontSize=10,
        leading=14,
        textColor=PALETTE["text_muted"],
        leftIndent=30,
        rightIndent=30,
        spaceAfter=SPACING["sm"],
    ))

    # Table Styles
    styles.add(ParagraphStyle(
        name="NeoTableHeader",
        parent=styles["Normal"],
        fontName="Verdana-Bold",
        fontSize=10,
        textColor=PALETTE["primary"],
        alignment=TA_LEFT,
    ))

    styles.add(ParagraphStyle(
        name="NeoTableBody",
        parent=styles["Normal"],
        fontName="Verdana",
        fontSize=10,
        textColor=PALETTE["text_main"],
        leading=12,
    ))

    return styles

def create_pdf(input_file, output_file):
    # --- Register Fonts ---
    try:
        pdfmetrics.registerFont(TTFont('Impact', '/System/Library/Fonts/Supplemental/Impact.ttf'))
        pdfmetrics.registerFont(TTFont('Verdana', '/System/Library/Fonts/Supplemental/Verdana.ttf'))
        pdfmetrics.registerFont(TTFont('Verdana-Bold', '/System/Library/Fonts/Supplemental/Verdana Bold.ttf'))
    except:
        print("Warning: System fonts not found. Falling back to defaults.")
        # In a real scenario, we'd handle this better.

    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        leftMargin=30,
        rightMargin=30,
        topMargin=70,
        bottomMargin=50,
    )
    
    styles = create_styles()
    
    # Parse Markdown
    print(f"Parsing {input_file}...")
    content_flowables = parse_markdown_file(input_file, styles)
    
    # Build Story
    story = []
    
    # Wrap content in a "Card" if we want, or just flow it.
    # Given the dynamic nature, flowing it is safer for page breaks.
    # But to keep the "Neo-Punk" look, maybe we can wrap sections?
    # For now, let's just flow the content directly but use the styles to maintain the look.
    
    story.extend(content_flowables)

    # Build PDF
    print(f"Generating PDF: {output_file}...")
    doc.build(
        story,
        onFirstPage=draw_page_frame,
        onLaterPages=draw_page_frame,
    )
    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Neo-Punk PDF from Markdown.")
    parser.add_argument("input_file", help="Path to input Markdown file")
    parser.add_argument("output_file", help="Path to output PDF file")
    
    args = parser.parse_args()
    
    # Update global title based on filename
    base_name = args.input_file.split("/")[-1].replace(".md", "").replace("_", " ")
    # Remove leading numbers if present (e.g. "01 ")
    base_name = re.sub(r'^\d+\s*', '', base_name)
    DOC_TITLE = base_name
    
    create_pdf(args.input_file, args.output_file)
