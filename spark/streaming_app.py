#!/usr/bin/env python3

import os
import json
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from influxdb import InfluxDBClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_spark_session():
    """Create Spark session with Kafka packages"""
    return SparkSession.builder \
        .appName("IoT-Kafka-Streaming") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.driver.memory", "1g") \
        .config("spark.executor.memory", "1g") \
        .getOrCreate()

def get_kafka_stream(spark):
    """Create Kafka streaming DataFrame"""
    return spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "iot-sensors") \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .load()

def parse_iot_data(df):
    """Parse IoT sensor data from Kafka messages"""
    
    # Define schema for IoT sensor data
    iot_schema = StructType([
        StructField("device_id", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("humidity", DoubleType(), True),
        StructField("pressure", DoubleType(), True),
        StructField("air_quality", DoubleType(), True),
        StructField("light", DoubleType(), True),
        StructField("sound_level", DoubleType(), True),
        StructField("co2", DoubleType(), True),
        StructField("motion", IntegerType(), True),
        StructField("battery_level", DoubleType(), True),
        StructField("location", StringType(), True)
    ])
    
    # Parse JSON from Kafka value
    parsed_df = df.select(
        col("key").cast("string"),
        from_json(col("value").cast("string"), iot_schema).alias("data"),
        col("timestamp").alias("kafka_timestamp")
    ).select("data.*", "kafka_timestamp")
    
    return parsed_df

def write_to_influxdb(df, epoch_id):
    """Write batch data to InfluxDB"""
    try:
        # Convert to Pandas DataFrame
        pandas_df = df.toPandas()
        
        if pandas_df.empty:
            logger.info(f"Batch {epoch_id}: No data to write")
            return
        
        # Connect to InfluxDB
        client = InfluxDBClient(host='influxdb', port=8086, database='iot_data')
        
        # Prepare data points for InfluxDB
        points = []
        for _, row in pandas_df.iterrows():
            point = {
                "measurement": "iot_data",
                "tags": {
                    "device_id": row.get('device_id', 'unknown'),
                    "location": row.get('location', 'unknown')
                },
                "time": row.get('timestamp', row.get('kafka_timestamp')),
                "fields": {
                    "temperature": float(row.get('temperature', 0)) if row.get('temperature') is not None else None,
                    "humidity": float(row.get('humidity', 0)) if row.get('humidity') is not None else None,
                    "pressure": float(row.get('pressure', 0)) if row.get('pressure') is not None else None,
                    "air_quality": float(row.get('air_quality', 0)) if row.get('air_quality') is not None else None,
                    "light": float(row.get('light', 0)) if row.get('light') is not None else None,
                    "sound_level": float(row.get('sound_level', 0)) if row.get('sound_level') is not None else None,
                    "co2": float(row.get('co2', 0)) if row.get('co2') is not None else None,
                    "motion": int(row.get('motion', 0)) if row.get('motion') is not None else None,
                    "battery_level": float(row.get('battery_level', 0)) if row.get('battery_level') is not None else None
                }
            }
            
            # Remove None fields
            point["fields"] = {k: v for k, v in point["fields"].items() if v is not None}
            
            if point["fields"]:  # Only add if there are valid fields
                points.append(point)
        
        if points:
            client.write_points(points)
            logger.info(f"Batch {epoch_id}: Successfully wrote {len(points)} points to InfluxDB")
        else:
            logger.info(f"Batch {epoch_id}: No valid data points to write")
            
        client.close()
        
    except Exception as e:
        logger.error(f"Batch {epoch_id}: Error writing to InfluxDB: {str(e)}")

def main():
    """Main streaming application"""
    logger.info("Starting IoT Kafka Streaming Application")
    
    # Create Spark session
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    try:
        # Create Kafka stream
        kafka_df = get_kafka_stream(spark)
        
        # Parse IoT data
        iot_df = parse_iot_data(kafka_df)
        
        # Add processing timestamp
        processed_df = iot_df.withColumn("processed_time", current_timestamp())
        
        # Write to InfluxDB using foreachBatch
        query = processed_df.writeStream \
            .foreachBatch(write_to_influxdb) \
            .outputMode("append") \
            .option("checkpointLocation", "/tmp/checkpoint") \
            .trigger(processingTime='10 seconds') \
            .start()
        
        logger.info("Streaming query started. Waiting for data...")
        
        # Wait for termination
        query.awaitTermination()
        
    except Exception as e:
        logger.error(f"Streaming application failed: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()