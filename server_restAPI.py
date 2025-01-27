from flask import Flask, jsonify, request,Response,send_file, render_template
import os


app = Flask(__name__) 

# Sample data (can be replaced with your own data source)
tasks = [
    {
        'id': 1,
        'title': 'ON/Off',
        'description': 'This is task 1.',
        'done': False
    },
    {
        'id': 2,
        'title': 'Timer',
        'description': 'This is task 2.',
        'done': False
    },
	    {
        'id': 1,
        'title': 'Calender',
        'description': 'This is task 1.',
        'done': False
    },	    
     
]

# Route to get all tasks
@app.route('/')
def handle_rout():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file_data = request.data  # Get the raw file data
        with open("updates_bin/test.txt", "wb") as f:
            f.write(file_data)
        return "File uploaded successfully", 200
    except Exception as e:
        return str(e), 400

"""
curl -X POST http://127.0.0.1:5000/update \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "target_path=updates_bin/test.txt"
"""

# @app.route('/update', methods=['POST'])
# def api_update():
#     post_data = request.get_json()
#     print(f"Received POST data: {post_data}")
#     size = os.path.getsize("updates_bin/firmware.bin")
#     print('Size of file is', size, 'bytes')
#     # key = request.form['api_key']
#     # target_path = request.form['target_path']
#     try:
#         return send_file("updates_bin/firmware.bin")
#     except Exception as e:
#         return str(e)

@app.route('/version',methods=['GET'])
def api_version():
    print ("Version ....")
    rest = {"success":True,"data":{"version":"1.2.1"}}
    return jsonify(rest),200
@app.route('/update', methods=['GET'])
def api_update2():
    # post_data = request.get_json()
    # print(f"Received POST data: {post_data}")
    size = os.path.getsize("updates_bin/firmware_1.2.1.bin")
    print('Size of file is', size, 'bytes')
    # key = request.form['api_key']
    # target_path = request.form['target_path']
    try:
        return send_file("updates_bin/firmware.bin")
    except Exception as e:
        return str(e)

# curl -X POST http://127.0.0.1:5000/receive -H "Content-Type: application/json" -d '{"key":"value", "number":123}'
@app.route('/receive', methods=['POST'])
def receive_data():
    data = request.get_json()  # Parse JSON data
    print("Received data:", data)
    data["numver"]=200
    return jsonify({"status": "success", "received": data}), 200
# curl "http://127.0.0.1:5000/get-data?key=value&number=123"

@app.route('/receive', methods=['GET'])
def receive_data2():
    data = request.args  # Retrieve query parameters
    print("Received GET data:", data)
    key1 = request.args.get('key1')
    key2 = request.args.get('key2')
    print(key1,key2)
    # Process incoming data
    # if key1 and key2:
    response_data = {
            "message": "Received your data",
            "key1": "key1",
            "key2": "key2"
        }
    return jsonify(response_data), 200
    # else:
    #     return jsonify({"error": "Missing parameters"}), 400

# curl  http://127.0.0.1:5000/test
@app.route('/test')
def handle_test():
    print("Get Request handled ")
    return Response(status=200)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# Route to get a specific task by its ID
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return jsonify({'task': task})
    else:
        return jsonify({'message': 'Task not found'}), 404

# Route to create a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        return jsonify({'message': 'Title is required'}), 400

    task = {
        'id': tasks[-1]['id'] + 1 if len(tasks) > 0 else 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

