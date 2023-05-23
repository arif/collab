# syntax=docker/dockerfile:1.0-experimental

FROM lambci/lambda:build-python3.8

COPY ./requirements.txt .

RUN python -m venv /ve && \
    source /ve/bin/activate && \
    pip install -r requirements.txt

RUN echo 'export PS1="\[\e[36m\]λ.shell>\[\e[m\] "' >> /root/.bashrc

COPY ./lambda/entrypoint /entrypoint
ENTRYPOINT ["/entrypoint"]
