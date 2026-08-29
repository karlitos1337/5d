FROM mcr.microsoft.com/devcontainers/python:3.12-bullseye

# The base image ships an apt source for dl.yarnpkg.com whose signing key has
# since been rotated/expired, causing "apt-get update" to fail with
# "NO_PUBKEY 62D54FD4003F6525" during dev container feature installation
# (e.g. the Python feature). We don't need the Yarn apt repo, so remove it.
RUN rm -f /etc/apt/sources.list.d/yarn.list
