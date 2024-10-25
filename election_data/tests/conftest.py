import ibis
import pytest


def pytest_addoption(parser) -> None:
    parser.addoption("--data", action="store", default="data/cleaned.parquet")


@pytest.fixture
def data(request) -> ibis.Table:
    path = request.config.getoption("--data")
    if path.endswith(".csv"):
        return ibis.read_csv(path)
    elif path.endswith(".parquet"):
        return ibis.read_parquet(path)
    else:
        raise ValueError(f"Unsupported file format: {path}")
