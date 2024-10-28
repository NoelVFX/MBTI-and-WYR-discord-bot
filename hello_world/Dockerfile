FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt ./

RUN python3.10 -m pip install -r requirements.txt -t .

COPY app.py ./
COPY Save.py ./

COPY test.json ${LAMBDA_TASK_ROOT}/
# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
