'''
A blob storage class for storing, checking, and loading submissions as zip files.

For Azure Blob Storage Object Model refer to:
https://docs.microsoft.com/en-ca/azure/storage/blobs/media/storage-blobs-introduction/blob1.png
'''
import os
import re
import zipfile
from server.config import Configuration
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

'''
- Container names must start or end with a letter or number, and can contain only letters, numbers, and the dash (-) character.
- Every dash (-) character must be immediately preceded and followed by a letter or number; consecutive dashes are not permitted in container names.
- All letters in a container name must be lowercase.
- Container names must be from 3 through 63 characters long.
'''
CONTAINER_NAME_REGEX = re.compile(r'^(([a-z\d]((-(?=[a-z\d]))|([a-z\d])){2,62}))$')

class BlobStorageModel:
    def __init__(self):
        self.key = Configuration.AZURE_KEY
        # Create the BlobServiceClient object
        self.service_client = BlobServiceClient.from_connection_string(self.key)

    def create_container(self, container_name):
        if not self.container_name_checker(container_name):
            return 
        try:
            container = self.service_client.create_container(container_name)
            print("Container created.")
            return container
        except ResourceExistsError:
            print('Specified container already exists.')
            pass

    def delete_container(self, container_name):
        if not self.container_name_checker(container_name):
            return
        try:
            container_client = self.service_client.get_container_client(container_name)
            container_client.delete_container()
            print('Container deleted.')
        except ResourceNotFoundError:
            print("No containers with given name")
            pass

    # Return all the blobs in the container with the given name
    def list_blobs_in_container(self, container_name):
        if not self.container_name_checker(container_name):
            return
        container = self.get_container(container_name)
        if not container:
            return
        return container.list_blobs()

    def get_container(self, container_name):
        if not self.container_name_checker(container_name):
            print("No containers with given name")
            return
        return self.service_client.get_container_client(container_name)

    def container_name_checker(self, container_name):
        if re.search(CONTAINER_NAME_REGEX, container_name):
            return True
        else: 
            print('Invalid container name')
            return False

    def upload_blob(self, container_name, blob_name):
        if not self.container_name_checker(container_name):
            return
        # check if the file is a zip file
        if self.is_zip(blob_name):
            blob_client = self.service_client.get_blob_client(
                container=container_name, blob=blob_name)
            try:
                with open(blob_name,'rb') as b:
                    blob_client.upload_blob(b)
                print('Blob uploaded to container.')
            except FileNotFoundError: 
                print('File does not exist.')
        else:
            raise FileExtensionError
        
    def delete_blob(self, container_name, blob_name):
        try:
            blob = self.get_blob(container_name, blob_name)
            blob.delete_blob()
            print('Blob deleted.')
        except ResourceNotFoundError as e:
            print('Specified blob doesn\'t exist')

    def get_blob(self, container_name, blob_name):
        container = self.get_container(container_name)
        return container.get_blob_client(blob_name)

    def is_zip(self, blob_file_name):
        try:
            return zipfile.is_zipfile(blob_file_name)
        except Exception as e:
            return False


class FileExtensionError(Exception):
    pass


