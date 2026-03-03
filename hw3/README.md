# Personal Library Tracker (Homework 3)

A web-based database application built with Python, Flask, and SQLite. This application allows users to manage their personal book collection, track their reading progress, and monitor their yearly reading goals.

## Features

* **Library Management:** Add, edit, view, and delete books from your personal library.
* **Progress Tracking:** Input the current page you are on, and the app automatically calculates and displays a visual progress bar using Bootstrap 5.
* **Search and Filter:** Search the database by book title or author, and filter the library by reading status ("Want to Read", "Reading", or "Finished").
* **Dashboard Statistics:** View dynamic statistics on the home page, including Total Books, Pages Read, and Average Rating, calculated using SQL aggregate functions.
* **Reading Goals:** Set and update a yearly reading goal. A secondary database table stores this goal and compares it against the total number of finished books.

## Technologies Used

* **Backend:** Python, Flask
* **Database:** SQLite (Relational Database)
* **Frontend:** HTML5, CSS3, Jinja2 Templating
* **Styling:** Bootstrap 5 (Responsive Grid and Components)

## Project Requirements Met

* Incorporates a Python web framework (Flask) with routing.
* Interacts with an SQLite database using SQL queries (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
* Uses a base template and template inheritance via Jinja2.
* Meets the **Advanced Requirements**:
  * Utilizes SQL aggregate functions (e.g., `SUM`, `AVG`, `COUNT`) to generate dashboard statistics.
  * Implements a multiple-table database schema (e.g., standard books table and a separate goals table).

## How to Run the Application

1. **Verify Python is installed:** Ensure you have Python 3.x installed on your computer.
2. **Install Flask:** Open your terminal or command prompt and run:
   ```bash
   pip install flask