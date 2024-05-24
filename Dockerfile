# python3.9 lambda base image. 
# Python version can be changed depending on your own version
FROM public.ecr.aws/lambda/python:3.9

# copy requirements.txt to container root directory
COPY requirements.txt ./

# installing dependencies from the requirements under the root directory
RUN pip3 install -r ./requirements.txt

RUN mkdir ./src

ADD src ./src

COPY ./src/handlers/process_document_handler.py ./

COPY document-processor-417317-fd90cd5558b7.json ./

# setting the CMD to your handler file_name.function_name

CMD [ "process_document_handler.process_document_handler" ]