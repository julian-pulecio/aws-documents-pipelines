from multipart import parse_form_data
from returns.result import safe
from dataclasses import dataclass
from io import BytesIO
from src.models.event import Event
from src.exceptions.bad_request_exception import BadRequestException
import magic

@dataclass
class MultiPartFile:
    file_data: BytesIO
    mime_type: str    

@dataclass
class MultiPartData:
    file: MultiPartFile
    prompt: str

@dataclass
class MultipartParser:
       
    @safe
    def extract_event_data(self, event:Event) -> MultiPartData:
        form, files = parse_form_data({
            'CONTENT_TYPE': event.headers['content-type'],
            'REQUEST_METHOD': 'POST',
            'wsgi.input': event.body
        })
        
        if 'file' not in files:
            raise BadRequestException('file not found in the event')
        
        if 'prompt' not in form:
            raise BadRequestException('prompt not found in the event')
        
        file_data:BytesIO = BytesIO(files.get('file').raw)
        
        multipart_data = MultiPartData(
            file = MultiPartFile(
                file_data = file_data,
                mime_type = magic.Magic(mime=True).from_buffer(file_data.getvalue())
            ),
            prompt = form.get('prompt')
        )
        
        return multipart_data