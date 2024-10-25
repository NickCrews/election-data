import enum

import ibis
from ibis.expr import types as ir

from election_data._mode import clean_mode as clean_mode


class ResultsTable(ibis.Table):
    year = ir.IntegerColumn
    date = ir.DateColumn
    state_po = ir.StringColumn
    county_name = ir.StringColumn
    county_fips = ir.StringColumn
    jurisdiction_name = ir.StringColumn
    jurisdiction_fips = ir.StringColumn
    district = ir.StringColumn
    office = ir.StringColumn
    magnitude = ir.IntegerColumn
    special = ir.BooleanColumn
    stage = ir.StringColumn
    precinct = ir.StringColumn
    writein = ir.BooleanColumn
    candidate = ir.StringColumn
    party_detailed = ir.StringColumn
    party_simplified = ir.StringColumn
    mode = ir.StringColumn
    votes = ir.StringColumn
    readme_check = ir.BooleanColumn


RESULTS_SCHEMA = ibis.schema(
    {
        "year": "int16",
        "date": "date",
        "state_po": "string",
        "county_name": "string",
        "county_fips": "string",
        "jurisdiction_name": "string",
        "jurisdiction_fips": "string",
        "district": "string",
        "office": "string",
        "magnitude": "int64",
        "special": "boolean",
        "stage": "string",
        "precinct": "string",
        "writein": "boolean",
        "candidate": "string",
        "party_detailed": "string",
        "party_simplified": "string",
        "mode": "string",
        "votes": "string",
        "readme_check": "boolean",
    }
)


class StatePo(enum.StrEnum):
    AK = "AK"
    AL = "AL"
    AR = "AR"
    AZ = "AZ"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DC = "DC"
    DE = "DE"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    IA = "IA"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    MA = "MA"
    MD = "MD"
    ME = "ME"
    MI = "MI"
    MN = "MN"
    MO = "MO"
    MS = "MS"
    MT = "MT"
    NC = "NC"
    ND = "ND"
    NE = "NE"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NV = "NV"
    NY = "NY"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VA = "VA"
    VT = "VT"
    WA = "WA"
    WI = "WI"
    WV = "WV"
    WY = "WY"


assert len(StatePo) == 51


class Mode(enum.StrEnum):
    ABSENTEE = "ABSENTEE"
    EARLY = "EARLY"


def make_results(
    t: ibis.Table,
    *,
    year: ir.IntegerValue | int,
    date: ir.DateValue | str,
    state_po: ir.StringValue | str,
    county_name: ir.StringValue,
    county_fips: ir.StringValue,
    jurisdiction_name: ir.StringValue,
    jurisdiction_fips: ir.StringValue,
    district: ir.StringValue,
    office: ir.StringValue,
    magnitude: ir.IntegerValue | int,
    special: ir.BooleanValue | bool,
    stage: ir.StringValue,
    precinct: ir.StringValue,
    writein: ir.BooleanValue | bool,
    candidate: ir.StringValue,
    party_detailed: ir.StringValue,
    party_simplified: ir.StringValue,
    mode: ir.StringValue,
    votes: ir.StringValue,
    readme_check: ir.BooleanValue | bool,
) -> ResultsTable:
    if isinstance(date, str):
        date = ibis.date(date)
    return t.select(
        year=year,
        date=date,
        state_po=state_po,
        county_name=county_name,
        county_fips=county_fips,
        jurisdiction_name=jurisdiction_name,
        jurisdiction_fips=jurisdiction_fips,
        district=district,
        office=office,
        magnitude=magnitude,
        special=special,
        stage=stage,
        precinct=precinct,
        writein=writein,
        candidate=candidate,
        party_detailed=party_detailed,
        party_simplified=party_simplified,
        mode=mode,
        votes=votes,
        readme_check=readme_check,
    ).cast(RESULTS_SCHEMA)
