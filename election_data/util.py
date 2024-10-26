import ibis
from ibis import _
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


def compare(
    a: ir.StringValue, b: ir.StringValue, *, norm: bool = True
) -> ir.BooleanValue:
    from IPython.display import display

    if norm:
        a = a.upper().strip()
        b = b.upper().strip()
    a = a.name("val")
    b = b.name("val")
    vc_a = a.value_counts(name="n_a")
    vc_b = b.value_counts(name="n_b")
    vc = vc_a.outer_join(vc_b, "val", lname="{name}_a", rname="{name}_b")
    w1 = vc.order_by(_.n_a.desc())
    w2 = vc.order_by(_.n_b.desc())
    display(w1)
    display(w2)
