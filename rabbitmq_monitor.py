#!/bin/env python
# encoding: utf-8

import sys, urllib2, base64, json

#rabbitmq 
ip = "127.0.0.1"
username = "guest"
password = "guest"

#monitor keys
keys = ('messages_ready', 'messages_unacknowledged')
rates = ('ack', 'deliver', 'deliver_get', 'publish')

#login and get rabbitmq api
request = urllib2.Request("http://%s:15672/api/queues" %ip)
base64string = base64.b64encode("%s:%s" % (username,password))
request.add_header("Authorization", "Basic %s" % base64string)   
result = urllib2.urlopen(request)
data = json.loads(result.read())

p = []
for queue in data:
	msg_total = 0
	for key in keys:
		q = {}
		q['method'] = key
		q['queue_name'] = queue['name']
		q['total'] = int(queue[key])
		msg_total += q['total']
		p.append(q)

	q = {}
	q['method'] = 'rabbitmq.messages_total'
	q['queue_name'] = queue['name']
	q['total'] = msg_total
	p.append(q)
	
	for rate in rates:
		q = {}
		q['method'] = rate
		q['queue_name'] = queue['name']
		try:
			q['total'] = int(queue['message_stats']["%s_details" % rate]['rate'])
		except:
			q['total'] = 0
		p.append(q)


for totals in p:
	if totals["queue_name"] == sys.argv[1]:
		if totals["method"] == sys.argv[2]:
			print totals["total"]

