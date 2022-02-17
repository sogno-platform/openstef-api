==========
OpenSTEF API
==================================================
This project exposes the functionality of the openstef package through an FASTApi based API.
This repo is very much a Work in Progress, and currently released for Sogno

## Example data files can be obtained in the [openstef-api-example-data](https://github.com/alliander-opensource/openstef-api-example-data) repo

## Installation

1. Make a virtual environment for this repository:
    ```bash
    cd <your_repo>
    python -m venv .venv
    source .venv/bin/activate
    ```
1. Install the general dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the app locally, then open your browser at: http://127.0.0.1:8000.
    ```bash
    cd <your_repo>
    gunicorn -k "uvicorn.workers.UvicornWorker" -c app/core/initializers/gunicorn_conf.py "app.main:app" --reload
    # optional set the number of workers using: `--workers N`
    ```

### Unit testing

1. Install the test dependencies -if applicable-:
    ```bash
    pip install -r test-requirements.txt
2. Run the unit tests locally:
    ```bash
    cd <your_repo>
    pytest
    ```

## Template structure

This templates structures the API so as to stimulate best practices in API design.
* It allows you to easily provide multiple major API versions in parallel.
* It decouples the (web-)API from the (business) logic.
* It provides a simple, yet easy to extend Settings management (based on Pydantic) with
    * automatic parsing and validation from environment variables/ConfigMaps and
    * different settings for local and remote deployment.

```
app
├── core                                (API core functionality)
|
├── routers                             (API endpoints and their implementation)
│   ├── {router name, e.g. pets}        (Collection of endpoints related to "pets")
│   │   └── v1                          (v1 version of this router)
│   │       ├── api_models.py           (Defines request and response data models)
│   │       ├── api_view.py             (Defines API endpoints. Uses controller.py to handle the actual logic)
│   │       ├── client.py               (Optional: wraps database/external API/library access)
│   │       ├── controller.py           (Defines the logic of the API. Uses repository.py to access data.)
│   │       └── repository.py           (Exposes read and write access to datasets, external APIs and databases.)
│   │   └── v2                          (v2 version of this router)
│   │       ├── [...]                   (... add code here for v2 version)
|
├── versions                            (Defines the major API versions)
│   └── v1.py
│   └── v2.py                           (... copy and adapt from v1.py if needed)
|
├── app_settings.py                     (APP and API settings)
└── main.py                             (Main entry point to initialize and start the app)
```

# License
This project is licensed under the Mozilla Public License, version 2.0 - see LICENSE for details.
