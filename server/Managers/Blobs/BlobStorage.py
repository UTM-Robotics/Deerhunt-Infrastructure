'''
A blob storage class for storing, checking, and loading submissions as zip files.

For Azure Blob Storage Object Model refer to:
https://docs.microsoft.com/en-ca/azure/storage/blobs/media/storage-blobs-introduction/blob1.png
'''
import re
import zipfile
from server.config import Configuration
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

'''
- Container names must start or end with a letter or number, and can contain only letters, numbers, and the dash (-) character.
- Every dash (-) character must be immediately preceded and followed by a letter or number; consecutive dashes are not permitted in container names.
- All letters in a container name must be lowercase.
- Container names must be from 3 through 63 characters long.
'''
CONTAINER_NAME_REGEX = re.compile(
    r'^(([a-z\d]((-(?=[a-z\d]))|([a-z\d])){2,62}))$')


class BlobStorageModel:
    def __init__(self):
        self.key = Configuration.AZURE_KEY
        # Create the BlobServiceClient object
        self.service_client = BlobServiceClient.from_connection_string(
            self.key)

    def create_container(self, container_name):
        # Return false if the container name is invalid
        if not self.container_name_checker(container_name):
            return False
        try:
            container = self.service_client.create_container(container_name)
            print("Container created.")
            return container
        # Return false if the specified container already exists
        except ResourceExistsError:
            print('Specified container already exists.')
            return False

    def delete_container(self, container_name):
        # Return false if the container name is invalid
        if not self.container_name_checker(container_name):
            return False
        try:
            container_client = self.service_client.get_container_client(
                container_name)
            container_client.delete_container()
            print('Container deleted.')
            return True
        # Return false if the specified container doesn't exist
        except ResourceNotFoundError:
            print("No containers with given name")
            return False

    # Return all the blobs in the specified container
    def list_blobs_in_container(self, container_name):
        # Return false if the container name is invalid
        if not self.container_name_checker(container_name):
            return
        container = self.get_container(container_name)
        # Return false if the specified container doesn't exist
        if not container:
            return False
        return container.list_blobs()

    def get_container(self, container_name):
        container = self.service_client.get_container_client(container_name)
        if not (self.container_name_checker(container_name) and container.exists()):
            print("Invalid container name or no containers with given name")
            return False
        else:
            return container

    def container_name_checker(self, container_name):
        if re.search(CONTAINER_NAME_REGEX, container_name):
            return True
        else:
            print('Invalid container name')
            return False

    def upload_blob(self, container_name, blob_name):
        bname = blob_name.split("/")[-1]
        # Return false if the container name is invalid
        if not (self.container_name_checker(container_name) and self.get_container(container_name)):
            return False
        # Return false if the specified blob already exists
        if self.get_blob(container_name, bname):
            print("The specified blob already exists.")
            return False
        try:
            with open(blob_name,'rb') as b:
                # check if the file is a zip file
                if self.is_zip(b):
                    blob_client = self.service_client.get_blob_client(
                    container=container_name, blob=bname)
                    b = blob_client.upload_blob(b)
                    print('Blob uploaded to container.')
                    return b
                else:
                    print('File is not a zip file.')
                    return False
        except FileNotFoundError:
            print('File does not exist.')
            return False

    def delete_blob(self, container_name, blob_name):
        bname = blob_name.split("/")[-1]
        # Return false if the container name is invalid
        if not (self.container_name_checker(container_name) and self.get_container(container_name)):
            return False
        blob = self.get_blob(container_name, bname)
        if blob:
            blob.delete_blob()
            print('Blob deleted.')
            return True
        else:
            print('Specified blob doesn\'t exist')
            return False

    def get_blob(self, container_name, blob_name):
        bname = blob_name.split("/")[-1]
        container = self.get_container(container_name)
        # Return false if the container name is invalid
        if not (self.container_name_checker(container_name) and container):
            return False
        b = container.get_blob_client(bname)
        if b.exists():
            return b
        else:
            return False

    def is_zip(self, blob_file_name):
        try:
            return zipfile.is_zipfile(blob_file_name)
        except Exception as e:
            return False
