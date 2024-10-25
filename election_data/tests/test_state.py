from election_data import StatePo


def test_state(data):
    illegal = data.filter(~data.state_po.isin(StatePo))
    illegal_df = illegal.to_pandas()
    assert illegal_df.empty, illegal_df
