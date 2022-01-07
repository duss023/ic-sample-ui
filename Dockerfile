FROM image-registry.openshift-image-registry.svc:5000/openshift/python:latest

COPY . /opt/app-root/src
WORKDIR /opt/app-root/src

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "./app.py"]
