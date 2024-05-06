from PIL import Image, ImageDraw
import base64
import io
from io import BytesIO
import boto3
import argparse
import json

import vertexai
from vertexai.preview.vision_models import ImageTextModel

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

import binascii
import calendar;
import time;

def lambda_handler(event, context): 
    bytes_file = convert_b64_file_to_bytes(event)
    mime_type = guess_file_mime_type(event['body'])
    if not mime_type:
        response = {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(
                {'message':'Hello from Lambda!'}
            )
        }
        return response
    
    # upload_file_to_s3(bytes_file, mime_type)

    result = upload_request_to_vertex_ia(bytes_file, mime_type, 'What is in this image?')

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(
            {'message': result}
        )
    }
    
    return response

def convert_b64_file_to_bytes(event):
    decoded_file = base64.b64decode(event['body'])
    bytes_file = BytesIO(decoded_file)
    return bytes_file

def upload_file_to_s3(bytes_file: BytesIO, mime_type: str):

    format = mime_type[len(mime_type)-3:len(mime_type)]

    temp_image = Image.open(bytes_file) 
    image_bytes = BytesIO()
    temp_image.save(image_bytes, format= format)

    image_bytes.seek(0)

    s3_client = boto3.client('s3')

    gmt = time.gmtime()
    ts = calendar.timegm(gmt)

    bucket_name = 'document-manager-20032024'  # Make sure to replace this with your bucket name
    object_name = str(ts) + '.' + format  # This is the name the file will have in S3

    s3_client.upload_fileobj(image_bytes, bucket_name, object_name)
    return bytes_file

def upload_request_to_vertex_ia(bytes_file: BytesIO, mime_type: str,prompt: str):
    credentials = Credentials.from_service_account_file('document-processor-417317-fd90cd5558b7.json', scopes=['https://www.googleapis.com/auth/cloud-platform'])

    if credentials.expired:
        credentials.refresh(Request())
   
    file = Part.from_data(
        data = bytes_file.getvalue(),
        mime_type = mime_type
    )

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    vertexai.init(project="document-processor-417317", location="us-central1", credentials = credentials)
    model = GenerativeModel("gemini-1.5-pro-preview-0409")
    responses = model.generate_content(
        [file, prompt],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    result = ''
    for response in responses:
        result += response.text
    print(result)
    return result

def guess_file_mime_type(encoded_str):
    byte_data = base64.b64decode(encoded_str[:24])  # Only decode some initial characters

    hex_data = binascii.hexlify(byte_data).decode('utf-8')

    file_signatures = {
        '89504e47': 'image/png',
        'ffd8ff': 'image/jpeg',
        '25504446': 'application/pdf',
    }

    for signature, extension in file_signatures.items():
        if hex_data.startswith(signature):
            return extension

    return False