FROM alpine
LABEL maintainer="Sebastian Serrano"
COPY . /src
WORKDIR /src
RUN apk --update add sudo && \
    apk --update add python3 py-pip openssl ca-certificates && \
    apk --update add --virtual build-dependencies \
			       python-dev libffi-dev \
			       openssl-dev build-base && \
    pip install --upgrade pip cffi && \
    pip install ansible && \

    apk del build-dependencies && \
    rm -rf /var/cache/apk/* && \

    mkdir -p /etc/ansible && \
    echo 'localhost' > /etc/ansible/hosts
CMD [ "ansible-playbook", "portfolio.yml" ]
