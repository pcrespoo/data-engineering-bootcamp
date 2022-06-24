import os
from google.cloud import storage

init_url = 'https://nyc-tlc.s3.amazonaws.com/trip+data/'
BUCKET = os.environ.get("GCP_GCS_BUCKET", "dtc_data_lake_dtc-boot-7639")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "/google/credentials/google_credentials.json")

def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

def web_to_gcs(year, service):
    for i in range(12):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        # parquet file_name 
        file_name = service + '_tripdata_' + year + '-' + month + '.parquet'

        # download it using bash command
        os.system(f'wget {init_url + file_name} -O {file_name}')

        # upload it to gcs 
        upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
        print(f"GCS: {service}/{file_name}")


web_to_gcs('2019', 'green')
web_to_gcs('2020', 'green')
# web_to_gcs('2019', 'yellow')
# web_to_gcs('2020', 'yellow')