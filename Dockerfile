FROM python:3.8.0
WORKDIR /home/user
Run pip install --upgrade pip --user
COPY requirement.txt .
RUN pip install -r requirement.txt && rm requirement.txt
RUN mkdir src
RUN mkdir data
COPY data/ data/
COPY src/ src/
WORKDIR /home/user/src
EXPOSE 5000
ENTRYPOINT [ "python", "main.py"]