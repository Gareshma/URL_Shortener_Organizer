URL Shortener & URL Organizer
=============================

A simple but powerful Flask web application that helps you:

- Shorten long URLs with custom aliases.
- Organize useful links into categories.
- Export links by category to Excel for offline storage.


Features
--------

URL Shortener:
- Generate short URLs with random or custom aliases.
- Track click counts for each shortened URL.
- Copy-to-clipboard button for quick sharing.

URL Organizer:
- Create, edit, and delete categories.
- Add, delete, and restore links inside categories.
- Export all links in a category to an Excel file.
- Clean and modern Bootstrap UI.

Data Persistence:
- SQLite database (urls.db) with SQLAlchemy ORM.


Tech Stack
----------

- Backend: Python, Flask, Flask-SQLAlchemy
- Frontend: HTML, Bootstrap 5, Vanilla JavaScript
- Database: SQLite
- Extras: Pandas + XlsxWriter for Excel export


Project Structure
-----------------

app.py                -> Main Flask app
models.py             -> Database models
config.py             -> Flask configuration
seed.py               -> Optional: populate DB with sample data
urls.db               -> SQLite database
requirements.txt      -> Python dependencies
static/js/category.js -> Category/Link handling JS
templates/            -> HTML templates (base, home, shorten, dashboard, stats, etc.)
README.txt            -> Project documentation


Getting Started
---------------

1. Clone the repository:
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>

2. Create and activate a virtual environment:
   python -m venv venv
   On Windows: venv\Scripts\activate
   On Mac/Linux: source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the app:
   flask run
   OR
   python app.py

The app will be available at:
   http://127.0.0.1:5000


Exporting Links
---------------

- Open the Dashboard.
- Select a category from the dropdown.
- Click the "Export to Excel" button.
- The app will download an .xlsx file named after the selected category 
  (for example: LeetCode_links.xlsx).


Future Improvements
-------------------

- User authentication (login/signup).
- Shareable public pages per category.
- Dark mode toggle.

