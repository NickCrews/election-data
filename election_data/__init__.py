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
    """Postal code for the state (or DC). See `StatePo`."""
    county_name = ir.StringColumn
    county_fips = ir.StringColumn
    jurisdiction_name = ir.StringColumn
    jurisdiction_fips = ir.StringColumn
    district = ir.StringColumn
    office = ir.StringColumn
    magnitude = ir.IntegerColumn
    special = ir.BooleanColumn
    stage = ir.StringColumn
    """Primary, general, etc. See `Stage`."""
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
        # if you roundtrip an int8 to parquet and back, the dtype changes
        # to int32. This looks like a bug on the ibis or duckdb side.
        # Whatever, just lean into it.
        "magnitude": "int32",
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
    """PO codes (eg AK, AL, etc) for all 50 states, plus DC."""

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
    """Democrat, Republican, etc.

    If this value is eg DEMOCRAT, then the party_detailed value should also
    be DEMOCRAT. Same thing for REPUBLICAN, etc: If party_simplified is REPUBLICAN,
    then party_detailed should be REPUPLICAN too.

    When party_simplified is OTHER, the party_detailed value should be something
    else, eg "WORKING FAMILIES PARTY" or "CONSTITUTION PARTY".
    """

    DEMOCRAT = "DEMOCRAT"
    REPUBLICAN = "REPUBLICAN"
    LIBERTARIAN = "LIBERTARIAN"
    GREEN = "GREEN"
    INDEPENDENT = "INDEPENDENT"
    NONPARTISAN = "NONPARTISAN"
    OTHER = "OTHER"


class Stage(enum.StrEnum):
    """Primary, general, etc."""

    PRI = "PRI"
    GEN = "GEN"
    GEN_RUNOFF = "GEN RUNOFF"
    GEN_RECOUNT = "GEN RECOUNT"
    GEN_RECOUNT_2 = "GEN RECOUNT 2"


class Office(enum.StrEnum):
    """The more common office types.

    Some states have unique offices that don't fit into these categories,
    eg "COUNTY 132 COMMISSIONER"
    """

    US_PRESIDENT = "US PRESIDENT"
    US_SENATE = "US SENATE"
    US_HOUSE = "US HOUSE"
    GOVERNOR = "GOVERNOR"
    LIEUTENANT_GOVERNOR = "LIEUTENANT GOVERNOR"
    ATTORNEY_GENERAL = "ATTORNEY GENERAL"
    STATE_TREASURER = "STATE TREASURER"
    SECRETARY_OF_STATE = "SECRETARY OF STATE"
    COMPTROLLER = "COMPTROLLER"
    STATE_SENATE = "STATE SENATE"
    STATE_HOUSE = "STATE HOUSE"
    SCHOOL_BOARD = "SCHOOL BOARD"
    MAYOR = "MAYOR"
