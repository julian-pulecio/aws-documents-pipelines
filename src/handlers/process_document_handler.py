from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from src.models.vertex_ia import VertexIa
from src.models.multipart_parser import MultipartParser
from src.models.event import Event
import json

def process_document_handler(event, context):
    event = Event(data=event)
    multipart_parser = MultipartParser()
    vertex_ia = VertexIa(project = 'document-processor-417317', location = 'us-central1')

    result = flow(
        event.format_event(),
        bind(multipart_parser.extract_event_data),
        bind(vertex_ia.upload_request_to_vertex_ia)
    )
    
    if is_successful(result):
        status_code = 200
        message = result.unwrap()
    else:
        status_code = 500
        message = str(result.failure())

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps( 
            {'message': message}
        )
    }
    
    