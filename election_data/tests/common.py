import ibis.expr.types as ir


def check_strings(s: ir.StringColumn):
    assert (s == s.upper().strip()).all().execute()
    assert (s != "NULL").all().execute()
    assert (s != "").all().execute()
