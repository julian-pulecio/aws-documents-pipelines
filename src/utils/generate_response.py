from returns.result import Success, Failure
from returns.pipeline import is_successful
from typing import Union
import json


def generate_response(result: Union[Success, Failure]) -> dict:

    if is_successful(result):
        status_code, message = handle_success(result)
    else:
        status_code, message = handle_failure(result)

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps( 
            {'message': message}
        )
    }

def handle_success(result: Success):
    return 200, result.unwrap()

def handle_failure(result: Failure):
    print(result)
    error_dict = json.loads(str(result.failure()).replace("'", "\""))
    if 'error_code' not in error_dict:
        return 500, error_dict['message']
    return error_dict['error_code'], error_dict['message']