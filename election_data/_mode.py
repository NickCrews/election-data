import ibis
from ibis.expr import types as ir


def clean_mode(mode: ir.StringValue) -> ir.StringValue:
    EARLY_PATTERN = r".*EARLY.*"
    ABSENTEE_PATTERN = r".*ABSENTEE.*"
    return (
        ibis.case()
        .when(mode.re_search(EARLY_PATTERN), "EARLY")
        .when(mode.re_search(ABSENTEE_PATTERN), "ABSENTEE")
        .end()
    )
