def test_state(t):
    from election_data import StatePo

    illegal = t.filter(~t.state_po.isin(StatePo))
    illegal_df = illegal.to_pandas()
    assert illegal_df.empty, illegal_df
