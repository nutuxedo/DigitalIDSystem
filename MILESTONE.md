# Milestones and To-Do development

## Milestone 1: Google Sheets digital ID integration

- [x] Connected the Python application to Google Sheets through the Google Sheets API.
- [x] Added OAuth authentication and token reuse.
- [x] Read digital ID records submitted through Google Forms.
- [x] Matched spreadsheet columns by header name instead of fixed column positions.
- [x] Supported ID, first name, last name, role, band, and status fields.
- [x] Implemented approved, pending, revoked, invalid-status, and unknown-ID handling.
- [x] Displayed the matching person's digital ID information in the command-line application.
- [x] Added setup and usage instructions to the README.
- [x] Added the required Google API dependencies.

## Milestone 2: Test and harden ID verification

- [ ] Test an approved ID.
- [ ] Test a pending ID.
- [ ] Test a revoked ID.
- [ ] Test an unknown ID.
- [ ] Test a duplicate ID.
- [ ] Improve error messages.
- [ ] Test missing Google Sheet columns.
- [ ] Confirm private files are ignored by Git.

Done means:

```text
The program handles normal and incorrect input safely.
```