const mqtt = require('mqtt');
const kafka = require('kafka-node');

const mqttClient = mqtt.connect('mqtt://mosquitto:1883');
const kafkaClient = new kafka.KafkaClient({ kafkaHost: 'kafka:9092' });
const producer = new kafka.Producer(kafkaClient);

mqttClient.on('connect', () => {
  console.log('✅ MQTT connected');
  mqttClient.subscribe('iot/sensors');
});

producer.on('ready', () => {
  console.log('✅ Kafka producer ready');
  mqttClient.on('message', (topic, message) => {
    const payloads = [{ topic: 'iot-data', messages: message.toString() }];
    producer.send(payloads, (err, data) => {
      if (err) console.error('Kafka error:', err);
      else console.log('Sent to Kafka:', data);
    });
  });
});