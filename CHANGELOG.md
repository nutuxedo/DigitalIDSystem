# Changelog

## v0.4.0-alpha - 2026-11-14

### Added

- Unified CLI menu for ID lookup, QR generation, and QR-image verification ([#10](https://github.com/nutuxedo/DigitalIDSystem/issues/10)).
- CLI controls to start and stop the Flask QR verifier ([#15](https://github.com/nutuxedo/DigitalIDSystem/issues/15)).
- Browser-based QR verification UI with separated static assets.
- Initial `pytest` coverage for Google Sheets column parsing.

### Improved

- Event configuration is saved and reused between runs.
- QR verification now checks signatures, expiry dates, current approval status, and registry changes ([#6](https://github.com/nutuxedo/DigitalIDSystem/issues/6), [#7](https://github.com/nutuxedo/DigitalIDSystem/issues/7)).
- Malformed QR data and key mismatches are handled more safely ([#6](https://github.com/nutuxedo/DigitalIDSystem/issues/6), [#8](https://github.com/nutuxedo/DigitalIDSystem/issues/8)).
- Private signing keys are protected with restricted file permissions ([#5](https://github.com/nutuxedo/DigitalIDSystem/issues/5)).
- README and project documentation were expanded and reorganized.

### Known limitations

- QR payloads still contain personal details; reducing stored personal information remains tracked in [#11](https://github.com/nutuxedo/DigitalIDSystem/issues/11).
- Automated test coverage is still incomplete ([#17](https://github.com/nutuxedo/DigitalIDSystem/issues/17)).

## v0.3.1-alpha - 2026-11-12

### Improved

- Hardened QR generation and verification.
- Added live registry checks and clearer verifier responses.
- Merged Milestone 6 CLI and OAuth improvements ([#16](https://github.com/nutuxedo/DigitalIDSystem/pull/16)).

## v0.3.0-alpha - 2026-11-12

### Added

- Initial unified CLI menu for the project tools.
- OAuth re-login handling for expired credentials ([#14](https://github.com/nutuxedo/DigitalIDSystem/issues/14)).

## v0.2.0-alpha - 2026-11-08

### Added

- Browser-based Flask QR verifier.
- QR image decoding and verification.
- Event-ready offline verification workflow ([#4](https://github.com/nutuxedo/DigitalIDSystem/pull/4)).

### Improved

- Disabled Flask debug mode for safer event use.

## v0.1.0-alpha - 2026-11-05

### Added

- Initial Google Sheets digital ID lookup flow.
- QR generation for approved IDs.
- Ed25519 signing and verification for QR payloads.
- QR expiry and approval-status checks.
- Persistent signing-key support.
- Initial project documentation and setup files ([#3](https://github.com/nutuxedo/DigitalIDSystem/pull/3)).
