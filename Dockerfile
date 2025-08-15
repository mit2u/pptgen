# syntax=docker/dockerfile:1

# Base image with the specified Python version.
ARG PYTHON_VERSION=3.13.5
FROM python:${PYTHON_VERSION}-slim as base

# Prevent Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set the working directory.
WORKDIR /app


# Copy only the requirements file initially to take advantage of Docker layer caching.
COPY requirements.txt /app/requirements.txt

# Install dependencies while using the cache mount for faster builds.
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r /app/requirements.txt


# Now, copy the entire source code into the container.
COPY . .
RUN python manage.py migrate
# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
