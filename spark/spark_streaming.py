from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StringType, FloatType, IntegerType
import requests
import json

spark = SparkSession.builder.appName("IoTStreaming").getOrCreate()

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "iot-data") \
    .load()

# Schéma corrigé pour correspondre aux données du producteur
schema = StructType() \
    .add("temperature", FloatType()) \
    .add("humidity", FloatType()) \
    .add("pressure", FloatType()) \
    .add("air_quality", FloatType()) \
    .add("light", FloatType()) \
    .add("motion", IntegerType()) \
    .add("sound_level", FloatType()) \
    .add("co2", FloatType()) \
    .add("battery_level", FloatType())

json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

def send_to_influxdb(row):
    try:
        # Format InfluxDB Line Protocol
        timestamp = int(current_timestamp().cast("long") * 1000000000)  # Nanoseconds
        line = f"iot_data temperature={row.temperature},humidity={row.humidity},pressure={row.pressure},air_quality={row.air_quality},light={row.light},motion={row.motion},sound_level={row.sound_level},co2={row.co2},battery_level={row.battery_level} {timestamp}"
        
        response = requests.post("http://influxdb:8086/write?db=iot_data", data=line)
        if response.status_code == 204:
            print(f"✅ Data sent to InfluxDB: {row.temperature}°C, {row.humidity}%")
        else:
            print(f"❌ InfluxDB Error: {response.status_code}")
    except Exception as e:
        print(f"❌ InfluxDB Error: {e}")

query = json_df.writeStream \
    .foreach(send_to_influxdb) \
    .start()

print("🚀 Spark Streaming started - waiting for data...")
query.awaitTermination()