import os
from pathlib import Path


DEFAULT_OAUTH_CLIENT_FILE = "oauth_client.json"
DEFAULT_OAUTH_TOKEN_FILE = "token.json"
DEFAULT_WORKSHEET_NAME = "Form Responses 1"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# These aliases make the code work with common Google Form question wording.
COLUMN_ALIASES = {
    "id": {"id", "id number", "id_number", "idnumber"},
    "lastname": {
        "last name", 
        "lastname", 
        "surname",
        "full name (lastname, firstname)"},
    "firstname": {
        "first name", 
        "firstname", 
        "given name",
        "full name (lastname, firstname)"},
    "role": {"role", "roles", "position"},
    "subrole": {"sub-role", "subrole"},
    "headshot":{"headshot picture", "headshot", "please upload your face (headshot)"},
    "bandname": {
        "band", 
        "band name", 
        "bandname",
        "name of band/artist"},
    "status": {"status", "approval status", "id status"},
    "timestamp": {"timestamp", "time", "date and time"},
    "email": {"email address", "email", "email add"},
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
    oauth_client_file = Path(
        os.getenv("GOOGLE_OAUTH_CLIENT_FILE", DEFAULT_OAUTH_CLIENT_FILE)
    )
    oauth_token_file = Path(
        os.getenv("GOOGLE_OAUTH_TOKEN_FILE", DEFAULT_OAUTH_TOKEN_FILE)
    )
    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")
    worksheet_name = os.getenv("GOOGLE_WORKSHEET_NAME", DEFAULT_WORKSHEET_NAME)

    if not oauth_client_file.is_file():
        raise RuntimeError(
            f"OAuth client file not found at '{oauth_client_file}'. "
            "Download a Desktop OAuth client JSON file and save it as "
            f"'{DEFAULT_OAUTH_CLIENT_FILE}', or set GOOGLE_OAUTH_CLIENT_FILE."
        )
    if not spreadsheet_id:
        raise RuntimeError(
            "GOOGLE_SHEET_ID is not set. Use the ID between /d/ and /edit "
            "in the Google Sheet URL."
        )

    try:
        import gspread
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError as error:
        raise RuntimeError(
            "Google dependencies are missing. Install them with "
            "'python -m pip install -r requirements.txt'."
        ) from error

    credentials = None
    if oauth_token_file.is_file():
        credentials = Credentials.from_authorized_user_file(
            oauth_token_file,
            SCOPES,
        )

    if credentials is None or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                oauth_client_file,
                SCOPES,
            )
            credentials = flow.run_local_server(port=0)
        oauth_token_file.write_text(credentials.to_json(), encoding="utf-8")

    client = gspread.authorize(credentials)

    try:
        worksheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        rows = worksheet.get_all_records()
    except gspread.exceptions.GSpreadException as error:
        raise RuntimeError(
            "Could not read the worksheet. Check the spreadsheet ID, worksheet "
            "name, and that your Google account can access the sheet."
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
