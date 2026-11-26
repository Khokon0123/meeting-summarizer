from io import BytesIO

from docx import Document
from fpdf import FPDF


def _latin(text):
    # The built-in PDF fonts only support Latin-1, so swap common symbols
    # and replace anything else that cannot be drawn.
    swaps = {
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-", "\u2026": "...", "\u2022": "-",
    }
    for old, new in swaps.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")


def make_txt(title, summary, action_items, attendees):
    lines = [title, "", "SUMMARY", summary, "", "ACTION ITEMS"]
    lines += [f"- {item}" for item in action_items] or ["None detected"]
    lines += ["", "ATTENDEES"]
    lines += [f"- {name}" for name in attendees] or ["None detected"]
    return "\n".join(lines)


def make_pdf(title, summary, action_items, attendees):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    def heading(text, size):
        pdf.set_font("Helvetica", "B", size)
        pdf.multi_cell(0, 9, _latin(text), new_x="LMARGIN", new_y="NEXT")

    def body(text):
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, _latin(text), new_x="LMARGIN", new_y="NEXT")

    heading(title, 18)
    pdf.ln(3)

    heading("Summary", 13)
    body(summary)
    pdf.ln(3)

    heading("Action Items", 13)
    if action_items:
        for item in action_items:
            body(f"- {item}")
    else:
        body("None detected")
    pdf.ln(3)

    heading("Attendees", 13)
    if attendees:
        for name in attendees:
            body(f"- {name}")
    else:
        body("None detected")

    return bytes(pdf.output())


def make_docx(title, summary, action_items, attendees):
    doc = Document()
    doc.add_heading(title, 0)

    doc.add_heading("Summary", 1)
    doc.add_paragraph(summary)

    doc.add_heading("Action Items", 1)
    if action_items:
        for item in action_items:
            doc.add_paragraph(item, style="List Bullet")
    else:
        doc.add_paragraph("None detected")

    doc.add_heading("Attendees", 1)
    if attendees:
        for name in attendees:
            doc.add_paragraph(name, style="List Bullet")
    else:
        doc.add_paragraph("None detected")

    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()
