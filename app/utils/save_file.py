import os.path
from pathlib import Path

def get_project_root() -> Path:
    current_file = Path(__file__).resolve()
    return current_file.parent.parent.parent

def get_temporary_local_storage_path() -> Path:
    root_dir = get_project_root()
    return root_dir / "storage_files"

def get_path(file_id: str) -> Path:
    storage_root = get_temporary_local_storage_path()
    storage_path = storage_root / "pdf" / file_id
    storage_path.mkdir(parents=True, exist_ok=True)
    return storage_path

def save_pdf_file(file_id: str, pdf_file) -> str:
    storage_path = get_path(file_id)

    # Save pdf file
    pdf_path = storage_path / pdf_file.filename
    with open(pdf_path, 'wb') as f:
        content = pdf_file.file.read()
        f.write(content)

    relative_pdf_path = os.path.relpath(pdf_path, get_temporary_local_storage_path())
    return relative_pdf_path

def get_pages_path():
    storage_root = get_temporary_local_storage_path()
    storage_path = storage_root / "pages"
    storage_path.mkdir(parents=True, exist_ok=True)
    return storage_path

def get_file_path(path: str) -> str:
    return os.path.relpath(path, get_temporary_local_storage_path())

def get_full_filepath(path):
    return get_temporary_local_storage_path() / path

def delete_stored_file(file_path: str) -> bool:
    full_path = os.path.join(get_temporary_local_storage_path(), file_path)

    if os.path.exists(full_path) and os.path.isfile(full_path):
        os.remove(full_path)

        parent_dir = os.path.dirname(full_path)

        if os.path.exists(parent_dir) and not os.listdir(parent_dir):
            os.rmdir(parent_dir)

        return True

    return False