from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_helm_values_files_are_valid_yaml():
    values_files = [
        ROOT / "stan_dask_chart" / "values.yaml",
        ROOT / "stan_ray_chart" / "ray_cluster" / "values.yaml",
        *sorted((ROOT / "examples" / "cloud").glob("*/*-values.yaml")),
    ]

    for path in values_files:
        with path.open(encoding="utf-8") as handle:
            parsed = yaml.safe_load(handle)
        assert isinstance(parsed, dict), path


def test_chart_templates_do_not_contain_placeholder_ellipses():
    template_files = [
        *sorted((ROOT / "stan_dask_chart" / "templates").glob("*.yaml")),
        *sorted((ROOT / "stan_ray_chart" / "ray_cluster" / "templates").glob("*.yaml")),
    ]

    for path in template_files:
        assert "\n  ...\n" not in path.read_text(encoding="utf-8"), path


def test_cloud_provider_examples_exist_for_dask_and_ray():
    for provider in ("aws", "gcp", "azure"):
        provider_dir = ROOT / "examples" / "cloud" / provider
        assert (provider_dir / "README.md").exists()
        assert (provider_dir / "dask-values.yaml").exists()
        assert (provider_dir / "ray-values.yaml").exists()
