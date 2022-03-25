FROM registry.access.redhat.com/ubi8/python-36

WORKDIR /opt/app-root/src
COPY --chown=default:root . /opt/app-root/src

## ppc64le need hdf5-devel for tensorflow
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm && \
    yum -y install hdf5-devel && \
    yum -y clean all --enablerepo='*'

# ppc64le h5py build needs Cython first
RUN chmod 775 /opt/app-root/src/logs && \
    pip install Cython==0.29.28 && \
    pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "./app.py"]
