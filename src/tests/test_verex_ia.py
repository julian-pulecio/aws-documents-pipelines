import unittest
from unittest.mock import patch, MagicMock
from unittest.mock import Mock
from returns.result import Failure

from multipart import MultiDict
from src.models.multipart_parser import MultiPartFile
from src.models.vertex_ia import VertexIa
from src.exceptions.bad_request_exception import BadRequestException
from src.models.event import Event

import io
from vertexai.generative_models import GenerativeModel

from vertexai.generative_models import Part

class TestVertexIA(unittest.TestCase):
    def setUp(self):
        self.multi_part_data = MagicMock()
        self.multi_part_data.file =  MultiPartFile(
            file_data=io.BytesIO(b'some-data'),
            mime_type='image/jpeg'
        )
        self.multi_part_data.prompt = 'what is in this image?'
        self.vertexia = VertexIa(
            project = 'document-processor-417317', location = 'us-central1'
        )
    
    @patch('vertexai.generative_models.GenerativeModel.generate_content')
    def test_upload_request_to_vertex_ia(self, mock_generate_content):
        self.vertexia.upload_request_to_vertex_ia(self.multi_part_data)
        mock_generate_content.assert_called_once()