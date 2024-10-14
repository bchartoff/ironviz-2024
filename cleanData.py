# location, month, month num, day, day of week, hour, minute
import csv
import re
from datetime import datetime
from pytz import timezone, utc
from timezonefinder import TimezoneFinder


tzf = TimezoneFinder()


def get_offset(lat, lng):
    """
    returns a location's time zone offset from UTC in minutes.
    
    from Timezonefinder documentation, https://timezonefinder.readthedocs.io/en/latest/2_use_cases.html#getting-a-location-s-time-zone-offset

    """

    today = datetime.now()
    tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))
    # ATTENTION: tz_target could be None! handle error case
    today_target = tz_target.localize(today)
    today_utc = utc.localize(today)
    return (today_utc - today_target).total_seconds() / 60



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
		cw = csv.writer(open("data/location_clean.csv","w"))
		cw.writerow(["location","locationType","state","lat","lon", "count"])
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
					cw.writerow([loc, locType,state,lat,lon,locCount])
					tmpLocs.append(loc)


def reformatIGFile():
	# split up date
	x = 1

def mergeLocationIg():
	# merge
	x = 1

def mergeTempIg():
	# merge
	x = 1




# ig_reader = csv.reader()
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

createSingleTable()

	# start with IG
	# 

	# with open('eggs.csv', newline='') as csvfile:
	#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')






