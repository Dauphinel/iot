# Use official Spark image
FROM apache/spark:3.5.0

# Switch to root to install packages
USER root

# Create directories and set permissions
RUN mkdir -p /home/spark/.ivy2/cache && \
    mkdir -p /home/spark/.ivy2/jars && \
    mkdir -p /opt/spark/notebooks && \
    mkdir -p /tmp/spark-events

# Install Python packages
RUN pip install --no-cache-dir \
    kafka-python==2.0.2 \
    influxdb==5.3.1 \
    pandas==2.0.3 \
    numpy==1.24.3 \
    requests==2.31.0 \
    pyspark

# Download required JARs
RUN cd /opt/spark/jars && \
    wget -q https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar && \
    wget -q https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.0/kafka-clients-3.4.0.jar && \
    wget -q https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.0/spark-token-provider-kafka-0-10_2.12-3.5.0.jar && \
    wget -q https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar

# Set proper permissions
RUN chown -R spark:spark /home/spark && \
    chown -R spark:spark /opt/spark && \
    chmod -R 755 /home/spark && \
    chmod -R 755 /opt/spark && \
    chmod -R 777 /tmp

# Switch back to spark user
USER spark

# Set working directory
WORKDIR /opt/spark

# Environment variables
ENV SPARK_HOME=/opt/spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
ENV SPARK_LOCAL_DIRS=/tmp/spark-local
ENV SPARK_WORKER_DIR=/tmp/spark-worker

# Expose ports
EXPOSE 8888 4040

# Default command
CMD ["python3"]