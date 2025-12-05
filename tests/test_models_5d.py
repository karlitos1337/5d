from src.universal_system_genesis_5d.models_5d import (
    FiveDProfile,
    aggregate_5d,
    project_profile_to_3d,
)


def test_aggregate_5d_equal_weights():
    profile = FiveDProfile(0.2, 0.4, 0.6, 0.8, 1.0)
    agg = aggregate_5d(profile)
    assert abs(agg - (0.2 + 0.4 + 0.6 + 0.8 + 1.0) / 5) < 1e-9


def test_project_profile_to_3d():
    profile = FiveDProfile(0.5, 0.7, 0.3, 0.9, 0.4)
    res = project_profile_to_3d(profile)
    assert set(res.keys()) == {"mind", "society", "tech"}
    assert abs(res["mind"] - (0.5 + 0.7) / 2) < 1e-9
    assert abs(res["society"] - (0.3 + 0.9) / 2) < 1e-9
    assert res["tech"] == 0.4
