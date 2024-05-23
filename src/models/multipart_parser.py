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


@dataclass
class MultipartParser:
    event: dict

    @safe
    def extract_event_data(self):
        result = flow(
            self.__init_headers(),
            bind(lambda _: self.__init_body()),
            bind(lambda _: self.__init_data()),
        )
        if not is_successful(result):
            raise Exception(str(result.failure()))
        
        return self
   
    @safe
    def __init_headers(self):
        if 'headers' not in self.event:
            raise Exception('not headers found in the event')
        self.headers = {k.lower():v for k,v in self.event['headers'].items()}

        return True
    
    @safe
    def __init_body(self):
        if 'body' not in self.event:
            raise Exception('not body found in the event')
        self.body = BytesIO(b64decode(self.event['body']))
        
        return True
    
    @safe
    def __init_data(self):
        form, files = parse_form_data({
            'CONTENT_TYPE': self.headers['content-type'],
            'REQUEST_METHOD': 'POST',
            'wsgi.input': self.body
        })
        self.form = dict(form)
        if 'file' not in files:
            raise Exception('not file found in the event')
        self.files = BytesIO(files.get('file').raw)
        self.mime_type = magic.Magic(mime=True).from_buffer(self.files.getvalue())
        
        return True