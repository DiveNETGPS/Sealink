# DiveNET: Sealink-OEM

Clean landing page for the Sealink-OEM repository.

## Where to start

- Product docs and source bundle: [`Sealink-OEM-main/`](Sealink-OEM-main/)
- Main product overview: [`Sealink-OEM-main/README.md`](Sealink-OEM-main/README.md)
- Requirements and options (canonical): [`Sealink-OEM-main/Sealink-OEM_Requirements_and_Options.md`](Sealink-OEM-main/Sealink-OEM_Requirements_and_Options.md)
- Integrator/testing process guide: [`Sealink-OEM-main/integrations/PLATFORM_INTEGRATOR_GUIDE.md`](Sealink-OEM-main/integrations/PLATFORM_INTEGRATOR_GUIDE.md)

## Repository layout

- `Sealink-OEM-main/` is the canonical documentation + integration content.
- Root-level build/release scripts (`*.bat`, `*.spec`, `VERSION.txt`) are packaging utilities.
- `release/` and `release_assets/` hold generated/customer-facing distribution assets.

## Testing release policy

- Do not resend a new tester app for GitHub sync-only or documentation-only updates.
- Resend the Operator Package only when candidate runtime behavior changes.
- Keep one published test baseline until a new candidate is intentionally announced.

Questions: support@divenetgps.com
