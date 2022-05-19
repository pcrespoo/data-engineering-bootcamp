## Topics covered in week 1 so far:
- Docker
- Docker Compose
- PostgreSQL
- pgAdmin
- pgcli

### Commands learned in week 1 so far:

- dataset: https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.parquet

 - build an image:
 ```
 docker build -t IMAGE_NAME .
 ``` 
 - run an image :
 ```
 docker run -it IMAGE_NAME
 ```
- run a postgres image 
```
docker run -it  \
    -e POSTGRES_USER='root' \
    -e POSTGRES_PASSWORD='root' \
    -e POSTGRES_DB='ny_taxi' \
    -v "YOUR_PATH/ny_taxi_postgres_data:/var/lib/postgresql/data" \
    -p 5432:5432 \
    postgres:13 
```

- how to connect to a postgres database with pgcli: 
```
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

- pgAdmin image: 
```
docker run -it \
        -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 \
        dpage/pgadmin4
```
    - 8080: the port in the local machine
    - 80: the port used by pgAdmin
    - 8080:80 is the setup to connect the local machine with pgAdmin

- create a docker network: 
```
docker network create pedro_network
```
 
- update PostgreSQL image: 
```
docker run -it  \
    -e POSTGRES_USER='root' \
    -e POSTGRES_PASSWORD='root' \
    -e POSTGRES_DB='ny_taxi' \
    -v "YOUR_PATH/ny_taxi_postgres_data:/var/lib/postgresql/data" \
    -p 5432:5432 \
    --network=pedro_network \
    --name pg-database-teste \
    postgres:13
```

- update pgAdmin image with network settings: 
```
docker run -it \
        -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
        -e PGADMIN_DEFAULT_PASSWORD="root" \
        -p 8080:80 \
        --network=pedro_network \
        --name pgAdmin-bootcamp \
        dpage/pgadmin4
```

- build an image for the data ingestion process: 
```
docker build -t taxi_ingest:v001 .
```

- run the docker image for data ingestion using the same network used by pgAdmin and PostgreSQL:
```
docker run -it \
    --network=pedro_network \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database-teste\
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_data \
        --url="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.parquet"
```
