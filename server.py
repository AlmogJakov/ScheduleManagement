from flask import Flask, render_template, request, redirect
import csv
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/index.html')
def main_page2():
    return render_template('index.html')

# write data to database.csv (meeting details)
def write_to_database(data):
	with open('database.csv', newline='', mode='a') as database:
		fullname = data[0]
		time = data[1]
		email = data[2]
		csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		#csv_writer = csv_writer(f'\n{name},{from},{to},{email}')
		csv_writer.writerow([fullname,time,email])

# write data to workers.csv (meeting details)
def write_to_workers(data):
	with open('workers.csv', mode='a') as database:
		time = data[1]
		csv_writer = csv.writer(database, lineterminator='', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		if get_from_workers() == []:
			csv_writer.writerow({time})
		else:
			csv_writer.writerow({'',time})

# write data to database.csv (meeting details)
def write_to_contact(data):
	with open('contact.csv', newline='', mode='a') as database:
		name = data["name"]
		email = data["email"]
		subject = data["subject"]
		message = data["message"]
		csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([name,email,subject,message])

# read data from workers.csv (schedule time)
def get_from_workers():
	with open('workers.csv', newline='') as database:
		csv_reader = csv.reader(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		data = list(csv_reader)
		if len(data) > 0:
			data[0].sort()
			return data[0]
		else:
			return []

##################################
# print worker schedule
def printSchedule(name):
    for i in range(len(name)):
        print(name[i])

# exchange Hours format To Minutes (for example convert 10:05 to 900)
def HTM(name): 
    x = int(name.partition(":")[2])+int(name.partition(":")[0])*60
    return x

# check worker availability for specific time input
def checkAvailability(name,worker):
    for i in range(len(worker)):
        if HTM(name)+29<=HTM(worker[i])-29:
            return True
        elif HTM(name)<=HTM(worker[i])+29 and HTM(name)>=HTM(worker[i])-29:
            return False
    return True
    
# show 30 minutes range (for example: convert 08:30 to 08:30-09:00)
def Vschedule(name):
    schedule = name
    for i in range(len(schedule)):
        temp = HTM(schedule[i])+30
        time = str(int(temp/60))+':'+str(temp%60)
        if len(time.partition(":")[2]) == 1:
            time = time.partition(":")[0]+":0"+time.partition(":")[2]
        if len(time.partition(":")[0]) == 1:
            time="0"+time
        schedule[i] += "-"+time
    return schedule
##################################

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
	if request.method == 'POST':
		data = request.form.to_dict()
		if len(data["fullname"])<=1:
			return 'Please enter a name!'
		if int(data["fromtimeH"])<8 or int(data["fromtimeH"])>20 or int(data["fromtimeM"])<0 or int(data["fromtimeM"])>59:
			return 'Time is out of range!'
		if len(data["email"])<=8:
			return 'Please enter a valid mail address!'
		# print(data["fromtime"])
		newTime = data["fromtimeH"]+":"+data["fromtimeM"]
		dataNew = [data["fullname"],newTime,data["email"]]
		#print(dataNew)
		if checkAvailability(dataNew[1],get_from_workers()):
			write_to_database(dataNew)
			write_to_workers(dataNew)
			#print(data["fromtime"])
			#print(data)
			return render_template('success.html', fullname = data["fullname"])
		else:
			return render_template('oops.html')
		return render_template('success.html')
	else:
		return 'Something went wrong!'

@app.route('/contact_form', methods=['POST', 'GET'])
def contact_form():
	if request.method == 'POST':
		data = request.form.to_dict()
		if len(data["name"])<=1 or len(data["email"])<=1 or len(data["subject"])<=1 or len(data["message"])<=1:
			return 'Please fill in all the fields!'
		else:
			write_to_contact(data)
			return render_template('success.html', fullname = data["name"])

@app.route('/contact.html')
def contact_page():
    return render_template('contact.html')

@app.route('/schedule.html')
def schedule_page():
	temp = get_from_workers()
	return render_template('schedule.html', schedule = Vschedule(temp))