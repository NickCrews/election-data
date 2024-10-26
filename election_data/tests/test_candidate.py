def test_candidate(t):
    # There ARE some null candidates, I think that's OK
    # assert t.candidate.notnull().all().execute()
    assert (t.candidate.length() > 0).all().execute()
    assert (t.candidate == t.candidate.upper()).all().execute()

    assert (t.filter(~t.writein).candidate != "WRITEIN").all().execute()
    assert t.filter(t.candidate == "WRITEIN").writein.all().execute()
    # Some candidates are marked as writein, but not named "WRITEIN"
    # eg OTHER, BRIAN CARROLL, etc.
    # assert (~t.filter(t.candidate != "WRITEIN").writein).all().execute()
    # assert (t.filter(t.writein).candidate == "WRITEIN").all().execute()
