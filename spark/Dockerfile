FROM apache/spark:3.4.1

USER root

# Télécharger le connecteur Kafka pour Spark 3.4 compatible avec Scala 2.12
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.4.1/spark-sql-kafka-0-10_2.12-3.4.1.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.2.0/kafka-clients-3.2.0.jar /opt/spark/jars/

# Installer Python packages
RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install requests pyspark kafka-python influxdb

WORKDIR /app
COPY spark_streaming.py .

CMD ["python3", "spark_streaming.py"]
