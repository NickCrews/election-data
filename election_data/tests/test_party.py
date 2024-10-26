import ibis
from ibis import _


def test_party(t):
    from election_data import PartySimplified

    simples = PartySimplified.__members__.keys()

    is_allowed = ibis.or_(
        *[
            ibis.and_(_.party_simplified == simple, _.party_detailed == simple)
            for simple in simples
        ],
        ibis.and_(
            _.party_simplified == "OTHER",
            _.party_detailed.length() > 0,
            _.party_detailed.notin(simples),
        ),
    )
    illegal = t.filter(~is_allowed)
    illegal_df = illegal.to_pandas()
    assert illegal_df.empty, illegal_df
