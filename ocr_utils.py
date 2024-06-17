import pdfplumber




def extract_text_with_layout_pdfplumber(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            text += page.extract_text(layout=True)  # Using layout=True to maintain structure

    return text