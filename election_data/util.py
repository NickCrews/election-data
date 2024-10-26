import ibis
from ibis.expr import types as ir


def cases(
    branch: tuple[ir.BooleanValue, ibis.Value],
    *branches: tuple[ir.BooleanValue, ibis.Value],
    else_: ibis.Value | None = None,
) -> list[tuple[ir.BooleanValue, ibis.Value]]:
    """A way to use ibis.cases() before it is released."""
    builder = ibis.case()
    builder = builder.when(*branch)
    for condition, value in branches:
        builder = builder.when(condition, value)
    return builder.else_(else_).end()
