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

## [DONE] Milestone 2: QR code generation

- [x] Define the QR payload fields: ID, event, and expiry.
- [x] Add signing so QR data cannot be altered unnoticed.
- [x] Generate QR images for approved IDs.
- [x] Add a local prompt to test and preview generated QR codes.
- [x] Create a folder for the generated QRs

## [DONE] Milestone 3: Test and harden ID verification

- [x] Test an approved ID.
- [x] Test a pending ID.
- [x] Test a revoked ID.
- [x] Test an unknown ID.
- [x] Test a duplicate ID.
- [x] Improve error messages.
- [x] Test missing Google Sheet columns.
- [x] Confirm private files are ignored by Git.

## [MERGED PR #3] Milestone 4: QR scanning and verification

- [x] Read QR data directly from an image
- [x] Verify the QR signature automatically
- [x] Check expiry date
- [x] Check approval status
- [x] Display clear accepted/rejected results
- [x] Test valid, tampered, expired, and revoked QR codes

## Milestone 5: Event-ready bouncer verification (Target: November 20)

The immediate goal is a reliable prototype that can be used at the event.
The current direction is a local Flask web verifier: a laptop runs the
verifier and a phone or tablet uses its browser to scan QR codes. A native
phone app remains a possible future direction, not a final decision.

**Crucial Milestone - as this will make the program be able to run on a gig event.**

- [x] Run the verifier on a laptop
- [x] Start a local Flask web verifier
- [x] Display a browser page with a scan button
- [x] Scan QR codes using a device camera
- [x] Connect scanned QR data to Python signature verification
- [x] Display clear ACCEPTED or REJECTED results
- [x] Make repeated scanning quick and easy
- [x] Handle invalid or unreadable QR codes
- [x] Work without internet access
- [x] Test the complete workflow on the event device
- [x] Prepare a backup verification method

## To-do after Milestone 5

Might do these before or after the November 20 music event:

- [ ] Consolidate the .py files into one menu (CLI) [MUST]
- [ ] Show ID details on verifier app [MUST]
- [ ] Protect the private signing key with secure storage or encryption.
- [ ] Check current revocation status instead of trusting an old QR status.
- [ ] Reject malformed QR data without showing a traceback.
- [ ] Reduce personal information stored in QR codes.
- [ ] Detect and safely handle public/private key mismatches.
- [ ] Build a native Android app for QR verification only
- [ ] Revamp README.md

