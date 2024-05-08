FROM python:3.13.0a4
WORKDIR /app
COPY . .
# RUN pip install -r requirements.txt
CMD ["python", "-u","./nexusguard.py"]


#docker image rm -f nexusguard; docker build --tag nexusguard .
#docker run -d --restart unless-stopped nexusguard