from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def create_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    styles.add(ParagraphStyle(name='TitleStyle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=24, spaceAfter=12, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='SubtitleStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=14, spaceAfter=24, alignment=TA_CENTER, textColor=colors.darkgray))
    styles.add(ParagraphStyle(name='Heading1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, spaceBefore=20, spaceAfter=12, color=colors.darkblue))
    styles.add(ParagraphStyle(name='Heading2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, spaceBefore=15, spaceAfter=10, color=colors.black))
    styles.add(ParagraphStyle(name='BodyText', parent=styles['Normal'], fontName='Helvetica', fontSize=11, spaceBefore=6, spaceAfter=6, leading=14))
    styles.add(ParagraphStyle(name='TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, alignment=TA_CENTER, textColor=colors.white))
    styles.add(ParagraphStyle(name='TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=10, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='QuestionText', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, spaceAfter=4))
    styles.add(ParagraphStyle(name='AnswerText', parent=styles['Normal'], fontName='Helvetica', fontSize=11, spaceAfter=8, leftIndent=20))

    story = []

    # --- Title Page ---
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Filipino Question Words – Study Guide", styles['TitleStyle']))
    story.append(Paragraph("Essential WH-Questions with Examples and English Translations", styles['SubtitleStyle']))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Prepared by: ____________________", styles['BodyText']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("This guide covers the most common Filipino question words, their meanings, and how to use them in everyday conversation. Perfect for beginner to low-intermediate learners.", styles['BodyText']))
    story.append(PageBreak())

    # --- Introduction ---
    story.append(Paragraph("Introduction", styles['Heading1']))
    intro_text = """
    <b>Mabuhay!</b> Welcome to your essential guide to <b>Filipino Question Words</b> (mga panghalip pananong).<br/><br/>
    Asking questions is one of the most important skills in learning a new language. Whether you are asking for directions, getting to know a new friend, or buying food at the market, knowing the right question word is key to clear communication.<br/><br/>
    In this guide, you will learn the most common Filipino question words, how to use them, and see them in natural, everyday sentences. We have included polite markers like "po" and "opo" in some examples, as using them is standard when speaking to elders, strangers, or people in authority.
    """
    story.append(Paragraph(intro_text, styles['BodyText']))
    story.append(Spacer(1, 12))

    # --- Master Table ---
    story.append(Paragraph("Master Table of Question Words", styles['Heading1']))
    
    master_data = [
        ["Filipino", "English Meaning", "Notes"],
        ["Ano", "What", "Used for things, events, or abstract concepts."],
        ["Sino", "Who", "Used for people."],
        ["Saan", "Where", "Used for places (locations, directions)."],
        ["Kailan", "When", "Used for time (dates, days, future/past events)."],
        ["Bakit", "Why", "Used for reasons or explanations."],
        ["Paano", "How", "Used for procedures, manner, or ways."],
        ["Magkano", "How much", "Used for asking prices."],
        ["Ilan", "How many", "Used for counting quantity."],
        ["Alin", "Which", "Used when choosing between options."],
        ["Kanino", "Whose / To whom", "Used for possession or direction."],
        ["Kumusta", "How is/are...", "Used to ask about condition/well-being."]
    ]

    t = Table(master_data, colWidths=[1.5*inch, 1.5*inch, 3*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(PageBreak())

    # --- Examples Section ---
    story.append(Paragraph("Example Questions & Answers", styles['Heading1']))

    examples = [
        {
            "word": "1. Ano (What)",
            "desc": "Used to ask about things, names, or information.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Ano ang pangalan mo?", "Maria ang pangalan ko.", "What is your name?", "My name is Maria."],
                ["Ano ang gusto mong kainin?", "Gusto ko ng adobo.", "What do you want to eat?", "I want adobo."],
                ["Ano ito?", "Regalo 'yan para sa iyo.", "What is this?", "That is a gift for you."]
            ]
        },
        {
            "word": "2. Sino (Who)",
            "desc": "Used to ask about people.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Sino ang kasama mo?", "Kasama ko ang kapatid ko.", "Who is with you?", "I am with my sibling."],
                ["Sino siya?", "Siya si Mr. Cruz, ang titser namin.", "Who is he?", "He is Mr. Cruz, our teacher."],
                ["Sino ang nagluto nito?", "Si Nanay ang nagluto.", "Who cooked this?", "Mom cooked this."]
            ]
        },
        {
            "word": "3. Saan (Where)",
            "desc": "Used to ask about locations.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Saan ka nakatira?", "Nakatira ako sa Manila.", "Where do you live?", "I live in Manila."],
                ["Saan tayo kakain?", "Sa Jollibee tayo kumain.", "Where shall we eat?", "Let's eat at Jollibee."],
                ["Saan ang banyo?", "Nasa kanan, malapit sa pinto.", "Where is the bathroom?", "It's on the right, near the door."]
            ]
        },
        {
            "word": "4. Kailan (When)",
            "desc": "Used to ask about time or dates.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Kailan ang birthday mo?", "Sa Oktubre ang birthday ko.", "When is your birthday?", "My birthday is in October."],
                ["Kailan ka uuwi?", "Uuwi ako bukas.", "When are you going home?", "I am going home tomorrow."],
                ["Kailan ang alis nila?", "Sa Linggo ang alis nila.", "When is their departure?", "Their departure is on Sunday."]
            ]
        },
        {
            "word": "5. Bakit (Why)",
            "desc": "Used to ask for reasons.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Bakit ka masaya?", "Kasi nakapasa ako sa exam.", "Why are you happy?", "Because I passed the exam."],
                ["Bakit wala si Ana?", "May sakit siya.", "Why is Ana not here?", "She is sick."],
                ["Bakit mahal ito?", "Kasi imported ang materyales.", "Why is this expensive?", "Because the materials are imported."]
            ]
        },
        {
            "word": "6. Paano (How)",
            "desc": "Used to ask about manner or procedure.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Paano pumunta sa airport?", "Sumakay ka ng taxi o bus.", "How do you go to the airport?", "Take a taxi or a bus."],
                ["Paano lutuin ang sinigang?", "Pakuluan muna ang karne.", "How do you cook sinigang?", "Boil the meat first."],
                ["Paano mo nalaman?", "Sinabi sa akin ni Pedro.", "How did you know?", "Pedro told me."]
            ]
        },
        {
            "word": "7. Magkano (How much)",
            "desc": "Used to ask about prices.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Magkano ito?", "Limampung piso lang po.", "How much is this?", "Just fifty pesos, sir/ma'am."],
                ["Magkano ang pamasahe?", "Dalawampung piso ang bayad.", "How much is the fare?", "The payment is twenty pesos."],
                ["Magkano ang sapatos na iyan?", "Mahal, isang libo.", "How much are those shoes?", "Expensive, one thousand."]
            ]
        },
        {
            "word": "8. Ilan (How many)",
            "desc": "Used to ask about quantity.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Ilan ang kapatid mo?", "Dalawa ang kapatid ko.", "How many siblings do you have?", "I have two siblings."],
                ["Ilan ang bibilhin mo?", "Tatlo lang.", "How many will you buy?", "Just three."],
                ["Ilan taon ka na?", "Dalawampu't isa na ako.", "How old are you?", "I am twenty-one."]
            ]
        },
        {
            "word": "9. Alin (Which)",
            "desc": "Used to ask to choose between options.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Alin ang mas gusto mo, kape o tsaa?", "Mas gusto ko ang kape.", "Which do you prefer, coffee or tea?", "I prefer coffee."],
                ["Alin dito ang sa iyo?", "Ang asul na bag ang akin.", "Which of these is yours?", "The blue bag is mine."],
                ["Alin ang mas mura?", "Ito ang mas mura.", "Which is cheaper?", "This one is cheaper."]
            ]
        },
        {
            "word": "10. Kanino (Whose / To whom)",
            "desc": "Used to ask about ownership or direction.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Kanino ang lapis na ito?", "Kay Juan 'yan.", "Whose pencil is this?", "That is Juan's."],
                ["Kanino ka sasama?", "Sasama ako kay Ate.", "With whom will you go?", "I will go with Big Sister."],
                ["Kanino mo ibibigay ito?", "Ibibigay ko ito sa titser.", "To whom will you give this?", "I will give this to the teacher."]
            ]
        },
        {
            "word": "11. Kumusta (How is/are)",
            "desc": "Used as a greeting or to ask about condition.",
            "data": [
                ["Filipino Question", "Filipino Answer", "English Question", "English Answer"],
                ["Kumusta ka?", "Mabuti naman, salamat.", "How are you?", "I'm fine, thank you."],
                ["Kumusta ang trabaho?", "Okay lang, medyo busy.", "How is work?", "It's okay, a bit busy."],
                ["Kumusta ang pamilya mo?", "Nasa probinsya sila ngayon.", "How is your family?", "They are in the province now."]
            ]
        }
    ]

    for item in examples:
        story.append(Paragraph(item["word"], styles['Heading2']))
        story.append(Paragraph(f"<i>{item['desc']}</i>", styles['BodyText']))
        story.append(Spacer(1, 6))
        
        # Format data for table
        # We need to wrap text in Paragraphs to allow wrapping in cells
        table_data = []
        # Header
        table_data.append([Paragraph(h, styles['TableHeader']) for h in item["data"][0]])
        # Rows
        for row in item["data"][1:]:
            table_data.append([Paragraph(cell, styles['TableCell']) for cell in row])
            
        t = Table(table_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))
        
    story.append(PageBreak())

    # --- Practice Section ---
    story.append(Paragraph("Quick Practice", styles['Heading1']))
    story.append(Paragraph("<b>Instructions:</b> Fill in the blank with the correct Filipino question word (<i>Ano, Sino, Saan, Kailan, Bakit, Paano, Magkano, Ilan, Alin, Kanino</i>).", styles['BodyText']))
    story.append(Spacer(1, 10))

    practice_items = [
        "1. __________ ang pangalan ng aso mo? (What is the name of your dog?)",
        "2. __________ ka nakatira? (Where do you live?)",
        "3. __________ ang kasama mong kumain? (Who is your companion eating?)",
        "4. __________ ang kilo ng mangga? (How much is a kilo of mangoes?)",
        "5. __________ ka aalis papuntang Japan? (When are you leaving for Japan?)",
        "6. __________ mo ginawa ang cake na ito? (How did you make this cake?)",
        "7. __________ ka umiiyak? (Why are you crying?)",
        "8. __________ ang mga anak mo? (How many are your children?)",
        "9. __________ ang payong na ito? (Whose umbrella is this?)",
        "10. __________ ang mas masarap, adobo o sinigang? (Which is more delicious, adobo or sinigang?)"
    ]

    for item in practice_items:
        story.append(Paragraph(item, styles['BodyText']))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 20))
    story.append(Paragraph("Answer Key", styles['Heading2']))
    
    answers = [
        "1. Ano", "2. Saan", "3. Sino", "4. Magkano", "5. Kailan",
        "6. Paano", "7. Bakit", "8. Ilan", "9. Kanino", "10. Alin"
    ]
    
    # Display answers in a simple list or grid
    answer_text = ", ".join(answers)
    story.append(Paragraph(answer_text, styles['BodyText']))
    
    story.append(PageBreak())

    # --- Summary Cheat Sheet ---
    story.append(Paragraph("Summary Cheat Sheet", styles['Heading1']))
    
    summary_data = [
        ["Question Word", "English", "Example"],
        ["Ano", "What", "Ano ito? (What is this?)"],
        ["Sino", "Who", "Sino siya? (Who is he/she?)"],
        ["Saan", "Where", "Saan ka pupunta? (Where are you going?)"],
        ["Kailan", "When", "Kailan ang party? (When is the party?)"],
        ["Bakit", "Why", "Bakit ka tumatawa? (Why are you laughing?)"],
        ["Paano", "How", "Paano ito gamitin? (How do use this?)"],
        ["Magkano", "How much", "Magkano ito? (How much is this?)"],
        ["Ilan", "How many", "Ilan ang aso mo? (How many dogs do you have?)"],
        ["Alin", "Which", "Alin ang gusto mo? (Which do you want?)"],
        ["Kanino", "Whose", "Kanino ito? (Whose is this?)"],
        ["Kumusta", "How is/are", "Kumusta ka? (How are you?)"]
    ]

    t_summary = Table(summary_data, colWidths=[1.5*inch, 1.5*inch, 3*inch])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_summary)

    # Build PDF
    doc.build(story)
    print(f"PDF generated successfully: {filename}")

if __name__ == "__main__":
    create_pdf("filipino_question_words_study_guide.pdf")
