from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
	
	return render_template("home.html")
	
@app.route("/about")
def about():
	return render_template("about.html")

"""Step 3: create a route in your python server that takes a fullname argument, splits it into first and last name and returns a response in a json format, e.g.:
"""

@app.route("/user")
def username_first_last():

		username = request.args.get('username')
		(firstname, lastname)= username.split(" ")
		user = {
			'firstname':firstname,
			'lastname':lastname
				}
		return jsonify(user)
		
	

if __name__ == "__main__":
	app.run(debug=True)
