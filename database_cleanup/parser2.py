import datetime
import os
import mysql.connector
import re
from nltk.tokenize import RegexpTokenizer
import nltk

# Consult Divit if you have any questions about the code


#connect to database
cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='dbms')
cursor = cnx.cursor()

add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")

tokenizer = RegexpTokenizer(r'\w+')

#reads and parses a file
def read_file(file_path, filename, year):
	curFile = open(file_path, 'r')

	add_meta = ("INSERT INTO paper_meta "
               "(paper, date_created, title, comments, abstract) "
               "VALUES (%s, %s, %s, %s, %s)")

	add_author = ("INSERT INTO author "
               "(name, paper) "
               "VALUES (%s, %s)")

	mysql_object = {
		"Title": "",
		"Paper": "",
		"Comments": "",
		"Journal-ref": "",
		"Abstract": "",
		"Authors": ""
	}
	abstract = ""

	for line in curFile:

		propertyName = line.split(':')

		if len(propertyName) > 1 and propertyName[0] != 'From':

			if propertyName[0] == 'Date':
				act_date = parse_date(line.strip(), year)
				mysql_object['Date'] = str(act_date)

			elif propertyName[0] == 'Comments' or propertyName[0] == 'Journal-ref':
				cleaned_word_array = tokenizer.tokenize(propertyName[1])
				cleaned_word = ""
				for word in cleaned_word_array:
					cleaned_word += word + ' '

				mysql_object[propertyName[0]] = str(cleaned_word.strip())

			elif propertyName[0] == 'Title':
				cleaned_word_array = tokenizer.tokenize(propertyName[1])
				cleaned_word = ""
				for word in cleaned_word_array:
					if word in nltk.corpus.stopwords.words('english') or len(word) < 3: 
						cleaned_word_array.remove(word)
				
				for word in cleaned_word_array:
					cleaned_word += word.lower() + ' '

				mysql_object[propertyName[0]] = str(cleaned_word.strip())

			elif propertyName[0] == 'Authors' or propertyName[0] == 'Paper':
				mysql_object[propertyName[0]] = str(propertyName[1].strip())


		elif len(line[2:]) > 1 and propertyName[0] != 'From' and line[0] != '-':
			word_list = tokenizer.tokenize(line)
			for word in word_list: # iterate over word_list
				if word in nltk.corpus.stopwords.words('english') or len(word) < 3: 
					word_list.remove(word) # remove word from filtered_word_list if it is a stopwo
			
			for word in word_list:
					abstract += word + ' '

	mysql_object['Abstract'] = abstract.lower().strip()
	add_info = (mysql_object['Paper'], mysql_object['Date'], mysql_object['Title'], mysql_object['Comments'], str(mysql_object['Abstract']))

	authors = mysql_object['Authors'].replace(" and ", ",");
	authors = authors.replace("&", ",")

	cleaned_authors = ""

	seenLeft = None
	for letter in authors:

		# print letter
		if letter == "(":
	 		seenLeft = True

	 	if seenLeft == None:
			cleaned_authors += letter

		if letter == ")":
			seenLeft = None

	if 'JR' in cleaned_authors.upper():
		temp = cleaned_authors.upper().replace(", JR", " JR")
		temp = temp.replace("JR.", "JR")
		cleaned_authors = temp


	parsed_authors = cleaned_authors.split(",")

	for author in parsed_authors:
		if len(author) > 0:
			add_author_info = (author.strip().upper(), mysql_object['Paper'])
			cursor.execute(add_author, add_author_info)

	cursor.execute(add_meta, add_info)
	cnx.commit()


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




