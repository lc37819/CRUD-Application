from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'tasks.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return redirect(url_for('tasks'))

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    conn = get_db_connection()
    if request.method == 'GET':
        entries = conn.execute('SELECT * FROM tasks ORDER BY Created DESC').fetchall()
        conn.close()
        return render_template('index.html', entries=entries)
    elif request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        points = request.form['points']
        
        existing_id = conn.execute('SELECT Id FROM tasks WHERE Id = ?', (id,)).fetchone()
        if existing_id:
            conn.close()
            flash('This ID already exists. Please use a different ID.', 'error')
            return redirect(url_for('tasks'))
        
        conn.execute('INSERT INTO tasks (Id, Name, Points) VALUES (?, ?, ?)', (id, name, points))
        conn.commit()
        conn.close()
        return redirect(url_for('tasks'))

@app.route('/tasks/edit/<int:id>', methods=['GET'])
def edit_task(id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE Id = ?', (id,)).fetchone()
    conn.close()
    if task is None:
        flash('Task not found.', 'error')
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', task=task)

@app.route('/tasks/update/<int:id>', methods=['POST'])
def update_task(id):
    name = request.form['name']
    points = request.form['points']
    
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET Name = ?, Points = ? WHERE Id = ?', (name, points, id))
    conn.commit()
    conn.close()
    flash('Task updated successfully.', 'success')
    return redirect(url_for('tasks'))

@app.route('/tasks/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    if request.form['_method'] == 'DELETE':
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE Id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True)
