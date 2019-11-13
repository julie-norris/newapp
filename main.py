from flask import Flask, render_template, url_for,jsonify, request, Response
import io
import requests
import json
import cx_Oracle
import pandas as pd
from pandas import ExcelFile
from pandas import ExcelWriter
con_str = 'psnavigator/navigate@xxxxxxx/xxxx'
con = cx_Oracle.connect(con_str)
c = con.cursor()



app = Flask(__name__)

@app.route("/")
def home():
	
	return render_template("home.html")
	
@app.route("/about")
def about():
	return render_template("about.html")
	
"""Step 3: create a route in your python server that takes a fullname argument, splits it into first and last name and returns a response in a json format"""	
"""Step 5: modify the python code to lookup the first and last name in the school database and return the row(s) data as json."""

@app.route("/user")
def username_first_last():

		username = request.args.get('username')
		(firstname, lastname)= username.split(" ")
		
		query="""
		SELECT student_number,
		 s.last_name, 
		 s.first_name,
		 s.dob,
		 s.schoolID  
		FROM students s 
		where s.first_name='""" + (firstname) + """'AND s.last_name='"""+(lastname)+"""'"""
			
		results=pd.read_sql(query, con)
		df=pd.DataFrame(results)

		return  (df.to_json(orient='records'))
		
@app.route("/missingapplication", methods=['GET', 'POST'])
def missing_applications():
		print ("this works")
		
		allstudentsquery="""
		SELECT s.student_number,
		  s.last_name,
		  s.first_name,
		  s.dob, 
		  s.schoolid,
		  p2.studentsdcid
		FROM students s
		where s.enroll_status = 0"""
	
		all_students=pd.read_sql(allstudentsquery, con)
		dfall=pd.DataFrame(all_students)
		
		
		file = request.files['franklin_file']
		colnames=['LAST_NAME','FIRST_NAME','SCHOOLID','DOB']
		df_franklin=pd.read_csv(file, names=colnames, header=None)
		
		df_franklin['DOB'] = pd.to_datetime(df_franklin['DOB'], format="%Y%m%d")

		result = dfall.merge(df_franklin, how='outer', indicator=True, on=['LAST_NAME','FIRST_NAME', 'SCHOOLID'])
		
		result = result[result['_merge'] == 'left_only']
		#creates memory to store data
		output = io.BytesIO()
		#create an excel writer to write to that memory
		writer=pd.ExcelWriter(output, engine='openpyxl')
		#tell pandas to write the results in excel format using the excel writer
		result.to_excel(writer)
		writer.save()
		writer.close()
		#go back to the beginning of the memory to read from it
		output.seek(0)
		#send the response containing the content from the memory in excel format 
		#and tell the browser to download it as an excelfile with a givenname
		return Response(output.read(),
        	mimetype="application/vnd.ms-excel",
        	headers={"Content-disposition":
                     "attachment; filename=StudentsWOApps.xlsx"})
		

@app.route("/userupload", methods=['GET', 'POST'])
def file_upload():
	
	file = request.files['selectfile']
	
	df=pd.read_excel(file)
	
	lastfirst = df['Student Name'] 
	schoolid = df['School']
	dob = df['dob']
	
	query="""
	SELECT student_number, s.dob, s.schoolid,  s.lastfirst,
	FROM students s
	JOIN schools sch ON s.schoolid = sch.school_number
	WHERE s.schoolid '""" + (schoolid) + """'AND s.lastfirst='"""+ (lastfirst)+"""'AND s.dob='"""+ (dob)+"""'"""
	
	results=pd.read_sql(query, con)
	df1=pd.DataFrame(results)
	
	#df1.to_excel("C:\\Users\\julie.norris\\Documents\\Data Warehouse Analyst\\Provision2\\19-20 Support for Schools\\output.xlsx")
		
	return (df1.to_json(orient='records'))
		
	
if __name__ == "__main__":
	app.run(debug=True)
