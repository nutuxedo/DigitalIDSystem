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

## [MERGED] Milestone 5: Event-ready bouncer verification

**This milestone is now able to use for the event on Nov 20, if Milestone 6 not finished.**

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

## [ONGOING] Milestone 6 [Refer to GitHub issues]: Cleanups

Planned before or after the November 20 event:
Also check FEEDBACK_TESTS.md for any additional information

- [x] Add one CLI menu for ID lookup/QR generation and QR-image verification. ([#10](https://github.com/nutuxedo/DigitalIDSystem/issues/10))
- [ ] Integrate the Flask phone verifier into the CLI menu.
- [x] Show ID details in the verifier app. [MUST] ([#9](https://github.com/nutuxedo/DigitalIDSystem/issues/9))
- [x] Protect the private signing key. ([#5](https://github.com/nutuxedo/DigitalIDSystem/issues/5))
- [x] Check current revocation status. ([#7](https://github.com/nutuxedo/DigitalIDSystem/issues/7))
- [x] Handle malformed QR data safely. ([#6](https://github.com/nutuxedo/DigitalIDSystem/issues/6))
- [ ] Store less personal information in QR codes. ([#11](https://github.com/nutuxedo/DigitalIDSystem/issues/11))
- [x] Detect public/private key mismatches. ([#8](https://github.com/nutuxedo/DigitalIDSystem/issues/8))
- [ ] Redo the README.

## Milestone 7: Major future changes (low prio)

- [ ] Build a native Android QR verifier. ([#12](https://github.com/nutuxedo/DigitalIDSystem/issues/12))
- [ ] Simplify the directory (looks too messy)
- [ ] Package the project into an executable
- [ ] Audience integration (like an event ticket)
