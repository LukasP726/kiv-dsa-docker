# KIV-DSA Docker Demos

Tento repozitář obsahuje tři postupně náročnější demonstrační projekty, které ukazují práci s kontejnery, Docker Compose a jednoduchou automatizaci generování konfigurací. Každé demo je samostatné a má vlastní `README.md` s návodem na spuštění.

## Struktura repozitáře

- `demo-1`  
  Úvod do Docker Compose, spuštění jednoho uzlu/kontejneru a základní správa životního cyklu.
- `demo-2`  
  Dvě služby (backend + frontend), build vlastních image a mapování portů, přístup k aplikaci z hosta.
- `demo-3`  
  Generování konfigurací před startem, škálování backendů a load‑balancing přes NGINX.
- `tools`  
  Pomocné Python skripty pro generování diagramů a assets (`compose_to_mermaid.py`, `generate_demo3_assets.py`).

## Požadované nástroje a verze

Repozitář používá moderní Docker Compose v2 (příkaz `docker compose`) a Taskfile v3. Konkrétní verze nástrojů nejsou v repozitáři explicitně zafixované, ale minimálně je potřeba:

- **Docker Engine**: `20.10+`  
  (kvůli pluginu Docker Compose v2)
- **Docker Compose (plugin)**: `2.0+`  
  (příkaz `docker compose`, nikoli `docker-compose`)
- **Taskfile (task)**: `v3`  
  (soubor `Taskfile.yml` má `version: "3"`)
- **Python**: `3.8+`  
  (pro `task graph` a `task prepare`, skripty v `tools/`)

Poznámka: Base image použitá v demo kontejnerech je `ghcr.io/maxotta/kiv-dsa-vagrant-base-docker:latest`. Pokud se tag `latest` změní, může to ovlivnit chování dem (záměrně není pinováno na konkrétní verzi).

## Instalace

1. Nainstalujte Docker Desktop (Windows/macOS) nebo Docker Engine (Linux).  
   [Docker Get Started](https://docs.docker.com/get-started/get-docker/)  
   [Docker Engine Install](https://docs.docker.com/engine/install/)
2. Ověřte, že funguje `docker compose version`.
3. Nainstalujte Taskfile (`task`).  
   [Taskfile Install](https://taskfile.dev/docs/installation/)
4. Ujistěte se, že máte Python 3 (`python --version` nebo `python3 --version`).

## Spuštění dem

Každé demo má vlastní návod. Příklad:

- `demo-?`: `task start` (před startem třetího tasku proběhne `task prepare`)

Další informace a obrázky najdete v jednotlivých `README.md`:

- `demo-?/README.md`


