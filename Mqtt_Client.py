import random
from paho.mqtt import client as mqtt_client

class MqttClient:
    def connect_mqtt(broker, port, client_id):
        def on_connect(client, userdata, flags, rc):
        # For paho-mqtt 2.0.0, you need to add the properties parameter.
        # def on_connect(client, userdata, flags, rc, properties):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        client = mqtt_client.Client(client_id)

        # For paho-mqtt 2.0.0, you need to set callback_api_version.
        client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

if __name__ == "__main__":
    mqtt_client = MqttClient()

    broker = 'mqtt.eclipse.org'
    port = 1883
    topic = "python/mqtt"
    client_id = f'publish-{random.randint(0, 1000)}'

    client = mqtt_client.connect_mqtt(broker, port, client_id)
    client.loop_start()
    client.publish(topic, 'test message')
    client.loop_stop()