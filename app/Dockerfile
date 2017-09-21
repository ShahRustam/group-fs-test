FROM python:2.7
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80

# run the app server
CMD ["python2.7","main.py"]
