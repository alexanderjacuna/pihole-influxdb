from influxdb import InfluxDBClient
import requests
import subprocess

#INFLUXDB CONNECTION INFO
host = "192.168.1.67"
port = 8086
user = "writer"
password = "password" 
dbname = "pihole"

#PIHOLE API 
piholeAPI = "http://192.168.1.34/admin/api.php"

def writeData(domains_being_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today, unique_clients):

	# CREATE CLIENT OBJECT
	client = InfluxDBClient(host, port, user, password, dbname)

	# MEASUREMENT NAME
	measurement = subprocess.check_output("hostname", shell=True)
	measurement = measurement.strip()

	data1 = [
	    {
	        "measurement": measurement + "-" + "pihole" + "-" + "domains_being_blocked",
	        "tags": {
	            "host": measurement
	        },
	        "fields": {
				"domains_being_blocked": int(domains_being_blocked)
	        }
	    }
	]

	data2 = [
	    {
	        "measurement": measurement + "-" + "pihole" + "-" + "dns_queries_today",
	        "tags": {
	            "host": measurement
	        },
	        "fields": {
				"dns_queries_today": int(dns_queries_today)
	        }
	    }
	]
	data3 = [
	    {
	        "measurement": measurement + "-" + "pihole" + "-" + "ads_percentage_today",
	        "tags": {
	            "host": measurement
	        },
	        "fields": {
				"ads_percentage_today": float(ads_percentage_today)
	        }
	    }
	]
	data4 = [
	    {
	        "measurement": measurement + "-" + "pihole" + "-" + "ads_blocked_today",
	        "tags": {
	            "host": measurement
	        },
	        "fields": {
				"ads_blocked_today": int(ads_blocked_today)
	        }
	    }
	]
	data5 = [
	    {
	        "measurement": measurement + "-" + "pihole" + "-" + "unique_clients",
	        "tags": {
	            "host": measurement
	        },
	        "fields": {
				"unique_clients": int(unique_clients)
	        }
	    }
	]

	# WRITE DATA
	client.write_points(data1)
	client.write_points(data2)
	client.write_points(data3)
	client.write_points(data4)
	client.write_points(data5)

if __name__ == "__main__":

	api = requests.get(piholeAPI)
	apiOut = api.json()
	domains_being_blocked = (apiOut['domains_being_blocked'])
	dns_queries_today = (apiOut['dns_queries_today'])
	ads_percentage_today = (apiOut['ads_percentage_today'])
	ads_blocked_today = (apiOut['ads_blocked_today'])		
	unique_clients = (apiOut['unique_clients'])
	
	writeData(domains_being_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today, unique_clients)
