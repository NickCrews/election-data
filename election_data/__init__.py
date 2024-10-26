import enum

import ibis
from ibis.expr import types as ir

from election_data import tests as tests
from election_data import util as util
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


class PartySimplified(enum.StrEnum):
    DEMOCRAT = "DEMOCRAT"
    REPUBLICAN = "REPUBLICAN"
    LIBERTARIAN = "LIBERTARIAN"
    GREEN = "GREEN"
    INDEPENDENT = "INDEPENDENT"
    NONPARTISAN = "NONPARTISAN"
    OTHER = "OTHER"


class Stage(enum.StrEnum):
    PRI = "PRI"
    GEN = "GEN"
    GEN_RUNOFF = "GEN RUNOFF"
    GEN_RECOUNT = "GEN RECOUNT"
    GEN_RECOUNT_2 = "GEN RECOUNT 2"
