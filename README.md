# RainVault

SUBMISSION HOLD: This version is a one-party, self-declared rainwater estimate. Although its local and StudioNet tests passed, it lacks a shared decision or independently sourced evidence strong enough for the current GenLayer review standard. Do not submit this deployment as a review-ready intelligent contract. A different mechanism and new deployment are required.

Batch C1. A reusable GenLayer intelligent contract for an indicative rainwater-capture calculation. A caller supplies one roof-surface description, catchment area, rainfall depth, and tank capacity. Independent validators categorize the surface; deterministic code applies the documented coefficient and computes captured liters, overflow, and a capacity status.

This is a rough scenario estimate from declared inputs. It neither verifies a real property nor predicts actual weather or safe installation capacity. `UNCLEAR` surfaces receive no positive capture estimate. Do not use this result for engineering or flood-safety decisions without professional measurements.

## Interface

`estimate(estimate_key, roof_description, area_m2, rainfall_mm, tank_liters)` stores an owner-scoped record. `get_estimate(estimate_id)` returns the canonical calculation and `estimate_count()` returns the record count. Inputs are bounded and records are immutable.

## Review boundary

The model only classifies surface material. Validators repeat and compare that label from the same source description. The fixed coefficient table is hard roof 8,500 bps, green roof 5,500 bps, pervious 3,000 bps, and unclear 0 bps. Liters equal square meters times millimeters times coefficient divided by 10,000; overflow is the amount above tank capacity.

## Verification

Run `genvm-lint check contracts/rain_vault.py`, `genvm-lint typecheck contracts/rain_vault.py --strict`, and `pytest -q`. The opt-in StudioNet smoke test uses an isolated encrypted wallet and records an exact source/ABI/deployment proof in `deployments/studionet.json`.

StudioNet deployment: [0x9400b2B3C3187A1335fe05C4Eb877465C2697DDf](https://explorer-studio.genlayer.com/address/0x9400b2B3C3187A1335fe05C4Eb877465C2697DDf). See `AUDIT.md` for the review boundary and test results.
