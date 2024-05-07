import vertexai.preview.generative_models as generative_models
import vertexai

from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

from dataclasses import dataclass
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from io import BytesIO



@dataclass
class VertexIa:
    project: str
    location: str
    credentials: Credentials = None
    safety_settings: dict = None
    generation_config:dict = None


    def __post_init__(self):
        self.credentials = Credentials.from_service_account_file(
            filename ='document-processor-417317-fd90cd5558b7.json',
            scopes = ['https://www.googleapis.com/auth/cloud-platform'])
        
        self.safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

        self.generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        }
        
        vertexai.init(project="document-processor-417317", location="us-central1", credentials = self.credentials)
    

    def upload_request_to_vertex_ia(self, bytes_file: BytesIO, mime_type: str,prompt: str) -> str:
        if self.credentials.expired:
            self.credentials.refresh(Request())
   
        file = Part.from_data(
            data = bytes_file.getvalue(),
            mime_type = mime_type
        )

        model = GenerativeModel("gemini-1.5-pro-preview-0409")
        responses = model.generate_content(
            [file, prompt],
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            stream=True,
        )

        result = ''
        for response in responses:
            result += response.text
                                                     
        return result




