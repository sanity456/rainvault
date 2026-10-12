"""Opt-in full StudioNet flow with a new encrypted wallet."""
import json
import secrets

from gltest.types import TransactionHashVariant
from release_support import prepare, save_proof, send


def test_studionet_rain_vault_flow():
    ctx = prepare("rain_vault.py", ("creator",))
    creator, account = ctx["contracts"]["creator"], ctx["accounts"]["creator"]
    transactions = {"deploy": ctx["deployment_hash"]}
    estimate_key = "release_" + secrets.token_hex(4)
    send(transactions, "estimate", creator.estimate(args=[estimate_key, "A single impermeable standing-seam metal roof catchment surface.", 100, 20, 1000]))
    estimate_id = account.address.lower() + ":" + estimate_key
    final = json.loads(creator.get_estimate(args=[estimate_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL))
    assert final["surface"] == "HARD_ROOF" and final["estimated_liters"] == 1700, final
    assert final["overflow_liters"] == 700 and final["status"] == "OVERFLOW_EXPECTED", final
    save_proof(ctx, transactions, estimate_id, "OVERFLOW_EXPECTED")
