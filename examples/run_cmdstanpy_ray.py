import os

from cloud_stan.backends import RayExecutor
from cloud_stan.cmdstanpy import bernoulli_stan_file, call_model_method


def main() -> None:
    data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}
    with RayExecutor(address=os.getenv("RAY_ADDRESS", "auto")) as ray:
        ref = ray.submit(
            call_model_method,
            bernoulli_stan_file(),
            "sample",
            data=data,
            chains=1,
            iter_warmup=100,
            iter_sampling=100,
        )
        fit = ray.compute(ref)
    print(fit.summary())


if __name__ == "__main__":
    main()
