FROM python:3.9
RUN apt-get update && apt-get install -y python3-tk x11-apps
WORKDIR /app
COPY /app
ENV DISPLAY=0:
CMD["python","Loans.py"]


