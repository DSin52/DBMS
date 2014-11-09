import datetime
import os
import copy

#Consult Divit if you have any questions about the code

#reads and parses a file
def read_file(file_path, filename, year):
	curFile = open(file_path, 'r')
	writeFile = open('./cleaned/' + filename +'_clean', 'w+')

	for line in curFile:

		propertyName = line.split(':')

		if len(propertyName) > 1 and propertyName[0] != 'From':

			if propertyName[0] == 'Date':
				act_date = parse_date(line.strip(), year)
				writeFile.write('Date: ' + str(act_date) + '\n\n')

			elif propertyName[0] == 'Title' or propertyName[0] == 'Paper' or propertyName[0] == 'Authors' or propertyName[0] == 'Comments' or propertyName[0] == 'Journal-ref':
				writeVal = str(propertyName[0].strip() + ': ' + propertyName[1].strip() + '\n\n')
				writeFile.write(writeVal)

		#abstract
		elif len(line[2:]) > 1 and propertyName[0] != 'From' and line[0] != '-':
			writeFile.write(str(line.strip()))

#Given in this format: Fri, 17 Jan 92 16
def parse_date(date_string, year):
	date_array = date_string.split(' ')

	#remove extra white spaces from array
	for item in date_array:
	    if item == '':
	         date_array.remove(item)

	cur_date = None

	#weekday appears first
	if contains_weekday(date_array[1]):

		if contains_month(date_array[2]):
 			cur_date = datetime.date(int(year), int(get_full_month(date_array[2])), int(date_array[3]))

		elif int(date_array[2]) >= 1 and int(date_array[2]) <= 31:
 			cur_date = datetime.date(int(year), int(get_full_month(date_array[3])), int(date_array[2]))

	#day-mon-year
 	elif '-' in date_array[1]:
 		temp_array = date_array[1].split('-')
 		cur_date = datetime.date(int(year), int(get_full_month(temp_array[1])), int(temp_array[0]))

 	#month/day/year
 	elif '/' in date_array[1]:
 		temp_array = date_array[1].split('/')
 		cur_date = datetime.date(int(year), int(get_full_month(temp_array[0])), int(temp_array[1]))

	#day, mon 
 	elif int(date_array[1]) >= 1 and int(date_array[1]) <= 31:
 		cur_date = datetime.date(int(year), int(get_full_month(date_array[2])), int(date_array[1]))

 	#debugging
 	else:
 		print 'ERROR'
 		return

 	return cur_date
	


def contains_weekday(day):
	day = day.upper()

	if 'MON' in day or 'TUE' in day or 'WED' in day or 'THU' in day or 'FRI' in day or 'SAT' in day or 'SUN' in day:
		return True

	return False;

def contains_month(month):
	month = month.upper()

	if 'JAN' in month or 'FEB' in month or 'MAR' in month or 'APR' in month or 'MAY' in month or 'JUN' in month or 'JUL' in month or 'AUG' in month or 'SEP' in month or 'OCT' in month or 'NOV' in month or 'DEC' in month:
		return True

	return False

def get_full_month(given_month):
	month = given_month.upper()

	if month == "JAN":
		return "1"
	elif month == "FEB":
		return "2"
	elif month == "MAR":
		return "3"
	elif month == "APR":
		return "4"
	elif month == "MAY":
		return "5"
	elif month == "JUN":
		return "6"	
	elif month == "JUL":
		return "7"
	elif month == "AUG":
		return "8"
	elif month == "SEP":
		return "9"
	elif month == "OCT":
		return "10"
	elif month == "NOV":
		return "11"
	else:
		return "12"

if __name__ == '__main__':

	for file in os.listdir('./1992'):
		if file.endswith('.abs'):
			read_file("./1992/" + file, file, "1992")

	for file in os.listdir('./1993'):
		if file.endswith('.abs'):
			read_file("./1993/" + file, file, "1993")

	for file in os.listdir('./1994'):
		if file.endswith('.abs'):
			read_file("./1994/" + file, file, "1994")

	for file in os.listdir('./1995'):
		if file.endswith('.abs'):
			read_file("./1995/" + file, file, "1995")

	for file in os.listdir('./1996'):
		if file.endswith('.abs'):
			read_file("./1996/" + file, file, "1996")

	for file in os.listdir('./1997'):
		if file.endswith('.abs'):
			read_file("./1997/" + file, file, "1997")

	for file in os.listdir('./1998'):
		if file.endswith('.abs'):
			read_file("./1998/" + file, file, "1998")

	for file in os.listdir('./1999'):
		if file.endswith('.abs'):
			read_file("./1999/" + file, file, "1999")

	for file in os.listdir('./2000'):
		if file.endswith('.abs'):
			read_file("./2000/" + file, file, "2000")

	for file in os.listdir('./2001'):
		if file.endswith('.abs'):
			read_file("./2001/" + file, file, "2001")

	for file in os.listdir('./2002'):
		if file.endswith('.abs'):
			read_file("./2002/" + file, file, "2002")

	for file in os.listdir('./2003'):
		if file.endswith('.abs'):
			read_file("./2003/" + file, file, "2003")




