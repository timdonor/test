import firebase_admin
from firebase_admin import credentials, storage
import requests
import time
from datetime import datetime

# Firebase Admin SDK Initialization
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'espfirebasedemo-acf81.appspot.com'
})
# gs://espfirebasedemo-acf81.appspot.com
# Reference to Firebase Storage
bucket = storage.bucket()

# Function to create a timestamped filename
def generate_timestamped_filename(base_name):
    timestamp = datetime.now().strftime('%d-%B-%Y-%H:%M:%S')
    return f'{base_name}-{timestamp}'

# Function to upload an image to Firebase Storage
def upload_image(file_path):
    timestamped_filename = generate_timestamped_filename('image')
    blob = bucket.blob(f'images/{timestamped_filename}.jpg')
    blob.upload_from_filename(file_path)
    print(f'File {file_path} uploaded to {blob.name}.')

# Blynk API Configuration
BLYNK_AUTH_TOKEN = 'DSb2WZsyByg4vCwr8m30nfyi_K3v6t_0'
VIRTUAL_PIN = 'V1'  # Change this to your widget's Virtual Pin
BLYNK_API_URL = f'https://ny3.blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}&{VIRTUAL_PIN}'

def get_image_url():
    try:
        response = requests.get(BLYNK_API_URL, timeout=10)
        response.raise_for_status()
        # Assuming the URL is in the response
        image_url = response.text.strip()
        return image_url
    except requests.RequestException as e:
        print(f"Error retrieving image URL: {e}")
        return None

def download_image(image_url):
    try:
        image_response = requests.get(image_url, timeout=10)
        image_response.raise_for_status()
        with open('image.jpg', 'wb') as f:
            f.write(image_response.content)
        print("Image downloaded successfully.")
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")

def main():
    previous_image_id = None  # Initialize outside the loop
    while True:
        image_url = get_image_url()
        if image_url:
            print(f"Image URL: {image_url}")
            download_image(image_url)
            # Extract image ID from URL
            image_id = image_url.split('=')[-1]
            if image_id == previous_image_id:
                print("Image already uploaded.")
            else:
                previous_image_id = image_id
                upload_image('image.jpg')
        else:
            print("Failed to retrieve image URL.")
        
        time.sleep(2)  # Check every 60 seconds

if __name__ == "__main__":
    main()
