# syntax=docker/dockerfile:1.7

FROM python:3.11-slim AS runtime

ARG INSTALL_EXTRAS="cmdstanpy,bridgestan,ray"
ARG INSTALL_CMDSTAN="false"
ARG CMDSTAN_VERSION=""

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    CLOUD_STAN_HOME=/app

LABEL org.opencontainers.image.title="cloud-stan" \
      org.opencontainers.image.description="Run CmdStanPy and BridgeStan workloads on Dask and Ray." \
      org.opencontainers.image.source="https://github.com/your-org/cloud-stan" \
      org.opencontainers.image.licenses="GPL-3.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        make \
        g++ \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${CLOUD_STAN_HOME}

COPY pyproject.toml README.md ./
COPY src ./src
COPY examples ./examples

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install ".[${INSTALL_EXTRAS}]"

RUN if [ "${INSTALL_CMDSTAN}" = "true" ]; then \
      python -m cmdstanpy.install_cmdstan \
        --dir /opt \
        ${CMDSTAN_VERSION:+--version "${CMDSTAN_VERSION}"} \
        --cores 2; \
    fi

RUN useradd --create-home --shell /usr/sbin/nologin cloudstan \
    && chown -R cloudstan:cloudstan ${CLOUD_STAN_HOME} /opt

USER cloudstan

CMD ["python", "-c", "import cloud_stan; print(f'cloud-stan {cloud_stan.__version__} ready')"]
