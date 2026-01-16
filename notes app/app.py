# Import the tools we need
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

# Create a Flask app
app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    """
    This function creates a connection to our SQLite database.
    SQLite is a simple database that saves data in a file (notes.db).
    """
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row  # This lets us access data like a dictionary
    return conn

# Function to create the notes table if it doesn't exist
def init_db():
    """
    This function creates a table called 'notes' in our database
    if it doesn't already exist.
    """
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Route for the home page
@app.route('/')
def index():
    """
    This function runs when someone visits the home page (/).
    It gets all notes from the database and shows them.
    """
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

# Route to add a new note
@app.route('/add', methods=['POST'])
def add_note():
    """
    This function runs when someone submits the form to add a note.
    It saves the new note to the database.
    """
    # Get the title and content from the form
    title = request.form['title']
    content = request.form['content']
    
    # Save to database
    conn = get_db_connection()
    conn.execute('INSERT INTO notes (title, content) VALUES (?, ?)',
                 (title, content))
    conn.commit()
    conn.close()
    
    # Redirect back to the home page
    return redirect(url_for('index'))

# Route to delete a note
@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    """
    This function deletes a note by its ID.
    The <int:note_id> means we expect a number in the URL.
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    init_db()  # Create the database table
    app.run(debug=True)  # Start the web server