from dataclasses import dataclass
from base64 import b64decode
from io import BytesIO
from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from returns.result import safe, Result
from typing_extensions import Self
from src.exceptions.bad_request_exception import BadRequestException


@dataclass
class Event:
    data: dict

    @safe
    def format_event(self) -> str:
        result:Result = flow(
            self.__init_headers(),
            bind(lambda _: self.__init_body()),
        )
        if not is_successful(result):
            raise Exception(str(result.failure()))
        
        return result.unwrap()


    @safe
    def __init_headers(self) -> Self:
        if 'headers' not in self.data:
            raise BadRequestException('not headers found in the event')
        self.headers:dict = {k.lower():v for k,v in self.data['headers'].items()}

        return self
    
    @safe
    def __init_body(self) -> Self:
        if 'body' not in self.data:
            raise BadRequestException('not body found in the event')
        self.body:BytesIO = BytesIO(b64decode(self.data['body']))
        
        return self
