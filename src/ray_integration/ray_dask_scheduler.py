import dask

def setup_ray_scheduler():
    """
    Set up Dask to use the Ray scheduler.
    This allows Dask tasks to be executed on a Ray cluster.
    """
    try:
        from ray.util.dask import ray_dask_get
    except ImportError as exc:
        raise RuntimeError("Ray and ray.util.dask are required for Dask-on-Ray execution.") from exc
    dask.config.set(scheduler=ray_dask_get)

def reset_default_scheduler():
    """
    Reset Dask to use the default scheduler.
    """
    dask.config.set(scheduler='threads')  # Or whatever the default is.
