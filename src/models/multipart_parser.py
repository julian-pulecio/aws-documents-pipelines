from botocore.exceptions import ClientError
from multipart import parse_form_data
from returns.result import safe
from dataclasses import dataclass
from base64 import b64decode
from io import BytesIO

from returns.result import Success
from returns.pipeline import flow, is_successful
from returns.pointfree import bind
import magic

from src.models.event import Event

@dataclass
class MultipartParser:   
    @safe
    def extract_event_data(self, event:Event):
        form, files = parse_form_data({
            'CONTENT_TYPE': event.headers['content-type'],
            'REQUEST_METHOD': 'POST',
            'wsgi.input': event.body
        })
        
        if 'file' not in files:
            raise Exception('not file found in the event')
        
        file_data = BytesIO(files.get('file').raw)
        
        multipart_data = MultiPartData(
            file = MultiPartFile(
                file_data = file_data,
                mime_type = magic.Magic(mime=True).from_buffer(file_data.getvalue())
            ),
            form = dict(form)
        )
        
        return multipart_data

@dataclass
class MultiPartFile:
    file_data: BytesIO
    mime_type: str    

@dataclass
class MultiPartData:
    file: MultiPartFile
    form: dict