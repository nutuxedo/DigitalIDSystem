import os
from pathlib import Path


DEFAULT_CREDENTIALS_FILE = "credentials.json"
DEFAULT_WORKSHEET_NAME = "Form Responses 1"

# These aliases make the code work with common Google Form question wording.
COLUMN_ALIASES = {
    "id": {"id", "id number", "id_number", "idnumber"},
    "lastname": {"last name", "lastname", "surname"},
    "firstname": {"first name", "firstname", "given name"},
    "role": {"role", "position"},
    "bandname": {"band", "band name", "bandname"},
    "status": {"status", "approval status", "id status"},
}


def _normalize_column_name(column_name):
    return " ".join(str(column_name).strip().lower().replace("_", " ").split())


def _find_columns(headers):
    normalized_headers = {
        _normalize_column_name(header): header for header in headers
    }
    columns = {}

    for field, aliases in COLUMN_ALIASES.items():
        matching_header = next(
            (
                normalized_headers[normalized_header]
                for normalized_header in normalized_headers
                if normalized_header in aliases
            ),
            None,
        )
        if matching_header is None:
            raise RuntimeError(
                f"Google Sheet is missing a column for '{field}'. "
                f"Expected one of: {', '.join(sorted(aliases))}."
            )
        columns[field] = matching_header

    return columns


def load_id_lists():
    """Read ID records from the Google Form response worksheet."""
    credentials_file = Path(
        os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", DEFAULT_CREDENTIALS_FILE)
    )
    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")
    worksheet_name = os.getenv("GOOGLE_WORKSHEET_NAME", DEFAULT_WORKSHEET_NAME)

    if not credentials_file.is_file():
        raise RuntimeError(
            f"credentials file not found at '{credentials_file}'. "
            "Set GOOGLE_SERVICE_ACCOUNT_FILE to its path."
        )
    if not spreadsheet_id:
        raise RuntimeError(
            "GOOGLE_SHEET_ID is not set. Use the ID between /d/ and /edit "
            "in the Google Sheet URL."
        )

    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError as error:
        raise RuntimeError(
            "Google dependencies are missing. Install them with "
            "'python -m pip install -r requirements.txt'."
        ) from error

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
    ]
    credentials = Credentials.from_service_account_file(
        credentials_file,
        scopes=scopes,
    )
    client = gspread.authorize(credentials)

    try:
        worksheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        rows = worksheet.get_all_records()
    except gspread.exceptions.GSpreadException as error:
        raise RuntimeError(
            "Could not read the worksheet. Check the spreadsheet ID, worksheet "
            "name, and that the sheet is shared with the service account email."
        ) from error

    if not rows:
        return {}

    columns = _find_columns(rows[0].keys())
    id_lists = {}
    for row_number, row in enumerate(rows, start=2):
        id_number = str(row[columns["id"]]).strip()
        if not id_number:
            continue
        if id_number in id_lists:
            raise RuntimeError(
                f"Duplicate ID '{id_number}' found on worksheet row {row_number}."
            )

        id_lists[id_number] = {
            field: str(row[header]).strip()
            for field, header in columns.items()
            if field != "id"
        }

    return id_lists
