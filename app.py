from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT)''')
        conn.commit()

# Initialize the database
init_db()

@app.route('/')
def index():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM items')
        items = c.fetchall()
        return render_template('index.html', items=items)

@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item = c.fetchone()
        if item:
            return render_template('item.html', item=item)
        else:
            return jsonify({'error': 'Item not found'}), 404

@app.route('/delete-item/<int:item_id>', methods=['GET'])
def delete_item(item_id):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
