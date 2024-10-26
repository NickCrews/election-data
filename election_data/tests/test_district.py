def test_district(t):
    assert not (t.district == "NULL").any().execute()
