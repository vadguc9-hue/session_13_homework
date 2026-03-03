from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = 'super_secret_homework_key'  # Needed for flash messages

# Initialize DB on startup
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    
    # 1. Fetch Statistics Using SQL Aggregate Functions
    stats = conn.execute('''
        SELECT 
            COUNT(id) as total_books,
            SUM(current_page) as pages_read,
            AVG(rating) as avg_rating
        FROM books
    ''').fetchone()
    
    goal = conn.execute('SELECT yearly_goal FROM user_settings LIMIT 1').fetchone()
    
    finished_count = conn.execute("SELECT COUNT(id) FROM books WHERE status = 'Finished'").fetchone()[0]
    
    # 2. Filtering, Searching, and Sorting Logic
    search_query = request.args.get('q', '')
    status_filter = request.args.get('status', '')
    
    # Base query
    query = "SELECT * FROM books WHERE 1=1"
    params = []
    
    # Add SQL LIKE for searching
    if search_query:
        query += " AND (title LIKE ? OR author LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
        
    # Add SQL WHERE for filtering
    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)
        
    # Add SQL ORDER BY for sorting
    query += " ORDER BY id DESC"
    
    books = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('index.html', books=books, stats=stats, goal=goal, finished_count=finished_count, search_query=search_query, status_filter=status_filter)

@app.route('/add', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        pages = request.form['pages']
        status = request.form['status']
        
        # Validation
        if not title or not author or not pages:
            flash('Title, Author, and Pages are required fields!', 'danger')
        else:
            conn = get_db_connection()
            # SQL Injection Prevention using Parameterized Query (?)
            conn.execute('''
                INSERT INTO books (title, author, genre, pages, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, author, genre, pages, status))
            conn.commit()
            conn.close()
            flash(f'"{title}" was successfully added!', 'success')
            return redirect(url_for('index'))
            
    return render_template('add.html')

@app.route('/<int:book_id>')
def view_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    
    if book is None:
        flash('Book not found.', 'danger')
        return redirect(url_for('index'))
        
    return render_template('view.html', book=book)

@app.route('/<int:book_id>/edit', methods=('GET', 'POST'))
def edit_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    
    if book is None:
        conn.close()
        flash('Book not found.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        pages = request.form['pages']
        current_page = request.form['current_page']
        status = request.form['status']
        rating = request.form.get('rating') or None
        review = request.form.get('review', '')
        
        try:
            conn.execute('''
                UPDATE books 
                SET title = ?, author = ?, genre = ?, pages = ?, current_page = ?, 
                    status = ?, rating = ?, review = ?
                WHERE id = ?
            ''', (title, author, genre, pages, current_page, status, rating, review, book_id))
            conn.commit()
            flash('Book successfully updated.', 'success')
            return redirect(url_for('view_book', book_id=book_id))
        except sqlite3.Error as e:
            flash(f'Database error: {e}', 'danger')
        finally:
            conn.close()
            
    conn.close()
    return render_template('edit.html', book=book)

@app.route('/<int:book_id>/delete', methods=('POST',))
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    flash('Book deleted successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/goal', methods=('POST',))
def update_goal():
    goal = request.form['goal']
    conn = get_db_connection()
    conn.execute('UPDATE user_settings SET yearly_goal = ? WHERE id = 1', (goal,))
    conn.commit()
    conn.close()
    flash('Reading goal updated!', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)