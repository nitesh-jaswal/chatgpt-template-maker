# syntax=docker/dockerfile:1.4
FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
ARG DEBCONF_NONINTERACTIVE_SEEN=true

# Install python & pip, curl for healthchecks, git for model validation, and vim for debugging
RUN apt-get update && apt install -y curl git python3 python3-pip vim python3.10-venv python3-venv zsh sudo tmux htop

RUN apt-get update && apt-get install -y 

# Install pip
RUN pip3 install --upgrade pip && pip3 install "pipenv>=2020.5.28"

# Install poetry
ARG POETRY_VERSION
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# add location where poetry installs to PATH
ENV PATH="/opt/poetry/bin:$PATH"

COPY utils/download-vscode-server.sh .
RUN sudo -E sh download-vscode-server.sh && rm download-vscode-server.sh

# Use an existing package to install zsh (and some of its plugins) in Docker:
# https://github.com/deluan/zsh-in-docker
RUN sh -c "$(curl -fsSL https://github.com/deluan/zsh-in-docker/releases/download/v1.1.3/zsh-in-docker.sh)" -- \
    -t robbyrussell \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions

CMD [ "zsh" ]

# copy these files in for the initial install so that we don't have to go
# through the installation of dependencies during rebuild when we only changed
# the source code
COPY pyproject.toml poetry.lock /opt/repo/
WORKDIR /opt/repo/
RUN poetry config virtualenvs.path /opt/venvs
RUN --mount=type=cache,target=$HOME/.cache/pypoetry/ poetry install --no-root
RUN ln -s $(poetry env info --path) /opt/.venv
ENV PATH /opt/.venv/bin:$PATH

# add our source code and install
COPY src ./src
RUN poetry install --no-root

# add flake8 config for style check at build time
COPY .flake8 .
