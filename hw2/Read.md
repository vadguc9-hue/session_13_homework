1. Which features did you add?
I went with Search Functionality and a Statistics Dashboard. I wanted the app to feel less like a static list and more like a tool where you can actually find stuff and see what's going on with the data.

2. What SQL queries power each feature?
I kept all the logic inside the SQL queries to keep things fast:

Search: I used LIKE with placeholders so users can search for partial words (like "choc" for chocolate) without the app being vulnerable to SQL injection.

SELECT * FROM items WHERE name LIKE ? OR description LIKE ?

Stats: I used COUNT, AVG, and GROUP BY to crunch the numbers for the dashboard.

SELECT category, COUNT(*) FROM items GROUP BY category (for the category breakdown).

SELECT name, rating FROM items ORDER BY rating DESC LIMIT 5 (to get the top-rated items).

3. What was challenging?
The hardest part was definitely the database setup. I kept hitting a "no such table" error because I forgot that schema.sql is just a text file—it doesn't do anything until you actually run it through Python to build the .db file. Once I got the init_db.py script working and the folders named correctly, everything clicked.

4. How do these features improve the app?
The search bar makes the app actually usable. No one wants to scroll through 50 items to find one thing. The dashboard is great because it gives you a "bird's eye view"—you can see the average quality and which categories are the most popular without doing the math yourself.

5. What would you add next?
I’d probably add Pagination next. It’s the last piece of the puzzle for a professional-feeling app. Having 10 items per page would make the layout look way cleaner than one giant scrolling list.