FROM image-registry.openshift-image-registry.svc:5000/openshift/python:latest

WORKDIR /opt/app-root/src
COPY --chown=default:root . /opt/app-root/src

RUN pip install flask

EXPOSE 8080

CMD ["python", "./app.py"]
