from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

Id_tracking = []
tasks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    message = None
    if request.method == 'POST':
        task_name = request.form['task']
        Id_tracking.sort()
        if len(Id_tracking) == 0:
            id_temp = len([x for x in tasks if x["status"] != "Deleted"]) + 1
            tasks.append({"sequence_number": id_temp, "task_name": task_name, "status": "Pending"})
        else:
            tasks.append({"sequence_number": Id_tracking[0], "task_name": task_name, "status": "Pending"})
            Id_tracking.pop(0)
        message = f'Task "{task_name}" added successfully!'
        print(message)
        tasks.sort(key=lambda x: (x['sequence_number'] is None, x['sequence_number']))
        #return redirect(url_for('index'))
    return render_template('add_task.html',task_added=message)

@app.route('/list_completed_tasks')
def list_completed_tasks():
    completed_tasks = [task for task in tasks if task["status"] == "Completed"]
    return render_template('list_completed.html', tasks=completed_tasks)

@app.route('/list_all_tasks')
def list_all_tasks():
    all_tasks = [task for task in tasks if task["status"] != "Deleted"]
    return render_template('list_all.html', tasks=all_tasks)

@app.route('/complete_task', methods=['GET', 'POST'])
def complete_task():
    message = None
    if request.method == 'POST':
        task_id = int(request.form.get('task_id'))
        
        for task in tasks:
            print(type(task['sequence_number']))
            if task['sequence_number'] == task_id:
                task['status'] = 'Completed'
                message = f'Task "{task["task_name"]}" marked as completed!'
                break
            else:
                message = 'Task not found or already completed.'

    pending_tasks = [task for task in tasks if task['status'] == 'Pending']
    return render_template('complete_task.html', tasks=pending_tasks, message=message)

@app.route('/delete_task', methods=['GET', 'POST'])
def delete_task():
    message = None
    if request.method == 'POST':
        try:
            sequence_number = int(request.form.get('task_id'))
            print(sequence_number)
            for task in tasks:
                if task["sequence_number"] == sequence_number:
                    task["status"] = "Deleted"
                    Id_tracking.append(sequence_number)
                    task["sequence_number"] = None
                    message = f'Task "{task["task_name"]}" deleted successfully.'
                    #return render_template('delete_task.html', message=message)
            
        except ValueError:
            message = "Invalid input. Please enter a valid number."
        #return render_template('delete_task.html', message=message)
    pending_tasks = [task for task in tasks if task['status'] == 'Pending' or task['status'] == 'Completed' ]
    return render_template('delete_task.html',tasks=pending_tasks,message=message)

if __name__ == '__main__':
    app.run(debug=True)
