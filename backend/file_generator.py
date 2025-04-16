from fpdf import FPDF
import os

def save_transcript_pdf(filename: str) -> str:
    txt_path = os.path.join("downloads", f"{filename}.txt")
    pdf_path = os.path.join("downloads", f"{filename}.pdf")

    with open(txt_path, "r", encoding="utf8") as f:
        text = f.read()

    pdf = FPDF()
    pdf.add_page()

    # Use Arabic-compatible TTF font
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=14)

    # Handle Arabic line-by-line
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, txt=line)

    pdf.output(pdf_path)
    return pdf_path
save_transcript_pdf("lec5_large")