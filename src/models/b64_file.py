from io import BytesIO
from base64 import b64decode
from binascii import hexlify
from dataclasses import dataclass

@dataclass
class B64File:
    b64_str: str    

    def convert_b64_file_to_bytes(self) -> BytesIO:
        decoded_file = b64decode(self.b64_str)
        bytes_file = BytesIO(decoded_file)
        return bytes_file

    def guess_file_mime_type(self) -> str:
        byte_data = b64decode(self.b64_str[:24])
        hex_data = hexlify(byte_data).decode('utf-8')
        file_signatures = {
            '89504e47': 'image/png',
            'ffd8ff': 'image/jpeg',
            '25504446': 'application/pdf',
        }
        for signature, extension in file_signatures.items():
            if hex_data.startswith(signature):
                return extension

        return False