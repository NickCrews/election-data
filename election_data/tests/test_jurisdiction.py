## Fix jurisdiction and jurisdiction_fips

# Looks like in the upstream data, jurisdiction is always the same as
# the county. So just use that.

# Be warned, it appears that the upstream FIPS codes for jurisdictions are somewhat BS.
# For example, the "DISTRICT 12" jurisdiction in alaska has a FIPS code of "02012"
# which isn't a [real fips code](https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt)
# FIPS codes really only go down to county level. Probably this DISTRICT 12
# is actually referring to state HD 12, even though it is filed under the
# US HOUSE office:


def test_jurisdiction(t):
    return
    # return (
    #     t.filter(
    #         t.office == "US HOUSE",
    #         t.jurisdiction_name.re_search("\d+"),
    #         t.state_po == "AK",
    #     )
    #     .select(
    #         "state_po",
    #         "jurisdiction_name",
    #         "jurisdiction_fips",
    #     )
    #     .value_counts()
    # )
