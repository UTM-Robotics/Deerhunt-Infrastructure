'''
A blob storage class for storing, checking, and loading submissions as zip files.

For Azure Blob Storage Object Model refer to:
https://docs.microsoft.com/en-ca/azure/storage/blobs/media/storage-blobs-introduction/blob1.png
'''
import os
from server.config import Configuration
from azure.storage.blob import BlobServiceClient

# A local directory to hold blob data
LOCAL_PATH = "./data"

class BlobStorageModel:
    def __init__(self):
        self.key = Configuration.AZURE_KEY
        # Create the BlobServiceClient object
        self.service_client = BlobServiceClient.from_connection_string(self.key)

    def create_container(self, container_name):
        return self.service_client.create_container(container_name)

    def delete_container(self, container_name):
        container_client = self.service_client.get_container_client(container_name)
        container_client.delete_container()

    # Return all the blobs in the container with the given name
    def list_blobs_in_container(self, container_name):
        container = self.get_container(container_name)
        return container.list_blobs()

    def get_container(self, container_name):
        return self.service_client.get_container_client(container_name)

    def upload_blob(self, container_name, blob_name):
        # check if the file is a zip file
        try:
            self.is_zip(blob_name)
        except FileExtensionError as e:
            print('Please upload a zip file')
        # Check if local directory exists
        if not os.is_dir(LOCAL_PATH):
            os.mkdir(LOCAL_PATH)
        upload_file_path = os.path.join(LOCAL_PATH, blob_name)
        # Create a blob client using the file name as the name for the blob
        blob_client = self.service_client.get_blob_client(container=container_name, blob=blob_name)
        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
        # Remove fle from local directory
        os.remove(upload_file_path)
        
    def delete_blob(self, container_name, blob_name):
        blob = self.get_blob(container_name, blob_name)
        blob.delete_blob()

    def get_blob(self, container_name, blob_name):
        container = self.get_container(container_name)
        return container.get_blob_client(blob_name)

    def is_zip(self, blob_file_name):
        split_tup = os.path.splitext(blob_file_name)
        if not split_tup[1] == ".zip":
            raise FileExtensionError("Not a zip file")
        return


class FileExtensionError(Exception):
    pass


