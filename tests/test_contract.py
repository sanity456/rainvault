import json
from pathlib import Path

import pytest


@pytest.fixture
def setup(direct_vm, direct_deploy, direct_accounts):
    creator = direct_accounts[0]
    direct_vm.sender = creator
    source = Path(__file__).parents[1] / "contracts" / "rain_vault.py"
    return direct_deploy(str(source), sdk_version="v0.2.16")


def mock(vm, surface):
    vm.clear_mocks()
    vm.mock_llm("Classify the described primary roof catchment surface", json.dumps({"surface": surface}))


def test_hard_roof_volume_and_overflow(setup, direct_vm):
    mock(direct_vm, "HARD_ROOF")
    record_id = setup.estimate("storm1", "An impermeable standing-seam metal roof.", 100, 20, 1000)
    state = json.loads(setup.get_estimate(record_id))
    assert state["estimated_liters"] == 1700
    assert state["overflow_liters"] == 700
    assert state["status"] == "OVERFLOW_EXPECTED"
    assert direct_vm.run_validator(leader_result="HARD_ROOF")
    assert not direct_vm.run_validator(leader_result="GREEN_ROOF")


def test_unclear_surface_does_not_claim_capacity(setup, direct_vm):
    mock(direct_vm, "UNCLEAR")
    record_id = setup.estimate("unclear", "Several mixed surfaces with no area split.", 100, 20, 1000)
    state = json.loads(setup.get_estimate(record_id))
    assert state["surface"] == "UNCLEAR" and state["status"] == "UNCLEAR"
    assert state["estimated_liters"] == 0


def test_bad_inputs_and_model_failure_are_atomic(setup, direct_vm):
    with direct_vm.expect_revert("area out of range"):
        setup.estimate("bad", "Metal roof", 0, 20, 1000)
    with direct_vm.expect_revert("rainfall out of range"):
        setup.estimate("bad", "Metal roof", 100, 0, 1000)
    mock(direct_vm, "NOT_A_SURFACE")
    with direct_vm.expect_revert("invalid surface"):
        setup.estimate("bad", "Metal roof", 100, 20, 1000)
    assert setup.estimate_count() == 0
