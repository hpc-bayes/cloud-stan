import os

from cloud_stan.backends import RayExecutor
from cloud_stan.bridgestan import call_model_method
from cloud_stan.cmdstanpy import bernoulli_stan_file


def main() -> None:
    data = {"N": 10, "y": [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]}
    with RayExecutor(address=os.getenv("RAY_ADDRESS", "auto")) as ray:
        ref = ray.submit(call_model_method, bernoulli_stan_file(), "log_density", [0.0], data=data)
        value = ray.compute(ref)
    print(value)


if __name__ == "__main__":
    main()
