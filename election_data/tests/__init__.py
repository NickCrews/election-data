from election_data.tests.test_candidate import test_candidate
from election_data.tests.test_district import test_district
from election_data.tests.test_party import test_party
from election_data.tests.test_schema import test_schema
from election_data.tests.test_state import test_state
from election_data.tests.test_year import test_year


def test_all(t):
    test_candidate(t)
    test_party(t)
    test_schema(t)
    test_state(t)
    test_year(t)
    test_district(t)
