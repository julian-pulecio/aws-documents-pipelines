from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import Result
from src.utils.generate_response import generate_response
from src.models.vertex_ia import VertexIa
from src.models.multipart_parser import MultipartParser
from src.models.event import Event
import base64


def process_document_handler(event_dict:dict, context:dict):
    event:Event = Event(data=event_dict)
    multipart_parser:MultipartParser = MultipartParser()
    vertex_ia:VertexIa = VertexIa(project = 'document-processor-417317', location = 'us-central1')

    result:Result = flow(
        event.format_event(),
        bind(multipart_parser.extract_event_data),
        bind(vertex_ia.upload_request_to_vertex_ia)
    )

    return generate_response(result = result)
    