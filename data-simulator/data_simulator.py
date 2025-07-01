#!/usr/bin/env python3

import json
import time
import random
import logging
from datetime import datetime
from kafka import KafkaProducer
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IoTDataSimulator:
    def __init__(self):
        self.kafka_servers = ['kafka:9092']
        self.topic = 'iot-sensors'
        self.producer = None
        self.device_count = 5
        self.running = True
        
    def connect_kafka(self):
        """Connect to Kafka with retry logic"""
        max_retries = 10
        for attempt in range(max_retries):
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=self.kafka_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=lambda k: k.encode('utf-8') if k else None,
                    retries=3,
                    retry_backoff_ms=1000
                )
                logger.info("Successfully connected to Kafka")
                return True
            except Exception as e:
                logger.warning(f"Kafka connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    logger.error("Failed to connect to Kafka after all attempts")
                    return False
        return False
    
    def generate_device_data(self, device_id):
        """Generate realistic IoT sensor data for a device"""
        # Simulate different device behaviors
        base_temp = 20 + (device_id * 2)  # Different base temperature per device
        temp_variation = random.uniform(-3, 8)
        
        # Create realistic correlations
        temperature = round(base_temp + temp_variation, 2)
        humidity = round(max(30, min(80, 60 + random.uniform(-15, 15) - (temperature - 22) * 2)), 2)
        pressure = round(1013.25 + random.uniform(-20, 20), 2)
        
        # Air quality gets worse with higher temperature
        air_quality = round(max(0, min(200, 50 + (temperature - 22) * 3 + random.uniform(-20, 20))), 1)
        
        # Light levels vary based on time simulation
        light_level = round(random.uniform(50, 800), 1)
        
        # Sound level has some correlation with motion
        motion = random.choice([0, 0, 0, 1])  # Motion less frequent
        base_sound = 35 if motion == 0 else 55
        sound_level = round(base_sound + random.uniform(-10, 15), 1)
        
        # CO2 correlates with occupancy (motion)
        base_co2 = 400
        co2_increase = 100 if motion == 1 else random.uniform(-20, 30)
        co2 = round(max(350, base_co2 + co2_increase), 1)
        
        # Battery drains over time with some randomness
        battery_level = round(random.uniform(20, 100), 1)
        
        locations = ["office", "warehouse", "lobby", "conference_room", "lab"]
        
        return {
            "device_id": f"sensor_{device_id:03d}",
            "timestamp": datetime.now().isoformat() + "Z",
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "air_quality": air_quality,
            "light": light_level,
            "sound_level": sound_level,
            "co2": co2,
            "motion": motion,
            "battery_level": battery_level,
            "location": locations[device_id % len(locations)]
        }
    
    def send_data(self, data):
        """Send data to Kafka"""
        try:
            future = self.producer.send(
                self.topic, 
                value=data, 
                key=data['device_id']
            )
            future.get(timeout=10)  # Wait for send confirmation
            return True
        except Exception as e:
            logger.error(f"Failed to send data: {e}")
            return False
    
    def run_simulation(self):
        """Main simulation loop"""
        logger.info(f"Starting IoT Data Simulator with {self.device_count} devices")
        
        if not self.connect_kafka():
            logger.error("Cannot start simulation without Kafka connection")
            return
        
        message_count = 0
        
        try:
            while self.running:
                # Generate data for all devices
                for device_id in range(1, self.device_count + 1):
                    sensor_data = self.generate_device_data(device_id)
                    
                    if self.send_data(sensor_data):
                        message_count += 1
                        logger.info(f"Sent data from {sensor_data['device_id']}: "
                                  f"temp={sensor_data['temperature']}°C, "
                                  f"humidity={sensor_data['humidity']}%, "
                                  f"motion={sensor_data['motion']}")
                    else:
                        logger.error(f"Failed to send data for device {device_id}")
                
                # Log statistics every 10 messages
                if message_count % 10 == 0:
                    logger.info(f"Total messages sent: {message_count}")
                
                # Wait before next batch
                time.sleep(5)  # Send data every 5 seconds
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, stopping simulation...")
        except Exception as e:
            logger.error(f"Simulation error: {e}")
        finally:
            if self.producer:
                self.producer.close()
            logger.info(f"Simulation stopped. Total messages sent: {message_count}")

def main():
    """Main function"""
    logger.info("IoT Data Simulator starting...")
    
    # Wait for Kafka to be ready
    logger.info("Waiting for Kafka to be ready...")
    time.sleep(30)
    
    simulator = IoTDataSimulator()
    simulator.run_simulation()

if __name__ == "__main__":
    main()