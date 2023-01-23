import json

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def load_data():
    with open('studentsGrades.json') as f:
        return json.load(f)


def save_data(json_data):
    with open('studentsGrades.json', 'w') as f:
        json.dump(json_data, f, indent=4)


@app.route('/worker', methods=['POST'])
def create_worker():
    data = request.get_json()
    existing_data_array = load_data()
    existing_data_array.append(data)
    with open('studentsGrades.json', 'w') as f:
        f.write(json.dumps(existing_data_array))

    return data


@ app.route('/worker', methods=['GET'])
@ app.route('/worker/<string:worker_email>', methods=['GET'])
def read_worker(worker_email=""):
    json_data = load_data()
    if (worker_email == ""):
        return json_data
    else:
        for x in json_data:
            if x['email'] == worker_email:
                return x
            else:
                return {"msg": "not such worker "}

@app.route('/worker/<string:worker_email>', methods=['PUT'])
def update_worker(worker_email):
    json_data = load_data()
    input_data = request.get_json()
    employee_found = False
    for employee in json_data:
        if (worker_email == employee['email']):
            employee_found = True
            employee.update(input_data)
            break
    if not employee_found: 
        return {"msg": "not such worker "}
    with open('studentsGrades.json', 'w') as f:
        f.write(json.dumps(json_data))

    
    return input_data
    
@app.route('/worker/<string:worker_email>', methods=['DELETE'])
def delete_worker(worker_email):
    json_data = load_data()
    index = 0
    for employee in json_data:
        if (worker_email == employee['email']):
            json_data.pop(index)
            break
        else:
            index = index + 1

    with open('studentsGrades.json', 'w') as f:
        f.write(json.dumps(json_data))

    return jsonify({'message': employee['email']})

    
####################STUDENTS####################
def getAllStudents():
    with open('students.json') as f:
        return json.load(f)

@ app.route('/students', methods=['GET'])
def getStudents():
    json_data = getAllStudents()
    return json_data

@app.route('/students', methods=['POST'])
def create_Student():
    data = request.get_json()
    existing_data_array = getAllStudents()
    existing_data_array.append(data)
    with open('students.json', 'w') as f:
        f.write(json.dumps(existing_data_array))
    return data

    
if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        app.run(debug=True)
