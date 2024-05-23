from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from src.models.b64_file import B64File
from src.models.vertex_ia import VertexIa
from src.models.multipart_parser import MultipartParser
from returns.result import safe
import json

def lambda_handler(event, context):
    multipart_parser = MultipartParser(event=event)
    vertex_ia = VertexIa(project = 'document-processor-417317', location = 'us-central1')

    result = flow(
        multipart_parser.extract_event_data(),
        bind(lambda _:vertex_ia.upload_request_to_vertex_ia(multipart_parser)), 
    )
    print(result)
    print(multipart_parser.mime_type)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps( 
            {'message': result.unwrap()}
        )
    }
    
    