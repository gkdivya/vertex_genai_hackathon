#########################################################
### THIS IS FOR LOCAL DEVELOPMENT NOT FOR PRODUCTIOPN ###
#########################################################
# Step 1: Use official lightweight Python image as base OS.
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV GOOGLE_APPLICATION_CREDENTIALS="/usr/src/app/serviceAccount.json"
ENV SENTRY_SDK_DSN="https://36508a31dbb3468994b7ae470704ce10@o718840.ingest.sentry.io/5783806"
ENV PATH /usr/local/bin:$PATH

WORKDIR pdf2jsonl
RUN curl -fsSLO --compressed "https://nodejs.org/dist/v14.17.1/node-v14.17.1-linux-x64.tar.xz" \
    && tar -xJf "node-v14.17.1-linux-x64.tar.xz" -C /usr/local --strip-components=1 --no-same-owner \
    && rm "node-v14.17.1-linux-x64.tar.xz" \
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs



WORKDIR ..
# Step 3. Install production dependencies.
RUN pip install -r requirements.txt
