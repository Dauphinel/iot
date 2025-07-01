#!/usr/bin/env python3

import json
import time
import random
import logging
import paho.mqtt.client as mqtt
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IoTSensorProducer:
    def __init__(self):
        self.mqtt_host = os.getenv('MQTT_BROKER_HOST', 'mosquitto')
        self.mqtt_port = int(os.getenv('MQTT_BROKER_PORT', 1883))
        self.topic = 'iot/sensors'
        
        # MQTT client setup
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to MQTT broker at {self.mqtt_host}:{self.mqtt_port}")
        else:
            logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")
            
    def on_disconnect(self, client, userdata, rc):
        logger.info("Disconnected from MQTT broker")
        
    def on_publish(self, client, userdata, mid):
        logger.debug(f"Message {mid} published successfully")
        
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.mqtt_host, self.mqtt_port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            return False
            
    def generate_sensor_data(self):
        """Generate random IoT sensor data"""
        return {
            "device_id": f"sensor_{random.randint(1, 10):03d}",
            "timestamp": datetime.now().isoformat(),
            "temperature": round(random.uniform(18.0, 35.0), 2),
            "humidity": round(random.uniform(30.0, 80.0), 2),
            "pressure": round(random.uniform(980.0, 1020.0), 2),
            "air_quality": round(random.uniform(0, 200), 1),
            "light": round(random.uniform(0, 1000), 1),
            "sound_level": round(random.uniform(30.0, 90.0), 1),
            "co2": round(random.uniform(300, 1000), 1),
            "motion": random.randint(0, 1),
            "battery_level": round(random.uniform(10.0, 100.0), 1),
            "location": random.choice(["office", "warehouse", "lobby", "conference_room"])
        }
        
    def publish_data(self, data):
        """Publish sensor data to MQTT topic"""
        try:
            payload = json.dumps(data)
            result = self.client.publish(self.topic, payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Published data from {data['device_id']}: temp={data['temperature']}°C, humidity={data['humidity']}%")
                return True
            else:
                logger.error(f"Failed to publish data. Error code: {result.rc}")
                return False
                
        except Exception as e:
            logger.error(f"Error publishing data: {e}")
            return False
            
    def run(self):
        """Main producer loop"""
        logger.info("Starting IoT sensor data producer...")
        
        if not self.connect():
            logger.error("Could not connect to MQTT broker. Exiting.")
            return
            
        try:
            while True:
                # Generate and publish sensor data
                sensor_data = self.generate_sensor_data()
                self.publish_data(sensor_data)
                
                # Wait 5 seconds before next reading
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal. Stopping producer...")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Producer stopped")

if __name__ == "__main__":
    producer = IoTSensorProducer()
    producer.run()