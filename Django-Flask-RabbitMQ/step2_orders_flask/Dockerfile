# в качестве родительского образа используем худенький image пайтона содержит минимум:
FROM python:3-slim

# ENV used to set environment variables:
ENV PYTHONUNBUFFERED=1

# sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions:
WORKDIR /my_app

# copy files or dir from <src> and adds them to the filesystem of the container at the path <dest>:
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

