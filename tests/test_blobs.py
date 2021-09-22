import server.Managers.Blobs.BlobStorage
from azure.storage.blob import BlobClient, ContainerClient
import time

# Blob storage model instance to be used in all functions
model = server.Managers.Blobs.BlobStorage.BlobStorageModel()
# Create two containers: dh1 and dh2
# TThis function is called to avoid duplicate code
def create_dh1_dh2():
    if not model.get_container("dh1"):
        model.create_container("dh1")
    if not model.get_container("dh2"):
        model.create_container("dh2")

def test_create_container():
    # The specified container doesn't exist
    assert type(model.create_container("dh1")) is ContainerClient
    assert type(model.create_container("dh2")) is ContainerClient
    time.sleep(10)
    # When sthe pecified container does already exist
    assert model.create_container("dh1") == False
    assert model.create_container("dh2") == False
    # Checking if dh1 is created correctly
    dh1 = model.get_container("dh1")
    assert type(dh1) is ContainerClient
    assert dh1.container_name == "dh1"
    # Checking if dh2 is created correctly
    dh2 = model.get_container("dh2")
    assert type(dh2) is ContainerClient
    assert dh2.container_name == "dh2"



def test_delete_container():
    create_dh1_dh2()
    time.sleep(10)
    # The specified container doesn't exist
    assert model.delete_container("dh3") == False
    # The specified container does exist
    assert model.delete_container("dh1") == True
    time.sleep(10)
    # Container dh3 still doesn't exist
    assert model.get_container("dh3") == False
    # Container dh1 doesn't exist anymore
    assert model.get_container("dh1") == False


'''
def test_list_blobs_in_container():
    create_dh1_dh2()
    model.upload_blob("dh1", "blob_test_files/blobx.zip")
    model.upload_blob("dh1", "blob_test_files/bloby.zip")
    model.upload_blob("dh1", "blob_test_files/blobz.zip")
    model.upload_blob("dh1", "blob_test_files/blobq.zip")
'''


def test_get_container():
    create_dh1_dh2()
    time.sleep(10)
    # The specified container does exist
    dh1 = model.get_container("dh1")
    assert type(dh1) is ContainerClient
    assert dh1.container_name == "dh1"
    dh2 = model.get_container("dh2")
    assert type(dh2) is ContainerClient
    assert dh2.container_name == "dh2"
    # Clean up
    model.delete_container("dh1")
    model.delete_container("dh2")
    # The specified container doesn't exist
    assert model.get_container("dh3") == False

def test_container_name_checker():
    '''
    - Container names must start or end with a letter or number, and can contain only letters, numbers, and the dash (-) character.
    - Every dash (-) character must be immediately preceded and followed by a letter or number; consecutive dashes are not permitted in container names.
    - All letters in a container name must be lowercase.
    - Container names must be from 3 through 63 characters long.
    '''
    # Consecutive dashes are not allowed
    assert model.container_name_checker("consecutive--dashes") == False
    # Container names must be minimum 2 characters
    assert model.container_name_checker("dh") == False
    # Container names can end and start with a number
    assert model.container_name_checker("dh1") == True
    assert model.container_name_checker("1dh") == True
    # Every dash must be followed by a number or letter
    assert model.container_name_checker("ends-with-dash-") == False
    assert model.container_name_checker("-starts-with-dash") == False
    # Container can contain only letters, numbers and the dash
    assert model.container_name_checker("includes!non_dash") == False
    # Container names must be lowercase
    assert model.container_name_checker("UPPER_CASE") == False


def test_upload_blob():
    # The specified blob is not already uploaded
    model.upload_blob("dh7", "blob_test_files/blob1.zip")
    assert model.get_blob("dh7", "blob_test_files/blob1.zip").container_name == "dh7"
    # When file type is invalid
    assert model.upload_blob("dh7", "blob_test_files/blob2.txt") == False
    # The specified blob is already uploaded
    assert model.upload_blob("dh7", "blob_test_files/blob1.zip") == False
    # Clean up
    model.delete_blob("dh7", "blob_test_files/blob1.zip")


def test_delete_blob():
    model.upload_blob("dh7", "blob_test_files/blob1.zip")
    time.sleep(10)
    # THe specified blob does exist
    model.delete_blob("dh7", "blob_test_files/blob1.zip")
    time.sleep(10)
    assert model.get_blob("dh7", "blob_test_files/blob1.zip") == False
    # The specified blob doesn't exist
    assert model.delete_blob("dh7", "blob_test_files/blob4.zip") == False


def test_get_blob():
    model.upload_blob("dh7", "blob_test_files/blobx.zip")
    # THe specified blob does exist
    bx = model.get_blob("dh7", "blob_test_files/blobx.zip")
    assert type(bx) is BlobClient
    # THe specified blob doesn't exist
    assert model.get_blob("dh7", "blob_test_files/bloby.zip") == False
    model.upload_blob("dh7", "blob_test_files/bloby.zip")
    time.sleep(10)
    by = model.get_blob("dh7", "blob_test_files/bloby.zip")
    assert type(by) is BlobClient
    # Clean up
    model.delete_blob("dh7", "blob_test_files/blobx.zip")
    model.delete_blob("dh7", "blob_test_files/bloby.zip")
