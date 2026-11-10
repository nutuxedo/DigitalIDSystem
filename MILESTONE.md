# Milestones and To-Do List

## [DONE/MERGED] Milestone 1: Google Sheets digital ID integration

- [x] Connected the app to Google Sheets.
- [x] Added Google OAuth login and token reuse.
- [x] Read Google Form responses.
- [x] Matched columns by header name.
- [x] Added ID, name, role, band, and status fields.
- [x] Added approved, pending, revoked, invalid, and unknown ID handling.
- [x] Displayed ID details in the CLI.
- [x] Added setup instructions to the README.
- [x] Added required dependencies.

## [DONE] Milestone 2: QR code generation

- [x] Added ID, event, and expiry to QR data.
- [x] Signed QR data to prevent unnoticed changes.
- [x] Generate QR images for approved IDs.
- [x] Added a prompt to generate and preview QR codes.
- [x] Created a folder for generated QR codes.

## [DONE] Milestone 3: Test and harden ID verification

- [x] Tested approved, pending, revoked, and unknown IDs.
- [x] Tested duplicate IDs.
- [x] Improved error messages.
- [x] Tested missing Google Sheet columns.
- [x] Confirmed private files are ignored by Git.

## [MERGED PR #3] Milestone 4: QR scanning and verification

- [x] Read QR data from images.
- [x] Verified QR signatures.
- [x] Checked expiry dates and approval status.
- [x] Displayed clear results.
- [x] Tested valid, changed, expired, and revoked QR codes.

## Milestone 5: Event-ready bouncer verification (Target: November 20)

Goal: a reliable prototype for event use. A laptop runs the local Flask
verifier, and a phone or tablet scans QR codes through its browser.

- [x] Run the verifier on a laptop.
- [x] Start the local Flask web app.
- [x] Add a browser scan page.
- [x] Scan QR codes with a device camera.
- [x] Connect scans to signature verification.
- [x] Display clear results.
- [x] Support repeated scanning.
- [x] Handle invalid and unreadable QR codes.
- [x] Work without internet access.
- [x] Test the event workflow.
- [x] Prepare a laptop backup method.

## To-do after Milestone 5

Planned before or after the November 20 event:

- [ ] Add one CLI menu for all tools. [MUST]
- [ ] Show ID details in the verifier app. [MUST]
- [ ] Protect the private signing key.
- [ ] Check current revocation status.
- [ ] Handle malformed QR data safely.
- [ ] Store less personal information in QR codes.
- [ ] Detect public/private key mismatches.
- [ ] Build a native Android QR verifier.
- [ ] Redo the README.
