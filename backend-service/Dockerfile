# syntax=docker/dockerfile:1

ARG USER="ionos"

FROM python:3.9

ARG USER

# make python use the system CA bundle
ENV REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"
ENV PIP_INDEX_URL="https://pypi.org/simple"

# create user
RUN useradd -U -ms /bin/bash -u 15004 ${USER}

# copy data
COPY Pipfile home/${USER}/code/
COPY Pipfile.lock home/${USER}/code/
COPY config.yml home/${USER}/code/
COPY src/ home/${USER}/code/src/
# changing work directory
WORKDIR /home/${USER}/code/

#setting path environment
ENV PATH /home/${USER}/.local/bin:${PATH}
RUN echo ${PATH}
# install python packages
RUN pip install pipenv 
RUN pipenv install --dev --deploy

CMD ["pipenv", "run", "python", "-m", "uvicorn", "src.service:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000 5432