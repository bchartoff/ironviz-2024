import csv

data = {}
with open('data/lookerData.csv', newline='') as csvfile:
	cr = csv.reader(csvfile, delimiter=',', quotechar='"')
	head = next(cr)
	for row in cr:
		parentCat = row[2]
		month = int(row[7])
		day = int(row[10])
		hour = int(row[11])

		if parentCat not in data:
			data[parentCat] = {
			"months":{1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0},
			"days":{0:0,1:0,2:0,3:0,4:0,5:0,6:0},
			"hours":{0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0},
			}
		data[parentCat]["months"][month] += 1
		data[parentCat]["days"][day] += 1
		data[parentCat]["hours"][hour] += 1


with open('data/lookerData.csv', newline='') as csvfile:
	cr = csv.reader(csvfile, delimiter=',', quotechar='"')
	head = next(cr)
	cw = csv.writer(open("data/lookerAggregateData.csv","w"))
	cw.writerow(["location","category","parentCategory","state","lat","lon","dateString","month","year","dayOfWeek","dayOfWeekNum","hour","minute","temperature","monthCountNormalized","dayCountNormalized","hourCountNormalized"])

	for row in cr:
		pc = data[row[2]]

		month = int(row[7])
		day = int(row[10])
		hour = int(row[11])

		mMax = max(pc["months"].values())
		dMax = max(pc["days"].values())
		hMax = max(pc["hours"].values())

		r  = row + [
			float(pc["months"][month]/mMax),
			float(pc["days"][day]/dMax),
			float(pc["hours"][hour]/hMax)
		]

		cw.writerow(r)


