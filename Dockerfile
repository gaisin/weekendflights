FROM python:3.7
ADD . /wf
WORKDIR /wf
RUN pip install -r requirements.txt \
    && pip install .
