# Use the official Python 3.12 image
FROM python:3.12

ENV PYTHONUNBUFFERED=1

ARG WORKDIR=/wd
ARG USER=user
ARG UID=1000

WORKDIR ${WORKDIR}

# Add system user
RUN useradd --system ${USER} --uid=${UID} && \
    chown --recursive ${USER} ${WORKDIR}

# Update and upgrade system packages
RUN apt update && apt upgrade -y

# Copy and install Python dependencies
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

# Copy entrypoint and start scripts
COPY --chmod=755 ./docker/app/entrypoint.sh /entrypoint.sh
COPY --chmod=755 ./docker/app/start.sh /start.sh

# Copy project files
COPY ./Makefile Makefile
COPY ./manage.py manage.py
COPY core ./core/
COPY ./apps ./apps/

# Switch to unprivileged user
USER ${USER}

# Define default command
ENTRYPOINT ["/entrypoint.sh"]

# Define volume (optional)
VOLUME ${WORKDIR}/db

# Expose default Django port
EXPOSE 8000