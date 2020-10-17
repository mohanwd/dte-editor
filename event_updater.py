# -*- coding: utf-8 -*-
# Syncing the data with server
# import time
from datetime import datetime
from uuid import uuid4
from sql_operations import *
from ip_info import *
from check_connectivity import *

def generateFileId():
	return 'zone-'+ datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

def eventRegister(fileid,event):
	conn = init_connection()
	date_time = datetime.now()
	ent_entry = (fileid, event, date_time, date_time.strftime('%H:%M:%S'))
	insertDteEntry(conn,ent_entry)
	conn.close()
	if is_connected("www.google.com"):
		metricsRegister()
	else:
		print("Skipping updates As there is no internet connectivity")

def metricsRegister():
	conn = init_connection()
	print("Metrics Register")
	username = userName()
	g = geoCode()
	q_start_eventid = 'SELECT min(e.eventid) FROM dte_entry e left outer join dte_events t on e.eventid=t.eventid where t.eventid is null'
	start_event_id = fetchFreshEventId(conn,q_start_eventid)
	print("SELECT * FROM dte_entry where eventid>="+str(start_event_id))
	if start_event_id:
		rows = fetchData(conn,"SELECT * FROM dte_entry where eventid>="+str(start_event_id))
		for row in rows:
			ent_events = (row[0], row[1], row[2], g.ip, g.org, username, g.address, g.city, g.state, g.country,  str(g.lat)+','+str(g.lng), g.lat, g.lng, row[3], row[4])
			insertDteEvents(conn,ent_events)
			esIngestor(ent_events)
	else:
		print('No new events to update!!!')
	conn.close()

def esIngestor(values):
	print("ES Ingestion")
	es = esInitConnect()
	record = esRecordCreator(values)
	try:
		outcome = es.index(index="test",doc_type='_doc',body=record)
	except Exception as ex:
		print('Error in indexing data')
		print(str(ex))

def esRecordCreator(values):
	cols = ["eventid","fileid","event","ipaddress","org","username","address","city","state","country","geo","lat","lon","e_date","e_time"]
	record = {}
	for ind,col in enumerate(cols):
		record[col] = values[ind]
	record["location"] = {
	"lat":record["lat"],
	"lon":record["lon"]
	}
	print(record)
	return record

if is_connected("www.google.com"):
	metricsRegister()
else:
	print("Skipping updates As there is no internet connectivity")
