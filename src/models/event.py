from returns.result import safe
from dataclasses import dataclass
from base64 import b64decode
from io import BytesIO
from returns.pipeline import flow, is_successful
from returns.pointfree import bind


@dataclass
class Event:
    data: dict

    @safe
    def format_event(self):
        result = flow(
            self.__init_headers(),
            bind(lambda _: self.__init_body()),
        )
        if not is_successful(result):
            raise Exception(str(result.failure()))
        
        return result.unwrap()


    @safe
    def __init_headers(self):
        if 'headers' not in self.data:
            raise Exception('not headers found in the event')
        self.headers = {k.lower():v for k,v in self.data['headers'].items()}

        return self
    
    @safe
    def __init_body(self):
        if 'body' not in self.data:
            raise Exception('not body found in the event')
        self.body = BytesIO(b64decode(self.data['body']))
        
        return self
