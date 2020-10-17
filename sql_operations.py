# -*- coding: utf-8 -*-
# Syncing the data with server
import time
import sqlite3 
from sqlite3 import Error

def init_connection():
	try:
		conn = sqlite3.connect('dte.db')
		print("Local DB Connection successfully")
		return conn
	except Error:
		print(Error)

def listTables(conn):
	conn.text_factory = str
	cur = conn.cursor()
	newline_indent = '\n '
	print("Listing Tables")
	result = cur.execute("SELECT * FROM sqlite_master WHERE type='table';").fetchall()
	table_names = sorted(list(zip(*result))[1])
	print ("\ntables are:"+newline_indent+newline_indent.join(table_names))
	return table_names

def listColumns(conn,table_names):
	conn.text_factory = str
	cur = conn.cursor()
	print("Listing Columns")
	newline_indent = '\n '
	for table_name in table_names:
		result = cur.execute("PRAGMA table_info('%s')" % table_name).fetchall()
		column_names = list(zip(*result))[1]
		print(("\ncolumn names for %s:" % table_name)
			+newline_indent
			+(newline_indent.join(column_names)))
def createTable(conn):
	cur = conn.cursor()
	print("Creating Tables")
	cur.execute("CREATE TABLE IF NOT EXISTS dte_entry(eventid integer primary key autoincrement, fileid text,event text, e_date text, e_time text)")
	cur.execute("CREATE TABLE IF NOT EXISTS dte_events(eventid integer primary key, fileid text,event text, ipaddress text, org text, username text, address text, city text, state text, country text, geo text, lat real, lon real, e_date text, e_time text)")
	conn.commit()

def insertDteEntry(conn,ent_entry):
	cur = conn.cursor()
	cur.execute('INSERT INTO dte_entry (fileid, event, e_date, e_time) VALUES (?,?,?,?)', ent_entry)
	# cur.execute('INSERT INTO dte_events (eventid, fileid, event, ipaddress, org, username, address, city, state, country, lat, lon, zone, e_date, e_time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', entities)
	conn.commit()

def insertDteEvents(conn,ent_events):
	cur = conn.cursor()
	cur.execute('INSERT INTO dte_events (eventid, fileid, event, ipaddress, org, username, address, city, state, country, geo, lat, lon, e_date, e_time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', ent_events)
	conn.commit()

def fetchData(conn,query):
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	return rows

def fetchFreshEventId(conn,query):
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	return rows[0][0]

def dropTable(conn):
	cur = conn.cursor()
	cur.execute("DROP TABLE IF EXISTS dte_events")
	conn.commit()

def db_update():
	while 1:
		print("Updating DB")
		time.sleep(3)

conn = init_connection()
#dropTable(conn)
createTable(conn)
#ent_events = (1,"1aksjdhkahsd", 'Opened', '213.55.101.101', 'AS24757 Ethio Telecom', 'Mohan', 'Addis Ababa, Addis Ababa, ET', 'Addis Ababa', 'Addis Ababa', 'ET', '[9.025, 38.7469]', 9.025, 38.7469, '2020-02-02', '12:34:00')
# ent_entry = ("1aksjdhkahsd", 'Opened', '2020-02-02', '12:34:00')
# insertDteEntry(conn,ent_entry)
#insertDteEvents(conn,ent_events)
#query = 'SELECT min(e.eventid) FROM dte_entry e left outer join dte_events t on e.eventid=t.eventid where t.eventid is null'
#print(fetchFreshEventId(conn,query))
# query = "SELECT  FROM dte_events"
# print(fetchData(conn,query))
#table_names = listTables(conn)
#listColumns(conn,table_names)
conn.close()
