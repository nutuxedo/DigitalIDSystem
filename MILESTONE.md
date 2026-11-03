# Milestones and To-Do development

## Milestone 1: Google Sheets digital ID integration (Done and Merged)

- [x] Connected the Python application to Google Sheets through the Google Sheets API.
- [x] Added OAuth authentication and token reuse.
- [x] Read digital ID records submitted through Google Forms.
- [x] Matched spreadsheet columns by header name instead of fixed column positions.
- [x] Supported ID, first name, last name, role, band, and status fields.
- [x] Implemented approved, pending, revoked, invalid-status, and unknown-ID handling.
- [x] Displayed the matching person's digital ID information in the command-line application.
- [x] Added setup and usage instructions to the README.
- [x] Added the required Google API dependencies.

## Milestone 2: QR code generation

- [x] Define the QR payload fields: ID, event, and expiry.
- [ ] Add signing so QR data cannot be altered unnoticed.
- [x] Generate QR images for approved IDs.
- [x] Add a local prompt to test and preview generated QR codes.
- [ ] Document QR generation for an event.
- [ ] Create a folder for the generated QRs

## Milestone 3: Test and harden ID verification (Low priority)

- [x] Test an approved ID.
- [x] Test a pending ID.
- [x] Test a revoked ID.
- [x] Test an unknown ID.
- [x] Test a duplicate ID.
- [x] Improve error messages.
- [ ] Test missing Google Sheet columns.
- [x] Confirm private files are ignored by Git.

Done means:

```text
The program handles normal and incorrect input safely.
```
