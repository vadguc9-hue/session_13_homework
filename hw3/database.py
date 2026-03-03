import sqlite3

DATABASE_NAME = 'library.db'

def get_db_connection():
    """Helper function to get a database connection."""
    conn = sqlite3.connect(DATABASE_NAME)
    # Return rows as dictionary-like objects
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database with schema and sample data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            pages INTEGER NOT NULL,
            current_page INTEGER DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Want to Read',
            rating INTEGER,
            review TEXT
        )
    ''')

    # Create user settings table for Reading Goals (Advanced feature: 2nd table)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            yearly_goal INTEGER DEFAULT 10
        )
    ''')

    # Insert default goal if missing
    cursor.execute('SELECT COUNT(*) FROM user_settings')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO user_settings (yearly_goal) VALUES (15)')

    # Sample Data (Insert only if books table is empty)
    cursor.execute('SELECT COUNT(*) FROM books')
    if cursor.fetchone()[0] == 0:
        sample_books = [
            ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 310, 310, 'Finished', 5, 'A masterpiece.'),
            ('1984', 'George Orwell', 'Sci-Fi', 328, 328, 'Finished', 4, 'Chilling and prophetic.'),
            ('Dune', 'Frank Herbert', 'Sci-Fi', 412, 150, 'Reading', None, ''),
            ('Project Hail Mary', 'Andy Weir', 'Sci-Fi', 496, 0, 'Want to Read', None, ''),
            ('Atomic Habits', 'James Clear', 'Non-Fiction', 320, 320, 'Finished', 5, 'Highly practical.'),
            ('Sapiens', 'Yuval Noah Harari', 'History', 443, 80, 'Reading', None, ''),
            ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 180, 180, 'Finished', 3, 'A bit overrated.'),
            ('Meditations', 'Marcus Aurelius', 'Philosophy', 200, 0, 'Want to Read', None, ''),
            ('Clean Code', 'Robert C. Martin', 'Technology', 464, 200, 'Reading', None, ''),
            ('Hyperion', 'Dan Simmons', 'Sci-Fi', 482, 0, 'Want to Read', None, '')
        ]
        
        cursor.executemany('''
            INSERT INTO books (title, author, genre, pages, current_page, status, rating, review)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_books)

    conn.commit()
    conn.close()
    print("Database initialized successfully with sample data!")

if __name__ == '__main__':
    init_db()