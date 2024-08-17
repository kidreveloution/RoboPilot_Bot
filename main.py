import mechcontrols.messageDigest
import modules.zmqHeader as zmqHeader
import mechcontrols
import mechcontrols.PWM



zmqObj = zmqHeader.ZMQ_CONNECTION(
    TX_ID="fake_worker_1",
    RX_ID="ROUTER",
    SERVER_IP="tcp://3.22.90.156:5555",
    message_handler=mechcontrols.messageDigest.messageHandler,
)

zmqObj.connectZMQ()
zmqObj.startListenThread()

