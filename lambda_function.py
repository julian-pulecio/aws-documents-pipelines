import json
import re
from src.models.b64_file import B64File
from src.models.vertex_ia import VertexIa
import base64
from io import BytesIO
from multipart import parse_form_data


def lambda_handler(event, context):
    
    headers = {k.lower():v for k,v in event['headers'].items()}
    body = base64.b64decode(event['body'])

    environ = {
        'CONTENT_TYPE': headers['content-type'],
        'REQUEST_METHOD': 'POST',
        'wsgi.input': BytesIO(body)
    }
    form, files = parse_form_data(environ)

    # Example usage...
    form_data = dict(form)
    print(form_data)

    file = BytesIO(files.get('file').raw)

    vertex_ia = VertexIa(project = 'document-processor-417317', location = 'us-central1')
    mime_type = 'image/png'
    result = vertex_ia.upload_request_to_vertex_ia(
        bytes_file=file,
        mime_type=mime_type,
        prompt=form_data['prompt']
    ) 
    
    if not mime_type:
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps( 
                {'message': 'NOT VALID'}
            )
        }

    else:
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