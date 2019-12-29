FROM python:3.7-alpine

RUN adduser -D lamb
USER lamb

WORKDIR /home/lamb

COPY requirements.txt ./
RUN python -m venv venv
RUN venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . ./

# run-time configuration
EXPOSE 5000
CMD [ "venv/bin/python", "-m", "flask", "run", "--host=0.0.0.0" ]
