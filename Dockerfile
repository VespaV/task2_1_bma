FROM python:3
WORKDIR /usr/src/app
COPY / ./
RUN apt-get update && apt-get install -y bedtools bwa  && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
CMD ["bash"]