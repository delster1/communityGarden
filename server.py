from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from database import authenticate, register_user, update_plant
from flask import jsonify
# from database import authenticate

app = Flask(__name__)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = "asdkjfhaskjdfhasiudfhasiudfuinyvulih324"

@app.route('/<path:filename>')
def send_file(filename):
    return app.send_static_file(filename)

# should be the plant homepage
@app.route('/')
# @jwt_required()
def index():
    print("INDEX")
    # return index.html from static folder
    return app.send_static_file('index.html')

# get the templates from mongodb and display them
@app.route('/templates')
def templates():
    return app.send_static_file('templates.html')

# login page
# create_access_token() function is used to actually generate the JWT, this function is in database
@app.route("/login", methods=['GET',"POST"])
def login():
    if request.method == "POST":
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        return authenticate(username, password)[0]

# registers a user into the db
@app.route('/register', methods=['GET',"POST"])
def register():
    if request.method == "POST":
        print("REGISTER called")
        data = request.get_json()
        username = data['username']
        password = data['password']
        register_user(username, password)
        return jsonify({"message": "User registered", "username": username})

# shows the garden of other users!
@app.route('/garden')
def garden():
    return app.send_static_file('garden.html')


# Swap task endpoint for user to change a task from their personal checklist
@app.route('/swap', methods=['POST'])
@jwt_required()
def swap_task():
    current_user = get_jwt_identity()
    return app.send_static_file('index.html')

# Grow user's plant
@app.route('/grow', methods=['POST'])
@jwt_required()
def grow():
    current_user = get_jwt_identity()
    update_plant(current_user, "test")
    return app.send_static_file('index.html')

# Add water to user's plant
@app.route('/water', methods=['POST'])
@jwt_required()
def water():
    update_plant(current_user, "test")
    return app.send_static_file('index.html')

# Add sunlight to user's plant
@app.route('/sunlight', methods=['POST'])
@jwt_required()
def sunlight():
    update_plant(current_user, "test")
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

