import cv2
import numpy as np
from pyzbar.pyzbar import decode
import paho.mqtt.client as mqtt

import RealTimeQR_Detector

class MTE460Scanner:

    def __init__(self):
        # Initialize camera & QR Code detector
        self.cap = cv2.VideoCapture(0)
        self.qr_detector = RealTimeQR_Detector.QRCodeDetector()

        # Initialize mqtt client
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.connect(host="localhost", port=1883)
        self.mqttc.loop_start()
    
    def publishData(self, dataTopic, dataValue):
        pubMessage = self.mqttc.publish(topic=dataTopic, payload=dataValue, qos=2)
        pubMessage.wait_for_publish()

    def run(self):
        qr_data_latest = ""

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            qr_codes = self.qr_detector.detect_qr_codes(frame)
            qr_data = self.qr_detector.extract_qr_data(qr_codes)
            print("QR Code Data:", qr_data)
            self.publishData('QRScanner/num_scans', len(qr_codes))

            if (qr_data != None):
                if (qr_data != qr_data_latest):
                    self.publishData('QRScanner/scan_data', qr_data)
                    qr_data_latest = qr_data

            self.qr_detector.draw_qr_code_rectangles(frame, qr_codes)

            # Display the frame with detected QR codes
            cv2.imshow("Detect QR Code from Webcam", frame)

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    scanner = MTE460Scanner()
    scanner.run()
