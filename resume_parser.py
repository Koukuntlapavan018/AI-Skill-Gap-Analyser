from pypdf import PdfReader


def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# Test the resume parser
resume_path = input("Enter the path of your resume PDF: ")

resume_text = extract_text_from_pdf(resume_path)

print("\n==========================================")
print("           RESUME TEXT")
print("==========================================")

print(resume_text)