import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_publish(client, userdata, mid):
    print(f"✅ Message published (ID: {mid})")

# Configuration du client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

try:
    client.connect("mosquitto", 1883, 60)
    client.loop_start()
    
    print("🚀 IoT Sensor Simulator started...")
    print("📡 Publishing data every 2 seconds...")
    
    while True:
        # Générer des données IoT réalistes
        data = {
            "temperature": round(random.uniform(18, 30), 2),
            "humidity": round(random.uniform(40, 70), 2),
            "pressure": round(random.uniform(980, 1050), 2),
            "air_quality": round(random.uniform(20, 150), 1),
            "light": round(random.uniform(100, 1000), 2),
            "motion": random.choice([0, 1]),
            "sound_level": round(random.uniform(30, 80), 2),
            "co2": round(random.uniform(350, 800), 2),
            "battery_level": round(random.uniform(10, 100), 2)
        }

        payload = json.dumps(data)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Publier sur le topic MQTT
        result = client.publish("iot/sensors", payload)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"[{timestamp}] 📊 Published: Temp={data['temperature']}°C, Humidity={data['humidity']}%")
        else:
            print(f"[{timestamp}] ❌ Failed to publish")
            
        time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 Stopping IoT Sensor Simulator...")
    client.loop_stop()
    client.disconnect()
except Exception as e:
    print(f"❌ Error: {e}")
    client.loop_stop()
    client.disconnect()
