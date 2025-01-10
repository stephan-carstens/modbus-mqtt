from paho.mqtt.client import mqtt
import logging
logger = logging.getLogger(__name__)

class MqttClient(mqtt.Client):
    def __init__(self, mqtt_cfg):
        super.__init__(mqtt.CLient.CallbackAPIVersion.VERSION2)
        self.username_pw_set(mqtt_cfg["user"], mqtt_cfg["password"])
        # self.mqtt_cfg = mqtt_cfg
    
    def on_connect(self, userdata, flags, rc):
        logger.info("Connected to MQTT broker")
        # subscribe to set topics (get from server implementation)

    def on_disconnect(self, userdata, rc):
        logger.info("Disconnected from MQTT broker")
        pass

    def on_message(self, userdata, rc):
        pass

if __name__ == "__main__":
    c = mqtt.Client().broker