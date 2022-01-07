FROM image-registry.openshift-image-registry.svc:5000/openshift/python:latest

WORKDIR /opt/app-root/src
COPY . /opt/app-root/src

RUN chmod 666 /opt/app-root/src/logs && \
    pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "./app.py"]
