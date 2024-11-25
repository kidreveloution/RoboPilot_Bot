import requests
import messageBuilder
import zmq
import json
import threading
# ZeroMQ Connection Class
class ZMQ_CONNECTION:
    def __init__(self, TX_ID, RX_ID, SERVER_IP, message_handler=None):
        if not TX_ID or not RX_ID or not SERVER_IP:
            raise ValueError("TX_ID, RX_ID, and SERVER_IP are required.")

        self.TX_ID = TX_ID
        self.RX_ID = RX_ID
        self.SERVER_IP = SERVER_IP
        self.context = zmq.Context()
        self.dealer = self.context.socket(zmq.DEALER)
        self.dealer.setsockopt(zmq.IDENTITY, self.TX_ID.encode('utf-8'))
        self.dealer.setsockopt(zmq.RCVHWM, 10)  # Limit the receive queue

        self.message_handler = message_handler
        self.running = False

    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org')
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch public IP: {e}")
            return "0.0.0.0"

    def registerAtRouter(self):
        try:
            return messageBuilder.MESSAGE_CLASS(
                tx_id=self.TX_ID,
                msg_name="register",
                rx_id=self.RX_ID,
                content={"ip_address": self.get_public_ip()}
            ).buildMessage()
        except Exception as e:
            print(f"Error building registration message: {e}")
            return ""

    def connectZMQ(self):
        try:
            self.dealer.connect(self.SERVER_IP)
            registration_message = self.registerAtRouter()
            self.dealer.send_multipart([self.TX_ID.encode('utf-8'), registration_message.encode('utf-8')])
            print("Connected to ZeroMQ server.")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def listen(self):
        try:
            while self.running:
                message = self.dealer.recv_multipart()
                if message and self.message_handler:
                    self.message_handler(message[0].decode('utf-8'))
        except Exception as e:
            print(f"Error while listening: {e}")

    def sendMessage(self, RX_ID, msg_name, content):
        try:
            if isinstance(content, str):
                content = json.loads(content)
            msg = messageBuilder.MESSAGE_CLASS(
                tx_id=self.TX_ID,
                msg_name=msg_name,
                rx_id=RX_ID,
                content=content
            ).buildMessage()
            self.dealer.send_multipart([self.TX_ID.encode('utf-8'), msg.encode('utf-8')])
        except Exception as e:
            print(f"Error sending message: {e}")

    def startListenThread(self):
        self.running = True
        threading.Thread(target=self.listen, daemon=True).start()

    def stopListenThread(self):
        self.running = False

    def close(self):
        self.stopListenThread()
        self.dealer.close()
        self.context.term()
        print("ZMQ connection closed.")
