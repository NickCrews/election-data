import dataclasses


@dataclasses.dataclass
class SchemaMismatchError:
    extra: set = None
    missing: set = None
    conflicts: set = None
    out_of_order: set = None


def test_schema(t):
    from election_data import RESULTS_SCHEMA

    s = t.schema()
    extra = set(s) - set(RESULTS_SCHEMA)
    missing = set(RESULTS_SCHEMA) - set(s)
    conflicts = {
        (col, s[col], RESULTS_SCHEMA[col])
        for col in set(s) & set(RESULTS_SCHEMA)
        if s[col] != RESULTS_SCHEMA[col]
    }

    if set(s) == set(RESULTS_SCHEMA):
        out_of_order = {
            (col, s[col], RESULTS_SCHEMA[col])
            for i, col in enumerate(RESULTS_SCHEMA)
            if col != list(s)[i]
        }
    else:
        out_of_order = set()

    if extra or missing or conflicts or out_of_order:
        raise SchemaMismatchError(extra, missing, conflicts, out_of_order)
