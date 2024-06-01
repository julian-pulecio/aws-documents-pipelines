import unittest
from returns.result import Success, Failure
from base64 import b64encode
from src.exceptions.bad_request_exception import BadRequestException
from src.models.event import Event

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.event_data = {
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': b64encode(b'{"key": "value"}').decode('utf-8')
        }

    def test_format_event_success(self):
        event = Event(self.event_data)
        formatted_event = event.format_event()
        self.assertIsInstance(formatted_event, Success)

    def test_format_event_missing_headers(self):
        invalid_event_data = self.event_data.copy()
        del invalid_event_data['headers']
        event = Event(invalid_event_data)
        result = event.format_event()
        self.assertIsInstance(result, Failure)

    def test_format_event_missing_body(self):
        invalid_event_data = self.event_data.copy()
        event = Event(invalid_event_data)
        del invalid_event_data['body']
        result = event.format_event()
        self.assertIsInstance(result, Failure)
