import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/')
def index():
    query = request.args.get('q', '').strip()
    conn = get_db_connection()
    
    if query:
        # FEATURE 1: SEARCH FUNCTIONALITY
        # Use LIKE with % wildcards for partial matches
        # SQL placeholders (?) prevent SQL injection
        search_pattern = f"%{query}%"
        sql = "SELECT * FROM items WHERE name LIKE ? OR description LIKE ?"
        items = conn.execute(sql, (search_pattern, search_pattern)).fetchall()
    else:
        items = conn.execute('SELECT * FROM items').fetchall()
    
    count = len(items)
    conn.close()
    return render_template('index.html', items=items, query=query, count=count)

@app.route('/dashboard')
def dashboard():
    # FEATURE 4: STATISTICS DASHBOARD
    conn = get_db_connection()
    
    # Total count
    total = conn.execute('SELECT COUNT(*) FROM items').fetchone()[0]
    
    # Average rating
    avg_rating = conn.execute('SELECT ROUND(AVG(rating), 1) FROM items').fetchone()[0]
    
    # Count by category
    categories = conn.execute('SELECT category, COUNT(*) as count FROM items GROUP BY category').fetchall()
    
    # Top 5 items
    top_items = conn.execute('SELECT name, rating FROM items ORDER BY rating DESC LIMIT 5').fetchall()
    
    conn.close()
    return render_template('dashboard.html', total=total, avg=avg_rating, categories=categories, top_items=top_items)

if __name__ == '__main__':
    app.run(debug=True)