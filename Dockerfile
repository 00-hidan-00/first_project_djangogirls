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

# Create logs and media directories with correct permissions
RUN mkdir -p /wd/logs /wd/media && chown -R ${USER}:${USER} /wd/logs /wd/media

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
COPY ./core ./core/
COPY ./apps ./apps/

# Switch to unprivileged user
USER ${USER}

# Set the container's entrypoint to prepare the environment
ENTRYPOINT ["/entrypoint.sh"]

# Define the default command to start the application
CMD ["/start.sh"]

# Persist user-uploaded media files
VOLUME ${WORKDIR}/media

# Expose default Django port
EXPOSE 8000