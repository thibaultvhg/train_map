import requests
import time
import boto3

# Mapbox API credentials
MAPBOX_ACCESS_TOKEN = "sk.eyJ1IjoidGhpYmF1bHR2YW5oZWVnaGUiLCJhIjoiY203cDAyeHhjMGdmOTJrcjNrdXpyb3RxZCJ9.9K-G7fb3SA4M_vbkAWhM0A"
USERNAME = "thibaultvanheeghe"
DATASET_ID = "thibaultvanheeghe.5dq5duqy"  # Get it from Mapbox Studio
NEW_DATA_FILE = r"C:\Users\ThibaultVanheeghe\iCloudDrive\INTERRAIL\Train Data GIS\0merged_new.geojson"  # Path to new dataset


# Step 1: Create an Upload URL
def create_upload_url():
    url = f"https://api.mapbox.com/uploads/v1/{USERNAME}/credentials?access_token={MAPBOX_ACCESS_TOKEN}"
    response = requests.post(url)

    if response.status_code == 200:
        upload_credentials = response.json()
        print("Upload Credentials Response:", upload_credentials)  # Debugging
        return upload_credentials
    else:
        print("Error creating upload URL:", response.status_code, response.text)
        return None


# 🔹 Step 2: Upload the Dataset to AWS S3 using boto3
def upload_to_s3(upload_credentials, file_path):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=upload_credentials["accessKeyId"],
        aws_secret_access_key=upload_credentials["secretAccessKey"],
        aws_session_token=upload_credentials["sessionToken"],
    )

    bucket_name = upload_credentials["bucket"]
    object_key = upload_credentials["key"]

    print(f"📤 Uploading {file_path} to S3 bucket {bucket_name} as {object_key}...")

    with open(file_path, "rb") as data:
        s3.upload_fileobj(data, bucket_name, object_key)

    print("✅ File uploaded successfully to S3!")


# Step 3: Notify Mapbox That the Upload is Ready
def notify_mapbox(upload_credentials, dataset_id):
    url = f"https://api.mapbox.com/uploads/v1/{USERNAME}?access_token={MAPBOX_ACCESS_TOKEN}"
    payload = {
        "url": upload_credentials["url"],
        "tileset": f"{USERNAME}.{dataset_id}",
        "name": "Updated Dataset"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        print("✅ Mapbox upload request successful!")
        print("🔄 Your dataset is now being processed by Mapbox.")
    else:
        print("❌ Error notifying Mapbox:", response.status_code, response.text)


# 🔹 Run the Full Workflow
def refresh_mapbox_dataset():
    print("🚀 Starting dataset refresh...")

    # Step 1: Get Upload Credentials
    upload_credentials = create_upload_url()
    if not upload_credentials:
        return

    # Step 2: Upload File to S3
    upload_to_s3(upload_credentials, NEW_DATA_FILE)

    # Step 3: Notify Mapbox
    dataset_id = "your_tileset_id"  # Replace with your dataset ID in Mapbox Studio
    notify_mapbox(upload_credentials, dataset_id)

# 🔹 Execute the script
refresh_mapbox_dataset()