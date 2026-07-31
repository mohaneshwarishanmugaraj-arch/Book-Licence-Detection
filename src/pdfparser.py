import opendataloader_pdf


def parse_pdf(pdf_path):

    opendataloader_pdf.convert(
        input_path=pdf_path,
        output_dir="output",
        format="json,markdown"
    )

    print("PDF parsing completed")