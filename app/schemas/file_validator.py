from fastapi import UploadFile

class FileValidator:
    @staticmethod
    def validate_pdf_file(file: UploadFile):
        errors = []
        if file.content_type != "application/pdf":
            print(f"Invalid file type: {file.content_type},")
            errors.append("file must be a PDF file")
        return errors