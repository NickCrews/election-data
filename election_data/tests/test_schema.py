import election_data as ed


def test_schema(data):
    assert data.schema() == ed.RESULTS_SCHEMA
