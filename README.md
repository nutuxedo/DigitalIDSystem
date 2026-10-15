# Digital ID System

Work in progress: a Google Sheets-based digital ID system with a Python command-line interface.

> **Note:** This project and its documentation are AI-assisted, but are not 100% AI-generated. The code, ideas, and final changes are reviewed and directed by the developer.

## Current Features

- Reads ID records from a Google Form response worksheet
- Displays basic person and band information
- Handles pending, approved, revoked, and unknown IDs

## How It Works

1. Google Form responses are stored as rows in Google Sheets.
2. Python authenticates with a Google service account and reads the worksheet.
3. The user enters an ID number.
4. The program looks up the ID in the downloaded rows.
5. The ID status is checked:
   - `approved`: access is allowed and details are displayed
   - `pending`: details are displayed with a pending notice
   - `revoked`: access is denied
   - unknown ID or status: access is denied
6. Google Sheets is the primary data source; the local program does not keep a
   second copy of the ID records.

## Google Sheets setup

1. In Google Cloud, create a project and enable the **Google Sheets API**.
2. Create a service account and download its JSON key into this project as
   `credentials.json`. Never commit or share this file.
3. Open the JSON file and copy the service account's `client_email`.
4. Share the Google Sheet with that email as a **Viewer**. The program only
   requests read-only access.
5. Copy the spreadsheet ID from its URL:
   `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`.
6. Install the Python dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

7. Set the spreadsheet ID before running. PowerShell example:

   ```powershell
   $env:GOOGLE_SHEET_ID = "your-spreadsheet-id"
   python main.py
   ```

The default worksheet name is `Form Responses 1`. If your worksheet has a
different name, set `GOOGLE_WORKSHEET_NAME`:

```powershell
$env:GOOGLE_WORKSHEET_NAME = "Responses"
```

The first row must contain columns for an ID, first name, last name, role,
band, and status. Common alternatives such as `ID Number`, `First Name`, and
`Approval Status` are accepted. Every later row is one ID record.

## Run

```bash
python main.py
```

The service account is used because this is a non-interactive command-line
program: it can authenticate without asking a person to sign in every run.