from flask import Flask, request, jsonify, render_template

import sqlite3

app = Flask(__name__)
DATABASE = 'notes.db'
app.debug = True


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    note_type = data.get('type')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO notes (title, content, type) VALUES (?, ?, ?)', (title, content, note_type))
    note_id = cursor.lastrowid
    db.commit()

    return jsonify({'id': note_id, 'title': title, 'content': content, 'type': note_type}), 201

@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    note = cursor.fetchone()

    if note:
        return jsonify(dict(note)), 200
    else:
        return jsonify({'error': 'Note not found'}), 404

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE notes SET title = ?, content = ? WHERE id = ?', (title, content, note_id))
    db.commit()

    return jsonify({'message': 'Note updated successfully'}), 200

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    db.commit()

    return jsonify({'message': 'Note deleted successfully'}), 200


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with sqlite3.connect(DATABASE) as db:
        db.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, type TEXT)')

    app.run(host='0.0.0.0', port=8080)
