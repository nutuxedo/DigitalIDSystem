# Digital ID System

Work in progress: a Google Sheets-based digital ID system with a Python command-line interface.

> **Note:** This project and its documentation are AI-assisted, but are not 100% AI-generated. The code, ideas, and final changes are reviewed and directed by the developer.

## Current Features

- Currently looks up sample IDs stored in `main.py`
- Displays basic person and band information
- Handles pending, approved, revoked, and unknown IDs

## How It Works

1. The user enters an ID number.
2. The program looks up the ID in the current ID data.
3. The ID status is checked:
   - `approved`: access is allowed and details are displayed
   - `pending`: details are displayed with a pending notice
   - `revoked`: access is denied
   - unknown ID or status: access is denied
4. Google Sheets will eventually serve as the primary data source.

## Run

```bash
python main.py
```

The system is intended to use Google Sheets as its ID data source. The live Google Sheets integration is not implemented yet.