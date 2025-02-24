FROM pdf2htmlex/pdf2htmlex:0.18.8.rc2-master-20200820-ubuntu-20.04-x86_64

RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

# Set the entrypoint to run the Flask app with Gunicorn
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
