BackendProjectv2

This project is a Flask-based API for managing song data with a PostgreSQL database. It also includes functionalities for importing JSON data into the database and testing the API.

Getting Started

Prerequisites
Ensure you have the following installed on your machine:
    Python 3.x
    PostgreSQL
    Git

1. Clone the repository
git clone git@github.com:Chiragjethwa6/backend_assignment.git
cd backend_assignment/baclend_app 

2. Set up a virtual environment
python -m venv venv
for bash use, venv/bin/activate
for Windows use, venv/Scripts/activate

3. Install dependencies
To install the required dependencies using requirements.txt:
pip install -r requirements.txt

4. Configure environment variables
Create a .env file in the backend directory with the following variables:
DB_USER=<your-database-username>
DB_PASSWORD=<your-database-password>
DB_HOST=<your-database-host>
DB_NAME=<your-database-name>

5. Import JSON data into the database
To import song data from the JSON file (playlist.json) into the database, run the import_json.py script:
python import_json.py

6. Run the Flask application
After setting up the environment and importing the data, run the Flask app:
flask run
The app will be available at: http://127.0.0.1:5000/

7. Running tests
run the unit tests using the test_app.py file:
python -m unittest test_app.py

Project Structure
backendprojectv2/
│
├── backend/
│   ├── app.py               # Main Flask application
│   ├── config.py            # Configuration file for PostgreSQL
│   ├── models.py            # Song model definition
│   ├── requirements.txt     # Python package dependencies
│   ├── test_app.py          # Unit tests for the API
│   ├── .env                 # Environment variables file
│   ├── import_json.py       # Script to import song data from JSON to the database
│   └── playlist.json        # JSON file containing the song data
├── README.md                # Project documentation

Important Note
In the original SQL table, there was a column named class. Since class is a reserved keyword in Python, it has been renamed to classes in the model and playlist.json to avoid conflicts with Python syntax.

API Endpoints
GET /api/songs - Fetches all songs or paginated list of songs.
GET /api/songs/<title> - Fetches a song by its title.
PUT /api/songs/rate/<id> - Updates the star rating of a song by its ID.