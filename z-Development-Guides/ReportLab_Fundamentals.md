# ReportLab Fundamentals: A Developer's Guide

This guide will teach you the basics of the **ReportLab** library in Python, which is used to generate professional PDF documents programmatically. We will walk through the core concepts and build a simplified version of the study guide script.

## What is ReportLab?

ReportLab is a powerful Python library for creating PDFs. Unlike tools that convert HTML to PDF, ReportLab allows you to build documents element by element, giving you precise control over layout, styling, and content.

There are two main ways to use ReportLab:
1.  **Canvas (Low-level):** You draw lines, shapes, and text at specific X, Y coordinates. Good for charts or complex graphics.
2.  **PLATYPUS (High-level):** Stands for "Page Layout and Typography Using Scripts". This handles page breaking, text wrapping, and layout for you. **We will focus on this.**

## Core Concepts

### 1. The Document Template (`SimpleDocTemplate`)
Think of this as the empty file you are creating. You define the page size (e.g., A4, Letter) and margins here.

### 2. The "Story"
In Platypus, you create a list of elements called "Flowables" (paragraphs, tables, images, spacers). You append them to a list (often called `story`), and ReportLab "builds" the PDF by placing them one after another, creating new pages as needed.

### 3. Styles (`ParagraphStyle`)
Just like CSS for HTML. You define fonts, sizes, colors, and alignment. ReportLab comes with a `getSampleStyleSheet()` to get you started.

---

## Mini-Project: Create a "Mini Study Sheet"

Let's build a script that creates a one-page PDF with a Title, a short intro, and a small table of vocabulary.

### Step 1: Setup and Imports

Create a file named `mini_pdf_guide.py` and add these imports:

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
```

### Step 2: Define the Document and Styles

We need a function to generate the PDF. First, we set up the document and customized styles.

```python
def create_mini_guide(filename):
    # 1. Create the Document Template
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    # 2. Get standard styles
    styles = getSampleStyleSheet()
    
    # 3. Create Custom Styles
    # It's best to create unique names to avoid conflicts
    
    # Title Style: Centered, Big, Bold
    title_style = ParagraphStyle(
        name='MyTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    # Normal Text Style
    body_style = ParagraphStyle(
        name='MyBody',
        parent=styles['Normal'],
        fontSize=12,
        leading=14, # Line height
        spaceAfter=12
    )
    
    # Table Header Style
    table_header_style = ParagraphStyle(
        name='MyTableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    # Initialize the story list
    story = []
    
    # ... (Content will go here)
```

### Step 3: Add Content (The Story)

Now we add the actual text and table to our `story` list.

```python
    # ... (inside create_mini_guide function)

    # Add Title
    story.append(Paragraph("Mini Filipino Guide", title_style))
    
    # Add Intro Text
    intro = "Welcome to this mini guide. Here are three essential words you should know."
    story.append(Paragraph(intro, body_style))
    story.append(Spacer(1, 12)) # Add vertical space (12 points)

    # Prepare Table Data
    # Row 1 is the header, Rows 2-4 are data
    data = [
        [Paragraph("Filipino", table_header_style), Paragraph("English", table_header_style)],
        ["Salamat", "Thank you"],
        ["Magandang Umaga", "Good Morning"],
        ["Paalam", "Goodbye"]
    ]

    # Create Table
    # colWidths defines how wide each column is
    t = Table(data, colWidths=[200, 200])

    # Style the Table
    t.setStyle(TableStyle([
        # (Column, Row) coordinates. (0,0) is top-left. (-1, -1) is bottom-right.
        
        # Header Row Background (Blue)
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        
        # Grid lines
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        
        # Padding
        ('PADDING', (0, 0), (-1, -1), 6),
        
        # Align text in data rows to left
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
    ]))

    story.append(t)
    
    # Build the PDF
    doc.build(story)
    print(f"PDF created: {filename}")

if __name__ == "__main__":
    create_mini_guide("mini_guide.pdf")
```

## Key Takeaways

1.  **Paragraphs wrap text**: Always use `Paragraph("Your text", style)` instead of raw strings for text content. It handles wrapping automatically.
2.  **Tables are powerful**: You can put `Paragraphs` *inside* table cells (like we did for the headers) to style them individually.
3.  **Coordinates**: In `TableStyle`, coordinates are `(col, row)`.
    *   `0, 0` = First column, First row.
    *   `-1, -1` = Last column, Last row.
    *   `(-1, 0)` = Last column, First row (entire header row).

## Practice Challenge

Try to modify the script to:
1.  Add a **Subtitle** below the main title.
2.  Add a **third column** to the table for "Pronunciation" (e.g., "Sa-la-mat").
3.  Change the table header color to **Dark Red**.
