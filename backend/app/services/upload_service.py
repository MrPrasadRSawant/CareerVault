import uuid
from pathlib import Path

import anyio
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".md"}


async def save_upload(file: UploadFile, user_id: uuid.UUID) -> tuple[str, str, int]:
    """Persist an upload off the event loop and return its metadata."""
    original_name = file.filename or "file"
    extension = Path(original_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported file type '{extension}'. "
            f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    upload_dir = Path(settings.UPLOAD_DIR) / str(user_id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid.uuid4().hex}{extension}"
    file_path = upload_dir / file_name

    return await anyio.to_thread.run_sync(
        _write_upload, file.file, file_path, settings.MAX_UPLOAD_SIZE, original_name
    )


def _write_upload(source, file_path: Path, max_upload_size: int, original_name: str) -> tuple[str, str, int]:
    """Write a spooled upload from a worker thread, not the ASGI event loop."""
    size = 0
    try:
        with file_path.open("wb") as destination:
            while chunk := source.read(1024 * 1024):
                size += len(chunk)
                if size > max_upload_size:
                    raise ValueError
                destination.write(chunk)
    except ValueError:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {max_upload_size} bytes limit",
        )

    return original_name, str(file_path), size


def delete_upload(file_path: str) -> None:
    """Remove an unreferenced upload after its HTTP response has been sent."""
    Path(file_path).unlink(missing_ok=True)
