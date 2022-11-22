# OpenAIRE Zenodo JSON dumps processing

## Introduction

The OpenAIRE data are published using a [REST API](https://graph.openaire.eu/develop/api.html#rproducts) or [JSON dumps on Zenodo](https://zenodo.org/record/6616871).
This repository provides a set of scripts for processing the JSON dumps:

* Download them from Zenodo.
* Import them into a Postgresql database.
  * At least for now the data is kept as JSON in the database.
    This is enough to allow to query all the data at once (and joininig different entity types using relations)
    and doesn't require to mappping of the OpenAIRE JSON schema to a relational database schema.

## Runtime environment

* A postgresql database instance, e.g. as a docker container:
  ```bash
  DBPSWD="***"
  docker run --name openairedb -p 5432:5432 -v "$HOME/openairePostgresql:/var/lib/postgresql/data" -e "POSTGRES_PASSWORD=$DBPSWD" -d postgres
  echo "127.0.0.1:5432:postgres:postgres:$DBPSWD" >> ~/.pgpass && chmod 600 ~/.pgpass
  ```
* Python3 (more or less in any version) with the psycopg2 module
* Curl
* Storage
  * The Postgresql database should use fast SSD storage. Without that you're doomed.
  * You need around 700 GB of storage for the Postgresql database (as for the dump from mid 2022).
  * On top of that you need around 150 GB of storage for the data downloaded from the Zenodo (as for the fump from mid 2022).

## Usage

Run:

* `./dwnld.sh` to download the data (data will be placed in the working directory)
* `./import.sh` do ingest the data into the database.
  * The script assumes the downloaded data is stored in the working directory.
    If not, pass the path do the data as the first parameter, e.g.
    ```bash
    ./import.sh ../path/to/data
    ```
  * The script assumes Postgresql connection parameters of `host=127.0.0.1 user=postgres`
    (which match the docker setup provided above).
    If you need to adjust them, use the following syntax:
    ```bash
    ./import.sh . --dbConf "host=myHost port=myPort user=myUser password=myPassword dbname=myDbName"
    ```
  * Other parameters of the `import.py` script (see below) can be passed to it in a same way as
    the database connection parameter - just append them ad the end of the `./import.sh` call.
  * The `import.sh` assumes the `import.py` is available in the working directory.
    If it's not the case, provide its location with the `IMPORTSCRIPT` environment variable, e.g.:
    ```bash
    IMPORTSCRIPT=../other/location/import.py ./import.sh
    ```

Remarks:

* The whole ingestion will likely take a few days and will be dominated by the relations ingestion time.
* You can import single JSON files using the `import.py` script.
  Run `import.py --help` and take a look at the `import.sh` script for details.

## Data model

* Entities (communities_infrastructures, datasets, datasources, organizations, other_research_products, projects, publications and software)
  are stored in individual tables with the same simple structure:
  * `id` - entity id in the OpenAIRE (pretty long text)
  * `type` - entity type `communities_infrastructures/datasets/datasources/organizations/other_research_products/projects/publications/software`
  * `data` - JSON data about the entity.
    The schema of this data is described in https://zenodo.org/record/5799514.
* There is a view `entities` providing access to all entity types at once. It also follows the `id`, `type`, `data` schema.
* Relations are stored in a separate table `relations` with three columns extracted from the OpenAIRE JSON data 
  `sourceid`, `targetid` and `reltype`.
  * Because of the number of relations the full JSON data aren't imported.

Remarks:

* [Schemas provided by the OpenAIRE](https://zenodo.org/record/5799514) describe all possible properties a given entity type may contain.
  **It doesn't mean all entities actually provide all of them.**
  The data is provided on the best effort basis only, e.g. an author can be denoted in any of following ways:
    ```JSON
    [
      {"fullname": "Patsy Mill"},
      {
        "fullname": "Darko, Godfred",
        "name": "Godfred", 
        "surname": "Darko"
      },
      {
        "fullname": "Charles-Hervé Vacheron",
        "name": "Charles-Hervé", 
        "surname": "Vacheron"
        "pid": {"id": {"value": "0000-0003-1575-5847", "scheme": "orcid_pending"}
      }
    }
    ```
    and the quality of records can vary within a single entity (e.g. some authors of a given publication can be denoted only by the `fullname` while others can have LOD identifiers).
  * We don't know what is a "schema properties coverage" in actual data.
    This has to be explored.

## Making qeuries

Just ;-) use [Postgresql JSON functions](https://www.postgresql.org/docs/15/functions-json.html) to extract desired information pieces from the `data` column and process further with SQL, e.g.:

```sql
-- get counts for the "label" property of the "bestaccessright" property on dataset entities
select data->'bestaccessright'->>'label', count(*) from datasets group by 1 order by 1;
-- get counts of the "code" property of the "country" array on dataset entities
select  jsonb_array_elements(data->'country')->>'code', count(*) from datasets group by 1;
```

You can find examples of working with JSON in Postgresql on the internet, e.g. in [this blog post](https://dev.to/ftisiot/using-postgresqlr-json-functions-to-navigate-reviews-of-restaurants-in-india-39ld).
