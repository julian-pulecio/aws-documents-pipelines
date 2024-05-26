from returns.result import Success, Failure
from returns.pipeline import is_successful
from typing import Union
import json


def generate_response(result: Union[Success, Failure]) -> dict:

    if is_successful(result):
        status_code = 200
        message = result.unwrap()
    else:
        error_dict = json.loads(str(result.failure()).replace("'", "\""))
        status_code =  error_dict['error_code']
        message = error_dict['message']

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps( 
            {'message': message}
        )
    }