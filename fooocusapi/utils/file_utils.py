# -*- coding: utf-8 -*-

""" File utils

Use for managing generated files

@file: file_utils.py
@author: Konie
@update: 2024-03-22
"""
import base64
import datetime
import shutil
from io import BytesIO
import os
from pathlib import Path
import numpy as np
from PIL import Image
# import boto3
import firebase_admin
from firebase_admin import credentials, storage
import time
cred = credentials.Certificate("/workspace/Virtual AI Influencer Firebase Admin.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'virtual-ai-influencer.appspot.com'
})

def convert_to_url(local_file, cloud_file):
    bucket = storage.bucket()
    blob = bucket.blob(cloud_file)
    blob.upload_from_filename(local_file)
    # Make the blob publicly viewable
    blob.make_public()
    # Return the public URL
    return blob.public_url

from fooocusapi.utils.logger import logger


output_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../..', 'outputs', 'files'))
os.makedirs(output_dir, exist_ok=True)

STATIC_SERVER_BASE = 'http://127.0.0.1:8888/files/'


def save_output_file(
        img: np.ndarray | str,
        image_name: str = '',
        extension: str = 'png') -> str:
    """
    Save np image to file
    Args:
        img: np.ndarray image to save
        image_name: str of image name
        extension: str of image extension
    Returns:
        str of file name
    """
    current_time = datetime.datetime.now()
    date_string = current_time.strftime("%Y-%m-%d")

    filename = os.path.join(date_string, image_name + '.' + extension)
    file_path = os.path.join(output_dir, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        if isinstance(img, str):
            shutil.move(img, file_path)
        return Path(file_path).as_posix()
    except Exception:
        raise Exception


def delete_output_file(filename: str):
    """
    Delete files specified in the output directory
    Args:
        filename: str of file name
    """
    file_path = os.path.join(output_dir, filename)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        logger.std_warn(f'[Fooocus API] {filename} not exists or is not a file')
    try:
        os.remove(file_path)
        logger.std_info(f'[Fooocus API] Delete output file: {filename}')
        return True
    except OSError:
        logger.std_error(f'[Fooocus API] Delete output file failed: {filename}')
        return False


def output_file_to_base64img(filename: str | None) -> str | None:
    """
    Convert an image file to a base64 string.
    Args:
        filename: str of file name
    return: str of base64 string
    """
    if filename is None:
        return None
    file_path = os.path.join(output_dir, filename)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None

    ext = filename.split('.')[-1]
    if ext.lower() not in ['png', 'jpg', 'webp', 'jpeg']:
        ext = 'png'
    img = Image.open(file_path)
    output_buffer = BytesIO()
    img.save(output_buffer, format=ext.upper())
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return f"data:image/{ext};base64," + base64_str


def output_file_to_bytesimg(filename: str | None) -> bytes | None:
    """
    Convert an image file to a bytes string.
    Args:
        filename: str of file name
    return: bytes of image data
    """
    if filename is None:
        return None
    file_path = os.path.join(output_dir, filename)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None

    img = Image.open(file_path)
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    return byte_data


def get_file_serve_url(filename: str | None) -> str | None:
    if filename is None:
        return None
    file_path = os.path.join(output_dir, filename)
    image_name = f"users_img/generated_image_{os.urandom(4).hex()}.webp"
    # #cloud_#file_ath = f"user/user_{int(time.time())}.png"
    url = convert_to_url(file_path,image_name)
    print(url)
    #print(file_path)
    return url
    # s3_client = boto3.client('s3')
    # BUCKET_NAME = 'aipicslibrary'
    # # FOLDER_NAME = 'users/'
    # file_path = os.path.join(output_dir, filename)
    # # image_name = f"generated_image_{os.urandom(4).hex()}.webp"
    # s3_client.upload_file(file_path,BUCKET_NAME,image_name)
    # static_serve_base_url = 'https://assets.virtualfantasy.ai/'
    # print(static_serve_base_url)
    # print(file_path)
    # return static_serve_base_url + image_name
