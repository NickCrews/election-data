def test_candidate(t):
    from election_data.tests.common import check_strings

    # There ARE some null candidates, I think that's OK
    # assert t.candidate.notnull().all().execute()
    check_strings(t.candidate)

    assert (t.filter(~t.writein).candidate != "WRITEIN").all().execute()
    assert t.filter(t.candidate == "WRITEIN").writein.all().execute()
    # Some candidates are marked as writein, but not named "WRITEIN"
    # eg OTHER, BRIAN CARROLL, etc.
    # assert (~t.filter(t.candidate != "WRITEIN").writein).all().execute()
    # assert (t.filter(t.writein).candidate == "WRITEIN").all().execute()
