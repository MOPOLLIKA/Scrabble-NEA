from fpdf import FPDF 

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt=title, ln=True, align="C")
pdf.output("/Users/MOPOLLIKA/Docs")