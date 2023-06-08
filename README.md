# ionos-fastapi-backend-service
Python backend service based on FastAPI with Postgres DB for storing the data and Swagger UI for testing the endpoints.

## Prequisites installation
 Install `docker` and `docker compose` by following the tutorials below:
 
 - [docker installation](https://docs.docker.com/engine/install/debian/) 
 - [docker compose installation](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)

## Starting the backend service

Clone the project using the below command.

```bash
git clone git@github.com:sivasundarkarthikeyan/ionos-fastapi-backend-service.git
```

The command below changes the current working directory to the **project's home directory** `ionos-fastapi-backend-service`:

```bash
cd ionos-fastapi-backend-service
```

**Note:** *All the following commands needs to be run from the project's home directory.*

The command below exports the required environment variables required for docker from the file `postgres.env`:
```bash
source set_env.sh
```

The command below creates a local directory named `postgres_data` in `postgres` folder which is linked to postgres docker volume for persisting the data:

```bash
mkdir postgres/postgres_data
```

The fastapi backend and postgres services are started using the below command:
```bash
docker compose up -d
```

The fastapi backend and postgres services can be stopped using the below command:
```bash
docker compose down
```

## Configuration details
The Postgres service container is hosted on the port `5432` and the fastapi backend service is hosted on the port `8000`. Ensure that these two ports are free while testing the service.


## Testing the local client

Click [here](http://127.0.0.1:8000/docs#) to open the Swagger UI created for testing the fastapi service endpoints locally. The list of endpoints available in the API are below:

|Endpoint | Purpose |
| ------- | ------- |
|/        | Endpoint to reach the homepage|
|/health  | Endpoint to check the status of the backend and Postgres service|
|/insert  | Endpoint to insert the rows in the Postgres table|
|/fetch   | Endpoint to fetch all the rows from the Postgres table|
|/filter  | Endpoint to fetch all the matching rows from the Postgres table|
|/nrows   | Endpoint to fetch the total number of records in the Postgres table|
|/update  | Endpoint to update the matching rows with new data in the Postgres table|
|/delete  | Endpoint to delete the matching rows|

## Inspecting Logs
Replace <CONTAINER_NAME> in the command below with FastAPI service container name or tag to inspect the `last 10 logs`:

```bash
docker logs -f --tail 10 <CONTAINER_NAME>
```

## Sample data

The folder `sample data` contains sample input and output data for testing the endpoints `insert`, `update`, `filter` and `delete`. The result data may vary according the present state of the table data, but the return structure stays the same.

