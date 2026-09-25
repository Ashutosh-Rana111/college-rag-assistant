import json
import os
import shutil
import tempfile
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


# Google Drive folder containing the college PDFs
FOLDER_ID = "1jSM7QkAaE5sfkPfToyazpeyz9geavI-F"

# PDFs will ultimately live here
PDF_DIR = Path("data/raw_pdfs")

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_drive_service():
    """Create an authenticated Google Drive client."""

    credentials_json = os.environ.get("GDRIVE_SERVICE_ACCOUNT_JSON")

    if not credentials_json:
        raise RuntimeError(
            "GDRIVE_SERVICE_ACCOUNT_JSON environment variable is not set."
        )

    credentials_info = json.loads(credentials_json)

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES,
    )

    return build("drive", "v3", credentials=credentials)


def list_pdfs(service):
    """Return all PDF files directly inside the configured Drive folder."""

    files = []
    page_token = None

    while True:
        response = service.files().list(
            q=(
                f"'{FOLDER_ID}' in parents "
                "and mimeType='application/pdf' "
                "and trashed=false"
            ),
            fields="nextPageToken, files(id, name)",
            pageSize=1000,
            pageToken=page_token,
        ).execute()

        files.extend(response.get("files", []))

        page_token = response.get("nextPageToken")

        if not page_token:
            break

    return files


def download_file(service, file_id, file_name, destination):
    """Download one PDF from Google Drive."""

    request = service.files().get_media(fileId=file_id)

    with open(destination, "wb") as file:
        downloader = MediaIoBaseDownload(file, request)

        done = False

        while not done:
            _, done = downloader.next_chunk()


def download_pdfs():
    """Download the current Drive PDF set safely."""

    service = get_drive_service()
    files = list_pdfs(service)

    print(f"Found {len(files)} PDF(s) in Google Drive.")

    # Temporary directory next to the real PDF directory.
    PDF_DIR.parent.mkdir(parents=True, exist_ok=True)

    temp_dir = Path(
        tempfile.mkdtemp(
            prefix="raw_pdfs_",
            dir=PDF_DIR.parent,
        )
    )

    try:
        for file in files:
            file_name = file["name"]
            file_id = file["id"]

            destination = temp_dir / file_name

            print(f"Downloading: {file_name}")

            download_file(
                service,
                file_id,
                file_name,
                destination,
            )

        # Only replace the existing dataset after every download succeeds.
        if PDF_DIR.exists():
            shutil.rmtree(PDF_DIR)

        temp_dir.rename(PDF_DIR)

        print(f"Successfully updated {PDF_DIR}")
        print(f"Current PDF count: {len(files)}")

    except Exception:
        # Keep the old PDF collection if anything fails.
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


if __name__ == "__main__":
    download_pdfs()
