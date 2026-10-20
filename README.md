
# ourAPI2026

A REST API built using Python and Flask.

## Data classes

### Student
- ID_S
- FN (first name)
- LN (last name)
- DMjr (double major: 0 or 1)
- Level (1, 2, 3 or 4)

### Report
- ID_R
- Title
- Type
- K1, K2, K3 (keywords)
- Release_Date

## Features
- GET all records and retrieve by ID
- POST new students and reports
- PUT and DELETE operations
- Bearer token authentication
- Access-token refresh and expiration
- Error handling

## Installation
1. Create a virtual environment.
2. Install dependencies:
   pip install -r requirements.txt
3. Configure the authentication credentials and signing secret.
4. Run the API:
   python app.py

## Local server
http://127.0.0.1:5000
