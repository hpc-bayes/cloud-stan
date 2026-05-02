from pathlib import Path

import pytest


@pytest.fixture
def bernoulli_stan_file():
    path = Path(__file__).resolve().parents[1] / "src" / "stan" / "bernoulli.stan"
    assert path.exists()
    return path


@pytest.fixture
def bernoulli_data():
    return {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}
