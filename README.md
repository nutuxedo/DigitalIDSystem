# Digital ID System

Work in progress: a Google Sheets-based digital ID system with a Python command-line interface.

> **Note:** This project and its documentation are AI-assisted, but are not 100% AI-generated. The code, ideas, and final changes are reviewed and directed by the developer.

## Current Features

- Reads ID records from a Google Form response worksheet
- Displays basic person and band information
- Handles pending, approved, revoked, and unknown IDs

## How It Works

1. Google Form responses are stored as rows in Google Sheets.
2. Python authenticates with your Google account through OAuth and reads the
   worksheet.
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
2. In **APIs & Services > OAuth consent screen**, configure an OAuth consent
   screen. For a personal hobby project, choose **External**, add your Google
   account as a test user, and request only the read-only Sheets scope.
3. In **APIs & Services > Credentials**, create an OAuth client ID for a
   **Desktop app**. Download the JSON file into this project as
   `oauth_client.json`. Never commit or share this file.
4. Make sure the Google account you use for OAuth has at least **Viewer**
   access to the spreadsheet.
5. Copy the spreadsheet ID from its URL:
   `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`.
6. Install the Python dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

7. Set the spreadsheet ID before running.

   Linux/macOS example:

   ```bash
   export GOOGLE_SHEET_ID="your-spreadsheet-id"
   python main.py
   ```

   PowerShell example:

   ```powershell
   $env:GOOGLE_SHEET_ID = "your-spreadsheet-id"
   python main.py
   ```

The default worksheet name is `Form Responses 1`. If your worksheet has a
different name, set `GOOGLE_WORKSHEET_NAME`:

```bash
export GOOGLE_WORKSHEET_NAME="Responses"
```

Or in PowerShell:

```powershell
$env:GOOGLE_WORKSHEET_NAME = "Responses"
```

The first row must contain columns for an ID, first name, last name, role,
band, and status. Common alternatives such as `ID Number`, `First Name`, and
`Approval Status` are accepted. Every later row is one ID record.

On the first run, the program opens a browser window for Google sign-in and
consent. It saves the authorization token locally in `token.json`, so later
runs normally do not require signing in again. Keep both JSON files private;
they are ignored by Git if you add them to `.gitignore`.

## Run

```bash
python main.py
```

OAuth is used because this is an interactive command-line program run by a
person. Google Cloud does not normally charge for this API usage, and billing
is not needed for this small hobby project.
