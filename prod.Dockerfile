FROM postgres:16.4

WORKDIR /data-model/

# Copy requirements files and schema
COPY ./requirements/build.in ./schema/ /data-model/
