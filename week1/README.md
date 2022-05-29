## Topics covered in week 1:
- Docker
- Docker Compose
- PostgreSQL
- pgAdmin
- pgcli
- Terraform
- Google Cloud Plataform

### Notes:
Notion page: https://www.notion.so/pcrespoo/Week-1-adea5a2dbf0f44e49749238957f99754

### Commands learned in week 1:

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

- Docker Compose:
```
docker-compose up
```

- Terraform
    - terraform init: here we are basically initializing default parameters, like specifying the provider, the backend state file that will manage all the resources to be created, etc

    - terraform plan: here, we will pass to the state file which resources we want to have and their parameters

    - terraform apply: the state file will have all the plan to be executed. Then, running this command, it will create all the resources for us
        - if we decide to create more resources during development stage, we basically need to add more resources to the main file, run 
        “terraform plan” and “terraform apply” to apply the changes

        
    - terraform destroy: if we want to remove all the resources created