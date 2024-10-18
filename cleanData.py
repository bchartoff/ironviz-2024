# location, month, month num, day, day of week, hour, minute
import csv
import re
import math
from datetime import datetime, timezone
from dateutil import tz
from pytz import timezone, utc
from timezonefinder import TimezoneFinder


tzf = TimezoneFinder()


def convertByTimezone(dt, lat, lng):
	fromZone = tz.tzutc()
	toZone = timezone(tzf.certain_timezone_at(lng=float(lng), lat=float(lat)))
	
	dt = dt.replace(tzinfo=fromZone)
	return dt.astimezone(toZone)


STATES = ["Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Minor Outlying Islands", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Northern Mariana Islands", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "U.S. Virgin Islands", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

def reformatLocationFile():
	with open('data/Location.csv', newline='') as csvfile:
		cr = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in cr:
			loc = row[0]
			geoLoc = row[4]
			lat = row[5]
			lon = row[6]
			state = ""

			geoComponents = geoLoc.split(",")

			country = geoComponents[-1].strip()
			if country != "United States" and country != "United States of America":
				# skip over locations not in USA,
				# likely geocoding errors in source data
				continue
			elif len(geoComponents) == 1:
				# skip over locations with no state data,
				# e.g. coded as "United States of America"
				continue
			elif geoComponents[-2].strip() in STATES:
				state = geoComponents[-2].strip()
			elif geoComponents[-3].strip() in STATES:
				state = geoComponents[-3].strip()
			else:
				# skip over locations with no state data,
				# e.g. "Cape Cod Bay, Plymouth, United States of America"
				continue


			locData[loc]["state"] = state
			locData[loc]["lat"] = lat
			locData[loc]["lon"] = lon

temperatureData = {}
def getTemperatureData():
	with open('data/Temperature.csv', newline='') as csvfile:
		cr = csv.reader(csvfile, delimiter=',', quotechar='"')
		h = next(cr)
		for row in cr:
			state = row[0]
			month = str(int(row[4]))
			year = row[5]
			# round down to nearest 10
			temp = math.floor(float(row[2])/10)*10
			temperatureData[state + "_" + year + "-" + month ] = temp

def buildBigTable():
	with open('data/IG.csv', newline='') as csvfile:
		cr = csv.reader(csvfile, delimiter=',', quotechar='"')
		h = next(cr)
		cw = csv.writer(open("data/lookerData.csv","w"))
		cw.writerow(["location","category","parentCategory","state","lat","lon","dateString","month","year","dayOfWeek","dayOfWeekNum","hour","minute","temperature"])

		for row in cr:

			locRaw = row[0]
			locObj = locData[locRaw]

			if "locType" not in locObj:
				continue

			datetimeRaw = row[1]
			# pop off the terminal "Z", indicating UTC time
			dateObjRaw = datetime.fromisoformat(datetimeRaw[:-1])

			location = locRaw
			locationType = locObj["locType"]
			locationParentType = locObj["locParentType"]
			state = locObj["state"]
			lat = locObj["lat"]
			lon = locObj["lon"]
			dateObj = convertByTimezone(dateObjRaw, lat, lon)

			month = dateObj.month
			year = dateObj.year
			dayOfWeek = dateObj.strftime("%A")
			dayOfWeekNum = dateObj.weekday()
			dateNum = dateObj.day
			hour = dateObj.hour
			minute = dateObj.minute

			temperatureKey = state + "_" + str(year) + "-" + str(month)
			if(temperatureKey not in temperatureData):
				continue

			temperature = temperatureData[temperatureKey]

			cw.writerow([location,locationType,locationParentType,state,lat,lon,datetimeRaw,month,year,dayOfWeek,dayOfWeekNum,hour,minute,dateNum])


locData = {}
def createSingleTable():
	# x = 1
	with open('data/IG.csv', newline='') as csvfile:
		cr = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in cr:
			loc = row[0]
			if loc not in locData:
				locData[loc] = {"locCount": 1}
			else:
				locData[loc]["locCount"] += 1
	with open('gptLocationClassifications.csv', newline = '') as csvfile:
		cr = csv.reader(csvfile, delimiter=',', quotechar='"')
		h = next(cr)
		for row in cr:
			if row[0] not in locData:
				continue
			locData[row[0]]["locType"] = row[1]
			locData[row[0]]["locParentType"] = row[2]


	reformatLocationFile()
	getTemperatureData()
	buildBigTable()

createSingleTable()





