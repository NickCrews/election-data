import ibis
import pytest
from ibis import _

# ┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ mode             ┃ CountStar(ibis_read_parquet_rlyp5bxitrhanaykejcdaepit4) ┃
# ┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
# │ string           │ int64                                                   │
# ├──────────────────┼─────────────────────────────────────────────────────────┤
# │ TOTAL            │                                                20344100 │
# │ ELECTION DAY     │                                                 3301064 │
# │ ABSENTEE         │                                                 2707749 │
# │ PROVISIONAL      │                                                 1562572 │
# │ EARLY            │                                                 1516644 │
# │ NOT ABSENTEE     │                                                 1252855 │
# │ ABSENTEE BY MAIL │                                                  630956 │
# │ UNSPECIFIED      │                                                  451357 │
# │ ONE STOP         │                                                  443871 │
# │ IN-PERSON        │                                                  261275 │
# │ …                │                                                       … │
# └──────────────────┴─────────────────────────────────────────────────────────┘


def test_mode(t):
    assert (t.mode == t.mode.strip().upper()).all().execute()
    # There aren't other total-ish modes lurking in there
    assert (t.filter(t.mode.contains("TOTAL")).mode == "TOTAL").all().execute()


# This currently doesn't appear to hold :(
@pytest.mark.skip
def test_total_matches_sum_of_components(t):
    # If we have some data like
    # ┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┓
    # ┃ office   ┃ precinct           ┃ candidate         ┃ mode         ┃ votes  ┃
    # ┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━┩
    # │ string   │ string             │ string            │ string       │ string │
    # ├──────────┼────────────────────┼───────────────────┼──────────────┼────────┤
    # │ GOVERNOR │ ARMADA TOWNSHIP 01 │ DARYL M SIMPSON   │ ABSENTEE     │ 1      │
    # │ GOVERNOR │ ARMADA TOWNSHIP 01 │ DARYL M SIMPSON   │ TOTAL        │ 2      │
    # │ GOVERNOR │ ARMADA TOWNSHIP 01 │ DARYL M SIMPSON   │ ELECTION DAY │ 1      │
    # │ GOVERNOR │ ARMADA TOWNSHIP 01 │ DONNA BRANDENBURG │ ELECTION DAY │ 4      │
    # │ GOVERNOR │ ARMADA TOWNSHIP 01 │ DONNA BRANDENBURG │ ABSENTEE     │ 7      │
    # │ GOVERNOR │ ARMADA TOWNSHIP 01 │ DONNA BRANDENBURG │ TOTAL        │ 11     │
    # │ GOVERNOR │ ARMADA TOWNSHIP 01 │ GRETCHEN WHITMER  │ TOTAL        │ 670    │
    # │ GOVERNOR │ ARMADA TOWNSHIP 01 │ GRETCHEN WHITMER  │ ABSENTEE     │ 383    │
    # │ GOVERNOR │ ARMADA TOWNSHIP 01 │ GRETCHEN WHITMER  │ ELECTION DAY │ 287    │
    # │ GOVERNOR │ ARMADA TOWNSHIP 01 │ KEVIN HOGAN       │ ABSENTEE     │ 0      │
    # └──────────┴────────────────────┴───────────────────┴──────────────┴────────┘
    # we expect the TOTAL mode to be the sum of the other modes.
    by_cand_by_precinct = t.group_by(
        *[c for c in t.columns if c not in {"mode", "votes"}]
    ).agg(
        votes_total=_.votes.try_cast(int).sum(where=_.mode == "TOTAL"),
        votes_other=_.votes.try_cast(int).sum(where=_.mode != "TOTAL"),
        others=ibis.struct({"mode": _.mode, "votes": _.votes}).collect(
            where=_.mode != "TOTAL"
        ),
    )
    by_cand_by_precinct = by_cand_by_precinct.cache()
    is_problem = ibis.and_(
        _.votes_total.notnull(),
        _.votes_other.notnull(),
        _.votes_total != _.votes_other,
    )
    problems = by_cand_by_precinct.filter(is_problem)
    assert problems.count().execute() == 0, problems.execute()

    # t.filter(
    #     _.year == 2022,
    #     _.state_po == "NY",
    #     _.office == "STATE HOUSE",
    #     _.district == "101",
    #     _.precinct == "AN 1",
    #     _.candidate == "BRIAN M MAHER",
    # ).order_by(
    #     "party_detailed",
    # )
    # ┏━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┓
    # ┃ year  ┃ date       ┃ state_po ┃ county_name ┃ county_fips ┃ jurisdiction_name ┃ jurisdiction_fips ┃ district ┃ office      ┃ magnitude ┃ special ┃ stage  ┃ precinct ┃ writein ┃ candidate     ┃ party_detailed ┃ party_simplified ┃ mode         ┃ votes  ┃ readme_check ┃
    # ┡━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━┩
    # │ int16 │ date       │ string   │ string      │ string      │ string            │ string            │ string   │ string      │ int64     │ boolean │ string │ string   │ boolean │ string        │ string         │ string           │ string       │ string │ boolean      │
    # ├───────┼────────────┼──────────┼─────────────┼─────────────┼───────────────────┼───────────────────┼──────────┼─────────────┼───────────┼─────────┼────────┼──────────┼─────────┼───────────────┼────────────────┼──────────────────┼──────────────┼────────┼──────────────┤
    # │  2022 │ 2022-11-08 │ NY       │ DELAWARE    │ 36025       │ DELAWARE          │ 36025             │ 101      │ STATE HOUSE │         1 │ False   │ GEN    │ AN 1     │ False   │ BRIAN M MAHER │ CONSERVATIVE   │ OTHER            │ ELECTION_DAY │ 22     │ True         │
    # │  2022 │ 2022-11-08 │ NY       │ DELAWARE    │ 36025       │ DELAWARE          │ 36025             │ 101      │ STATE HOUSE │         1 │ False   │ GEN    │ AN 1     │ False   │ BRIAN M MAHER │ CONSERVATIVE   │ OTHER            │ TOTAL        │ 24     │ True         │
    # │  2022 │ 2022-11-08 │ NY       │ DELAWARE    │ 36025       │ DELAWARE          │ 36025             │ 101      │ STATE HOUSE │         1 │ False   │ GEN    │ AN 1     │ False   │ BRIAN M MAHER │ REPUBLICAN     │ REPUBLICAN       │ ABSENTEE     │ 17     │ True         │
    # │  2022 │ 2022-11-08 │ NY       │ DELAWARE    │ 36025       │ DELAWARE          │ 36025             │ 101      │ STATE HOUSE │         1 │ False   │ GEN    │ AN 1     │ False   │ BRIAN M MAHER │ REPUBLICAN     │ REPUBLICAN       │ ELECTION_DAY │ 170    │ True         │
    # │  2022 │ 2022-11-08 │ NY       │ DELAWARE    │ 36025       │ DELAWARE          │ 36025             │ 101      │ STATE HOUSE │         1 │ False   │ GEN    │ AN 1     │ False   │ BRIAN M MAHER │ REPUBLICAN     │ REPUBLICAN       │ TOTAL        │ 205    │ True         │
    # └───────┴────────────┴──────────┴─────────────┴─────────────┴───────────────────┴───────────────────┴──────────┴─────────────┴───────────┴─────────┴────────┴──────────┴─────────┴───────────────┴────────────────┴──────────────────┴──────────────┴────────┴──────────────┘
