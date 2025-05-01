from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from azure.storage.blob import BlobServiceClient
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

# Initialize Azure Blob client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def cleanup_highlighted_files():
    """Delete all blobs starting with 'highlighted_' that are older than 2 minutes."""
    try:
        # Get current time in UTC
        current_time = datetime.now(timezone.utc)
        
        # List all blobs in the container
        blobs = container_client.list_blobs()
        
        # Delete blobs that start with 'highlighted_' and are older than 2 minutes
        for blob in blobs:
            if blob.name.startswith('highlighted_'):
                try:
                    # Get blob properties to check creation time
                    blob_client = container_client.get_blob_client(blob.name)
                    properties = blob_client.get_blob_properties()
                    
                    # Get creation time and ensure it's timezone-aware
                    creation_time = properties.creation_time
                    if creation_time.tzinfo is None:
                        creation_time = creation_time.replace(tzinfo=timezone.utc)
                    
                    # Calculate age of the blob
                    blob_age = current_time - creation_time
                    
                    # Delete if older than 2 minutes
                    if blob_age > timedelta(minutes=2):
                        blob_client.delete_blob()
                        print(f"Deleted old highlighted file: {blob.name}")
                    else:
                        print(f"Blob {blob.name} is {blob_age.total_seconds() / 60:.2f} minutes old - not deleting yet")
                except Exception as e:
                    print(f"Error processing blob {blob.name}: {str(e)}")
                    continue
    
    except Exception as e:
        print(f"Error in cleanup_highlighted_files: {str(e)}")

def start_scheduler():
    """Initialize and start the scheduler."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=cleanup_highlighted_files,
        trigger=IntervalTrigger(minutes=1),  # Run every minute
        id='cleanup_job',
        name='Cleanup highlighted files every minute',
        replace_existing=True
    )
    
    if not scheduler.running:
        scheduler.start()
        print("Scheduler started successfully")
    
    return scheduler

if __name__ == "__main__":
    # Start the scheduler when run directly
    scheduler = start_scheduler()
    
    try:
        # Keep the script running
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        # Shutdown the scheduler when the script is stopped
        scheduler.shutdown()
        print("Scheduler stopped") 