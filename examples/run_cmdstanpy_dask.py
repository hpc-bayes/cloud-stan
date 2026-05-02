import os

from dask.distributed import Client

from cloud_stan.cmdstanpy import bernoulli_stan_file, sample


def main() -> None:
    scheduler = os.environ["DASK_SCHEDULER_ADDRESS"]
    data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}
    task = sample(bernoulli_stan_file(), data=data, chains=1, iter_warmup=100, iter_sampling=100)

    with Client(scheduler) as client:
        fit = client.compute(task).result()
    print(fit.summary())


if __name__ == "__main__":
    main()
