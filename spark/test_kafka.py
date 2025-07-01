#!/usr/bin/env python3

import os
import time
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_spark_kafka():
    """Simple test for Spark Kafka connectivity"""
    logger.info("Testing Spark with Kafka...")
    
    try:
        # Create simple Spark session without packages (JARs are already in classpath)
        spark = SparkSession.builder \
            .appName("Kafka-Test") \
            .config("spark.driver.memory", "1g") \
            .config("spark.executor.memory", "1g") \
            .getOrCreate()
        
        spark.sparkContext.setLogLevel("WARN")
        logger.info("Spark session created successfully")
        
        # Test basic Kafka connectivity
        try:
            df = spark \
                .readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "kafka:9092") \
                .option("subscribe", "iot-sensors") \
                .option("startingOffsets", "latest") \
                .load()
            
            logger.info("Kafka stream created successfully")
            
            # Simple console output test
            query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp") \
                .writeStream \
                .outputMode("append") \
                .format("console") \
                .option("truncate", "false") \
                .trigger(processingTime='10 seconds') \
                .start()
            
            logger.info("Streaming query started. Listening for messages...")
            
            # Run for 2 minutes then stop
            time.sleep(120)
            query.stop()
            
        except Exception as e:
            logger.error(f"Kafka streaming error: {str(e)}")
            
        finally:
            spark.stop()
            
    except Exception as e:
        logger.error(f"Spark session creation failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_spark_kafka()