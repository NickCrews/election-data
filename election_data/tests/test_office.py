import pytest


@pytest.mark.skip
def test_all(t):
    test_normalized(t)
    test_presidential(t)
    test_us_senate(t)


def check_no_bad(bad):
    assert bad.count().execute() == 0, bad.value_counts().execute()


def test_normalized(t):
    bad_office = t.filter(t.office.strip().upper() != t.office).office
    check_no_bad(bad_office)

    non_norm_treasurer = t.filter(
        t.office.contains("TREASURER"),
        t.office.contains("STATE"),
        t.office != "STATE TREASURER",
    ).office
    check_no_bad(non_norm_treasurer)

    non_norm_house = t.filter(
        t.office.contains("HOUSE"),
        ~t.office.contains("COURTHOUSE"),
        t.office.length() < 30,  # remove ballot measures, which are verbose
        t.office != "US HOUSE",
        t.office != "STATE HOUSE",
    ).office
    check_no_bad(non_norm_house)

    non_norm_senate = t.filter(
        t.office.contains("SENATE"),
        t.office.length() < 30,  # remove ballot measures, which are verbose
        t.office != "US SENATE",
        t.office != "STATE SENATE",
    ).office
    check_no_bad(non_norm_senate)

    non_norm_governor = t.filter(
        t.office.contains("GOV"),
        t.office.length() < 30,  # remove ballot measures, which are verbose
        t.office != "GOVERNOR",
        t.office != "LIEUTENANT GOVERNOR",
        t.office != "GOVERNORS COUNCIL",
        t.office != "GOVERNOR'S COUNCIL",
    ).office
    check_no_bad(non_norm_governor)


def test_presidential(t):
    """For every presidential year, there should be presidential results for every state."""
    from election_data import StatePo

    counts_by_state = (
        t.filter(
            t.year % 4 == 0,
            t.office == "US PRESIDENT",
        )
        .group_by("year")
        .agg(states=t.state_po.collect().unique())
    )
    records = counts_by_state.to_pandas().to_dict(orient="records")
    for r in records:
        r["states"] = set(r["states"])
    expected = [{"year": 2020, "states": set(StatePo)}]
    assert records == expected


def test_us_senate(t):
    # https://en.wikipedia.org/wiki/Classes_of_United_States_senators
    class1_states = {
        "AZ",
        "CA",
        "CT",
        "DE",
        "FL",
        "HI",
        "IN",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NJ",
        "NM",
        "NY",
        "ND",
        "OH",
        "PA",
        "RI",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    } | {"DC"}  # Also include DC's shadow senator
    assert len(class1_states) == 34
    class2_states = {
        "AL",
        "AK",
        "AR",
        "CO",
        "DE",
        "GA",
        "ID",
        "IL",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MA",
        "MI",
        "MN",
        "MS",
        "MT",
        "NE",
        "NH",
        "NJ",
        "NM",
        "NC",
        "OK",
        "OR",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "VA",
        "WV",
        "WY",
    } | {"DC"}  # Also include DC's shadow senator
    assert len(class2_states) == 34
    class3_states = {
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "MD",
        "MO",
        "NV",
        "NH",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "SC",
        "SD",
        "UT",
        "VT",
        "WA",
        "WI",
    }
    assert len(class3_states) == 34
    states_by_year = (
        t.filter(
            t.year % 2 == 0,
            t.office == "US SENATE",
        )
        .group_by("year")
        .agg(states=t.state_po.collect().unique())
    )
    records = states_by_year.to_pandas().to_dict(orient="records")
    for r in records:
        r["states"] = set(r["states"])
    expected = [
        {"year": 2018, "states": class1_states},
        # AZ had a special election in 2020: https://en.wikipedia.org/wiki/2020_United_States_Senate_special_election_in_Arizona
        {"year": 2020, "states": class2_states | {"AZ"}},
        # CA is missing US Senate data for 2022: https://github.com/MEDSL/2022-elections-official/issues/23
        {"year": 2022, "states": class3_states - {"CA"}},
    ]
    assert records == expected
