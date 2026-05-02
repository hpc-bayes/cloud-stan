import os

from dask.distributed import Client

from cloud_stan.bridgestan import log_density
from cloud_stan.cmdstanpy import bernoulli_stan_file


def main() -> None:
    scheduler = os.environ["DASK_SCHEDULER_ADDRESS"]
    data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}
    task = log_density(bernoulli_stan_file(), [0.0], data=data)

    with Client(scheduler) as client:
        value = client.compute(task).result()
    print(value)


if __name__ == "__main__":
    main()
