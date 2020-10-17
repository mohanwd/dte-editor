import socket
from elasticsearch import Elasticsearch

REMOTE_SERVER = "www.google.com"
def is_connected(hostname):
	try:
		host = socket.gethostbyname(hostname)
		s = socket.create_connection((host, 80), 2)
		s.close()
		return True
	except:
		pass
	return False

def esInitConnect():
	print("es-ingestion initiated")
	es = None
	es = Elasticsearch(hosts="http://admin:admin@192.168.0.124:9200")
	if es.ping():
		print('Yay Connect')
	else:
		print('Awww it coould not connect')
	return es

#print(is_connected(REMOTE_SERVER))