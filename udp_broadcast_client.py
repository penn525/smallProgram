import socket


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(('', 7788))

print('Listening for broadcast at ', client.getsockname())

while True:
	recv_data, addr = client.recvfrom(2048)
	print('Server received from {}:{}'.format(addr, recv_data.decode()))