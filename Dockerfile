FROM image-registry.openshift-image-registry.svc:5000/openshift/python:latest

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "./app.py"]
