def test_schema(t):
    from election_data import RESULTS_SCHEMA

    assert t.schema() == RESULTS_SCHEMA
