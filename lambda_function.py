import json
from src.models.b64_file import B64File
from src.models.vertex_ia import VertexIa

def lambda_handler(event, context):

    b64_file = B64File(b64_str=event['body'])
    vertex_ia = VertexIa(project = 'document-processor-417317', location = 'us-central1')
    mime_type = b64_file.guess_file_mime_type()
    result = vertex_ia.upload_request_to_vertex_ia(
        bytes_file=b64_file.convert_b64_file_to_bytes(),
        mime_type=mime_type,
        prompt='what is in this image?'
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