# python3.9 lambda base image. 
# Python version can be changed depending on your own version
FROM public.ecr.aws/lambda/python:3.9

# copy requirements.txt to container root directory
COPY requirements.txt ./

# installing dependencies from the requirements under the root directory
RUN pip3 install -r ./requirements.txt

# Copy function code to container
COPY lambda_function.py ./

COPY document-processor-417317-fd90cd5558b7.json ./

# setting the CMD to your handler file_name.function_name
CMD [ "lambda_function.lambda_handler" ]