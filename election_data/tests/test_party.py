import ibis
from ibis import _


def test_party_combos(data):
    data = data.head(1000)
    is_allowed = ibis.or_(
        ibis.and_(_.party_simplified == "OTHER", _.party_detailed.length() > 0),
        ibis.and_(_.party_simplified == "DEMOCRAT", _.party_detailed == "DEMOCRAT"),
        ibis.and_(_.party_simplified == "REPUBLICAN", _.party_detailed == "REPUBLICAN"),
    )
    illegal = data.filter(~is_allowed)
    illegal_df = illegal.to_pandas()
    assert illegal_df.empty, illegal_df
