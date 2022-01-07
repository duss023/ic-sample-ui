FROM image-registry.openshift-image-registry.svc:5000/openshift/python:latest

WORKDIR /opt/app-root/src
COPY . /opt/app-root/src
RUN chown -R :0 /opt/app-root/src

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "./app.py"]
