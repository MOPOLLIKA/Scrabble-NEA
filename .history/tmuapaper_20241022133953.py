from fpdf import FPDF

# Function to create a TMUA mock paper
def create_tmua_paper(title, instructions, questions, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=True, align="C")
    pdf.ln(10)

    # Instructions
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, instructions)
    pdf.ln(5)

    # Add all questions to the PDF
    for question in questions:
        pdf.multi_cell(0, 10, question)
        pdf.ln(5)

    # Save the PDF to the specified file name
    pdf.output(file_name)

# Title and instructions for Paper 1
title_paper_1 = "TMUA Mock Paper 1 (2024)"
instructions_paper_1 = """Instructions:
- There are 20 multiple-choice questions in this paper.
- For each question, choose the one answer you consider correct.
- Calculators and formula sheets are not allowed.
- Marks will not be deducted for incorrect answers, so it is to your advantage to attempt every question.
"""

# Questions for Paper 1
questions_paper_1 = [
    "Question 1: If f(x) = x^2 + 4x + 3, which of the following is true about the minimum value of f(x)?\n"
    "A. f(0) = 3  B. f(-2) = -1  C. f(-1) = 0  D. The minimum value does not exist  E. f(2) = 1",

    "Question 2: Evaluate the following integral: S (x^2 - 4x + 3) dx from 0 to 2.\n"
    "A. -2/3  B. -2  C. -1  D. 0  E. 1",

    "Question 3: Solve for x in the equation log_2(x+1) + log_2(x-1) = 3.\n"
    "A. 1  B. 3  C. 7  D. 5  E. 8",

    "Question 4: Find the area enclosed between the curve y = sin(x) and the x-axis from x = 0 to x = pi.\n"
    "A. 2  B. 1  C. pi/2  D. 1.5  E. 4",

    "Question 5: If the sequence u_n is defined by u_n = 3u_(n-1) + 2 for n ≥ 2 and u_1 = 1, what is u_3?\n"
    "A. 13  B. 11  C. 9  D. 7  E. 5",

    "Question 6: Solve the following inequality: (2x + 3) / (x - 1) ≥ 4.\n"
    "A. x ≤ -5/2 or x ≥ 2  B. x ≤ 5/2 or x ≥ 2  C. x ≥ 1  D. x ≤ -1  E. x < 1",

    "Question 7: Find the value of k such that the function f(x) = kx^3 - 6x + 2 has a point of inflection at x = 1.\n"
    "A. k = 3  B. k = 2  C. k = 1  D. k = 0  E. k = -1",

    "Question 8: Given that tan(θ) = 3/4, find sin(2θ).\n"
    "A. 24/25  B. 7/25  C. 12/25  D. 15/25  E. 9/25",

    "Question 9: Which of the following best represents the equation of a circle that passes through the points (0, 0), (1, 0), and (0, 1)?\n"
    "A. x^2 + y^2 - x - y = 0  B. x^2 + y^2 + x + y = 0  C. x^2 + y^2 - 2x = 0  D. x^2 + y^2 - 1 = 0  E. x^2 + y^2 + 2xy = 0",

    "Question 10: Find the inverse function of f(x) = (2x - 1) / (x + 3).\n"
    "A. f^(-1)(x) = (x + 1) / (3 - 2x)  B. f^(-1)(x) = (x + 3) / (2x - 1)  C. f^(-1)(x) = (3x - 1) / (x + 2)  D. f^(-1)(x) = (x + 3) / (2x + 1)  E. f^(-1)(x) = (3x - 1) / (2x + 1)",

    "Question 11: The equation x^2 + 4x - 5 = 0 has two solutions x_1 and x_2. What is the value of x_1 + x_2?\n"
    "A. -4  B. 1  C. 5  D. -1  E. 4",

    "Question 12: A geometric progression has first term a = 4 and common ratio r = 1/2. What is the sum to infinity of this series?\n"
    "A. 2  B. 4  C. 8  D. 16  E. 10",

    "Question 13: Find the determinant of the matrix:\n"
    "    | 3  2 |\n"
    "    | 5  4 |\n"
    "A. -2  B. -4  C. 2  D. 4  E. 1",

    "Question 14: If f(x) = ln(x), then what is d/dx [f(f(x))]?\n"
    "A. 1 / (x ln(x))  B. ln(x) / x  C. 1 / x^2  D. 1 / (x ln(x)^2)  E. 1 / ln(x)",

    "Question 15: Which of the following functions has no real roots?\n"
    "A. f(x) = x^2 - 4x + 5  B. f(x) = x^2 - 5x + 6  C. f(x) = x^2 - 3x - 4  D. f(x) = x^2 + 4x - 5  E. f(x) = x^2 - x - 2",

    "Question 16: Given the function f(x) = (2x^3 - 3x^2 + x) / (x - 1), what is the limit of f(x) as x approaches 1?\n"
    "A. -1  B. 0  C. 1  D. ∞  E. Does not exist",

    "Question 17: Find the number of distinct solutions to the equation sin(x) + sin(2x) = 0 in the interval [0, 2π].\n"
    "A. 2  B. 3  C. 4  D. 5  E. 6",

    "Question 18: The curve y = x^2 is rotated about the x-axis. What is the volume of the solid formed between x = 0 and x = 2?\n"
    "A. 8π/3  B. 16π/3  C. 8π  D. 4π/3  E. 4π",

    "Question 19: Given that z = 2 + 3i is a complex number, find the modulus of z^2.\n"
    "A. 5  B. 13  C. 25  D. 34  E. 15",

    "Question 20: If the series S = 1 + 1/2 + 1/4 + 1/8 + ... continues infinitely, find the sum of the series.\n"
    "A. 1  B. 2  C. 3  D. 4  E. 5",
]

# Create the PDF for Paper 1
create_tmua_paper(title_paper_1, instructions_paper_1, questions_paper_1, "/Users/MOPOLLIKA/Docs/tmuamock1.pdf")
