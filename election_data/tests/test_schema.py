import dataclasses


@dataclasses.dataclass
class SchemaMismatchError(Exception):
    extra: set = None
    missing: set = None
    conflicts: set = None
    out_of_order: set = None

    def __str__(self):
        return "\n".join(
            [
                f"Extra columns: {self.extra}",
                f"Missing columns: {self.missing}",
                f"Conflicting columns: {self.conflicts}",
                f"Columns out of order: {self.out_of_order}",
            ]
        )


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
