import zmqHeader as zmqHeader

obj = zmqHeader.ZMQ_CONNECTION(TX_ID="TESTING",RX_ID="ROUTER",SERVER_IP="tcp://3.22.90.156:5555")
obj.connectZMQ()