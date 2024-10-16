# location, month, month num, day, day of week, hour, minute
import csv
import re
from datetime import datetime, timezone
from pytz import timezone, utc
from timezonefinder import TimezoneFinder


tzf = TimezoneFinder()


def convertByTimezone(dt, lat, lng):

    tz = timezone(tzf.certain_timezone_at(lng=float(lng), lat=float(lat)))
    return dt.astimezone(tz)


STATES = ["Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Minor Outlying Islands", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Northern Mariana Islands", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "U.S. Virgin Islands", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

f = []
def guessLocationType(loc):
	locComponents = loc.split(",")
	# if(str.find(loc, ""))
	matchPatterns = [
		["restaurant", "Restaurant"],
		["Kitchen", "Restaurant"],
		["eatery", "Restaurant"],
		["Coffee", "Restaurant"],
		["bakery", "Restaurant"],
		["burger", "Restaurant"],
		["Winery", "Restaurant"],
		["vineyards", "Restaurant"],
		["pizza", "Restaurant"],
		["avenue", "Neighborhood"],
		["street", "Neighborhood"],
		["times square", "Neighborhood"],
		["Santa Monica Pier", "Neighborhood"],
		["horseshoe bend", "Natural Attraction"],
		["Hollywood Walk of Fame", "Place of Interest"],
		["Empire State Building", "Place of Interest"],
		["Antelope Canyon", "Natural Attraction"],
		["Bellagio Las Vegas", "Travel"],
		["Las Vegas Strip", "Neighborhood"],
		["Griffith Observatory", "Place of Interest"],
		["Lincoln Memorial", "Place of Interest"],
		["Monument Valley", "Natural Attraction"],
		["United States Capitol", "Place of Interest"],
		["PIER 39", "Neighborhood"],
		["Hollywood Sign", "Place of Interest"],
		["Lower Antelope Canyon", "Natural Attraction"],
		["Statue of Liberty National Monument", "Place of Interest"],
		["Venice Beach", "Neighborhood"],
		["DUMBO", "Neighborhood"],
		["The High Line", "Neighborhood"],
		["Hollywood", "Neighborhood"],
		["Rockefeller Center", "Place of Interest"],
		["Grand Central Terminal", "Travel"],
		["The Venetian Resort Las Vegas", "Travel"],
		["Union Square, San Francisco", "Neighborhood"],
		["Fisherman's Wharf", "Neighborhood"],
		["The White House", "Place of Interest"],
		["Millennium Park", "Place of Interest"],
		["grand canyon", "Natural Attraction"],
		["museum", "Place of Interest"],
		["national park", "Natural Attraction"],
		["state park", "Natural Attraction"],
		["bridge", "Natural Attraction"],
		["central park", "Natural Attraction"],
		["niagara falls", "Natural Attraction"],
		["botanical garden", "Natural Attraction"],
		["botanic garden", "Natural Attraction"],
		["universal studios", "Place of Interest"],
		["disney", "Place of Interest"],
		["busch gardens", "Place of Interest"],
		["Wizarding World", "Place of Interest"],
		["zoo","Place of Interest"],
		["airport", "Travel"],
		["LAX", "Travel"],
		["statue of liberty", "Place of Interest"],
		["World Trade Center", "Place of Interest"],
		["hoover dam", "Place of Interest"],
		["Beach", "Natural Attraction"],
		["soho", "Neighborhood"],
		["Lake Powell", "Natural Attraction"],
		["Death Valley", "Natural Attraction"],
		["bubba gump", "Restaurant"],
		["downtown", "Neighborhood"],
		["district", "Neighborhood"],
		["chinatown", "Neighborhood"],
		["denny's", "Neighborhood"],
		["the signature room","Restaurant"],
		["Upper East Side","Neighborhood"],
		["Stearns Wharf","Neighborhood"],
		["hotel","Travel"],
		["eataly","Restaurant"],
		["lake","Natural Attraction"],
		["Eagle Point","Natural Attraction"],
		["Chicago River","Neighborhood"],
		["Yard House","Neighborhood"],
		["apartments","Neighborhood"],
		["beacon hill","Neighborhood"],
		["roosevelt island","Natural Attraction"],
		["national preserve","Natural Attraction"],
		["San Francisco Bay Area","Neighborhood"],
		["midtown","Neighborhood"],
		["waterfront","Neighborhood"],
		["river","Natural Attraction"],
		["falls","Natural Attraction"],
		["New York City","City"],
		["chelsea","Neighborhood"],
		["St. Louis","City"],
		["ihop","Restaurant"],
		["Washington, DC","City"],
		["Williamsburg, Brooklyn","Neighborhood"],
		["Capitol Hill","Neighborhood"],
		["Boulevard","Neighborhood"],
		["Badwater Basin","Natural Attraction"],
		["New York City - Manhattan - Nyc","City"],
		["Bryant Park","Natural Attraction"],
		["Navy Pier","Neighborhood"],
		["white sands","Natural Attraction"],
		["Little Havana","Neighborhood"],
		["Kerry Park","Neighborhood"],
		["La Jolla Cove","Natural Attraction"],
		["Balboa Park","Neighborhood"],
		["Washington Square Park","Natural Attraction"],
		["Georgetown","Neighborhood"],
		["union station","Travel"],
		["cheesecake","Restaurant"],
		["Boston Harbor","Neighborhood"],
		["Golden Gate Park","Natural Attraction"],
		["Madison Square Park","Neighborhood"],
		["Battery Park","Neighborhood"],
		["Glacier Point","Natural Attraction"],
		["yosemite","Natural Attraction"]
	]

	if locComponents[-1].strip() in STATES and len(locComponents) == 2:
		return "City"

	if loc.strip() in STATES:
		return "State"

	for mp in matchPatterns:
		if re.search(mp[0], loc, re.IGNORECASE):
			return mp[1]

	return ""

def reformatLocationFile():
	tmpLocs = []
	with open('data/Location.csv', newline='') as csvfile:
		cr = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in cr:
			loc = row[0]
			locCount = locData[loc]["locCount"]
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

			locType = guessLocationType(loc)
			if(loc not in tmpLocs):
				if(locType == "" and locCount >= 10):
					# default location type, checked as valid for all location Counts >= 10
					# small location counts are not part of analysis data set
					locType = "Place of Interest"
				if locType != "":
					locData[loc]["locType"] = locType
					locData[loc]["state"] = state
					locData[loc]["lat"] = lat
					locData[loc]["lon"] = lon

					tmpLocs.append(loc)

temperatureData = {}
def getTemperatureData():
	with open('data/Temperature.csv', newline='') as csvfile:
		cr = csv.reader(csvfile, delimiter=',', quotechar='"')
		h = next(cr)
		for row in cr:
			state = row[0]
			month = str(int(row[4]))
			year = row[5]
			temp = row[2]
			temperatureData[state + "_" + year + "-" + month ] = temp



def buildBigTable():
	with open('data/IG.csv', newline='') as csvfile:
		cr = csv.reader(csvfile, delimiter=',', quotechar='"')
		h = next(cr)
		cw = csv.writer(open("data/lookerData.csv","w"))
		cw.writerow(["location","locationType","state","lat","lon","month","year","dayOfWeek","hour","minute","temperature"])

					# locData[loc]["locType"] = locType
					# locData[loc]["state"] = state
					# locData[loc]["lat"] = lat
					# locData[loc]["lon"] = lon

					# temperatureData[state + "_" + year + "-" + month ] = temp


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
			state = locObj["state"]
			lat = locObj["lat"]
			lon = locObj["lon"]
			dateObj = convertByTimezone(dateObjRaw, lat, lon)
			# dateObj = dateObjRaw

			# print(dateObj)

			month = dateObj.month
			year = dateObj.year
			dayOfWeek = dateObj.strftime("%A")
			dayOfWeekNum = dateObj.weekday()
			hour = dateObj.hour
			minute = dateObj.minute

			temperatureKey = state + "_" + str(year) + "-" + str(month)
			if(temperatureKey not in temperatureData):
				continue

			temperature = temperatureData[temperatureKey]

			cw.writerow([location,locationType,state,lat,lon,month,year,dayOfWeek,dayOfWeekNum,hour,minute,temperature])






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

	reformatLocationFile()
	getTemperatureData()
	buildBigTable()

createSingleTable()





