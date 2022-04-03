FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --requirement requirements.txt

COPY . .

EXPOSE 5010

ENTRYPOINT [ "python3" ]

CMD [ "routes.py" ]

#docker run -p 80:5000 ing-soft-back
#docker build -t ing-soft-back .    
