def test_year(t):
    assert t.year.isin([2018, 2019, 2020, 2021, 2022, 2023]).all().execute()
    assert t.year.notnull().all().execute()
