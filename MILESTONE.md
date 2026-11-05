# Milestones and To-Do development

## [DONE/MERGED] Milestone 1: Google Sheets digital ID integration

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
- [x] Add signing so QR data cannot be altered unnoticed.
- [x] Generate QR images for approved IDs.
- [x] Add a local prompt to test and preview generated QR codes.
- [ ] Document QR generation for an event.
- [x] Create a folder for the generated QRs

## [DONE] Milestone 3: Test and harden ID verification (Low priority)

- [x] Test an approved ID.
- [x] Test a pending ID.
- [x] Test a revoked ID.
- [x] Test an unknown ID.
- [x] Test a duplicate ID.
- [x] Improve error messages.
- [x] Test missing Google Sheet columns.
- [x] Confirm private files are ignored by Git.

Done means:

```text
The program handles normal and incorrect input safely.
```

## Milestone 4: QR scanning and verification

- [x] Read QR data directly from an image
- [x] Verify the QR signature automatically
- [x] Check expiry date
- [x] Check approval status
- [x] Display clear accepted/rejected results
- [x] Test valid, tampered, expired, and revoked QR codes

## Milestone 5: Bouncer device verification

- [ ] Run the verifier on a phone, tablet, or laptop
- [ ] Scan QR codes using the device camera
- [ ] Display clear ACCEPTED or REJECTED results
- [ ] Make repeated scanning quick and easy
- [ ] Handle invalid or unreadable QR codes
- [ ] Test the workflow at an event

## Future security and reliability follow-up

These improvements are intentionally deferred until the core project is complete:

- [ ] Protect the private signing key with secure storage or encryption.
- [ ] Check current revocation status instead of trusting an old QR status.
- [ ] Reject malformed QR data without showing a traceback.
- [ ] Reduce personal information stored in QR codes.
- [ ] Detect and safely handle public/private key mismatches.
