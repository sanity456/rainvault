# Release audit

- Mechanism: consensus classifies one catchment surface; a fixed coefficient table computes indicative liters, tank overflow, and capacity status. It does not aggregate supplier categories or select time slots.
- Source policy: roof description, area, rainfall, and tank capacity are public caller declarations. No property records or weather sources are fetched.
- Security: caller-scoped immutable records, input bounds, strict model-label parsing, independent validator rerun, and no funds or privileged global registry.
- Local gates: GenVM lint and strict type check passed; 3 direct tests passed, including arithmetic, unclear surfaces, input bounds, and malformed output.
- StudioNet gate: full deploy/estimate flow passed with its own fresh wallet; final state `OVERFLOW_EXPECTED`; read-only release proof passed. Manifest source bytes and ABI match the deployment.
- Limits: coefficients are indicative planning assumptions, not engineering design, weather prediction, or site verification.
