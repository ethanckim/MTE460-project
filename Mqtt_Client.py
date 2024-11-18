import random
import paho.mqtt.client as mqtt

def on_connect(mqttc, obj, flags, reason_code, properties):
    print("connect_status: " + str(reason_code))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid, reason_code, properties):
    print("mid: " + str(mid))


def on_log(mqttc, obj, level, string):
    print(string)


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect(host="localhost", port=1883)

mqttc.loop_start()

pubMessage = mqttc.publish(topic="barcodeScanner/test", payload=f"value={random.random()}", qos=2)
pubMessage.wait_for_publish()
