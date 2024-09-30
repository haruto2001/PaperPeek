ARG UBUNTU_VERSION=22.04
FROM ubuntu:${UBUNTU_VERSION}

ARG USERNAME=user
ARG WORKDIR=/work

ENV LANG ja_JP.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

ENV PATH=/venv/bin:$PATH \
    PATH=/root/.cargo/bin:$PATH

RUN adduser --disabled-password --gecos "" ${USERNAME}
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        gosu \
        tmux \
        tree \
        vim \
        wget \
        zsh && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN . $HOME/.bashrc
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN mkdir ${WORKDIR}
WORKDIR ${WORKDIR}

COPY ./pyproject.toml ./uv.lock* ./
RUN uv sync --no-dev

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]