import vertexai.preview.generative_models as generative_models
import vertexai
from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import GenerationResponse
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from typing import Union, Iterable, Optional
from dataclasses import dataclass
from returns.result import safe
from src.models.multipart_parser import MultiPartData


@dataclass
class VertexIa:
    project:str
    location:str


    def __post_init__(self) -> None:
        self.credentials:Credentials = Credentials.from_service_account_file(
            filename ='document-processor-417317-fd90cd5558b7.json',
            scopes = ['https://www.googleapis.com/auth/cloud-platform']
        )
        
        self.safety_settings:dict = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

        self.generation_config:dict = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        }
        
        vertexai.init(
            project=self.project,
            location=self.location,
            credentials=self.credentials
        )
    
    @safe
    def upload_request_to_vertex_ia(self, multipart_data:MultiPartData) -> str:
        if self.credentials.expired:
            self.credentials.refresh(Request())
   
        file:Part = Part.from_data(
            data = multipart_data.file.file_data.getvalue(),
            mime_type = multipart_data.file.mime_type
        )

        model:GenerativeModel = GenerativeModel("gemini-1.5-pro-preview-0409")
        responses:Union[GenerationResponse, Iterable[GenerationResponse]] = model.generate_content(
            [file, multipart_data.prompt],
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            stream=True,
        )

        result = ''
        for response in responses:
            result += response.text
                                                     
        return result




