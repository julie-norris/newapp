from pandas import ExcelWriter
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
		 s.dob 
		FROM students s 
		where s.first_name='""" + (firstname) + """'AND s.last_name='"""+(lastname)+"""'"""
			
		results=pd.read_sql(query, con)
		df=pd.DataFrame(results)
		return  (df.to_json(orient='records'))
		
		"""return jsonify(my_table=json.loads(df.to_json(orient="split"))["data"],
                   columns=[{"title": str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]])"""
		
	
if __name__ == "__main__":
	app.run(debug=True)
