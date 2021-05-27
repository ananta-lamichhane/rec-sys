FROM python:3.8
ADD . /code
WORKDIR /code
ENV FLASK_APP run.py
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]