FROM python:3.9-slim-bullseye AS base

LABEL org.emqu.image.authors="gonzalezrujano@gmail.com" \
      version=$VERSION \
      description="Servicio de consulta de valores UF en el SII"

ARG VERSION

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN python3 -m venv /.venv

COPY dist/mic_serv_uf_chile-1.0.0-py3-none-any.whl /

RUN /.venv/bin/pip install mic_serv_uf_chile-1.0.0-py3-none-any.whl

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

COPY ./instance/etc/config.yml /instance/etc/config.yml
ENV MS_CONFIG=/instance/etc/config.yml

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

USER 999
EXPOSE 80/tcp
