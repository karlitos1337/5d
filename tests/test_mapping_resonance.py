from src.universal_system_genesis_5d.mapping_resonance import project_5d_to_3d


def test_project_5d_to_3d_basic():
    dims = {
        "neurobiology": 0.8,
        "psychology": 0.6,
        "philosophy": 0.4,
        "economics": 0.2,
        "technology": 0.9,
    }
    res = project_5d_to_3d(dims)
    assert set(res.keys()) == {"mind", "society", "tech"}
    assert abs(res["mind"] - (0.8 + 0.6) / 2) < 1e-9
    assert abs(res["society"] - (0.4 + 0.2) / 2) < 1e-9
    assert res["tech"] == 0.9
