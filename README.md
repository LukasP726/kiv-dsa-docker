# KIV-DSA Docker Demos

This repository contains three progressively more advanced demo projects that showcase containers, Docker Compose, and simple config generation automation. Each demo is self‑contained and has its own `README.md` with run instructions.

## Repository Structure

- `demo-1`  
  Intro to Docker Compose, a single node/container, and basic lifecycle management.
- `demo-2`  
  Two services (backend + frontend), building custom images, port mapping, and host access.
- `demo-3`  
  Pre‑startup config generation, backend scaling, and NGINX load balancing.
- `tools`  
  Helper Python scripts for diagram and asset generation (`compose_to_mermaid.py`, `generate_demo3_assets.py`).

## Required Tools and Versions

This repo uses Docker Compose v2 (`docker compose`) and Taskfile v3. Exact versions are not pinned, but at minimum you need:

- **Docker Engine**: `20.10+`  
  (for the Docker Compose v2 plugin)
- **Docker Compose (plugin)**: `2.0+`  
  (`docker compose`, not `docker-compose`)
- **Taskfile (task)**: `v3`  
  (`Taskfile.yml` uses `version: "3"`)
- **Python**: `3.8+`  
  (for `task graph` and `task prepare`, scripts in `tools/`)

Note: The base image used in the demo containers is `ghcr.io/maxotta/kiv-dsa-vagrant-base-docker:latest`. If the `latest` tag changes, demo behavior may change as well (intentionally not pinned to a specific version).

## Installation

1. Install Docker Desktop (Windows/macOS) or Docker Engine (Linux).  
   [Docker Get Started](https://docs.docker.com/get-started/get-docker/)  
   [Docker Engine Install](https://docs.docker.com/engine/install/)
2. Verify that `docker compose version` works.
3. Install Taskfile (`task`).  
   [Taskfile Install](https://taskfile.dev/docs/installation/)
4. Make sure Python 3 is available (`python --version` or `python3 --version`).

## Running the Demos

Each demo has its own instructions. Example:

- `demo-?`: `task start` (task 3 runs `task prepare` before start)

More details and images are in the demo READMEs:

- `demo-?/README.md`


