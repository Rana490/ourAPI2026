# 🎓 Student & Report Management REST API

A RESTful API developed with **Python and Flask** to manage student records and academic reports. The application provides CRUD operations, JSON-based communication, token-based authentication, access-token refresh, input validation, and structured error handling.

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Objectives](#-objectives)
3. [Technologies Used](#-technologies-used)
4. [Project Structure](#-project-structure)
5. [Installation and Setup](#-installation-and-setup)
6. [Running the Application](#-running-the-application)
7. [API Documentation](#-api-documentation)
8. [Authentication](#-authentication)
9. [Data Models](#-data-models)
10. [Error Handling](#-error-handling)
11. [Testing the API](#-testing-the-api)
12. [Security Considerations](#-security-considerations)
13. [Future Improvements](#-future-improvements)

---

## 📖 Project Overview

This project implements a REST API for managing two main resources: **Students** and **Reports**.

The API allows clients to retrieve, create, update, and delete records through HTTP requests. Data is exchanged in JSON format, making the application suitable for integration with web applications, mobile applications, or other software systems.

In addition to resource management, the API includes an authentication mechanism based on signed tokens. Protected student endpoints require an access token, while refresh tokens allow clients to obtain a new access token without submitting their credentials again.

The project demonstrates fundamental concepts of backend development, REST architecture, HTTP methods, authentication, data validation, and error handling.

## 🎯 Objectives

- Implement a RESTful API using Flask.
- Define Python classes to represent students and reports.
- Perform CRUD operations on application resources.
- Exchange structured data using JSON.
- Protect selected endpoints using token-based authentication.
- Implement access-token expiration and refresh functionality.
- Validate incoming requests and return meaningful HTTP status codes.
- Test API endpoints using an API testing tool such as Postman.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web framework used to implement the API |
| ItsDangerous | Signing and validating authentication tokens |
| REST | Architectural approach for resource management |
| HTTP | Communication protocol |
| JSON | Request and response data format |
| Postman | Manual API testing |
| Git and GitHub | Version control and project hosting |
| Visual Studio Code | Development environment |

## 📁 Project Structure

```text
ourAPI2026/
│
├── app.py             # Flask application, models, routes and logic
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
├── .gitignore         # Files excluded from version control
└── .venv/             # Local virtual environment (not uploaded)
```

The `.venv/` directory is created locally and should not be committed to the Git repository.

## ⚙️ Installation and Setup

### Prerequisites

Before running the project, ensure that the following software is installed:

- Python 3.10 or later
- Git
- Visual Studio Code (recommended)
- Postman (recommended for testing)

### 1. Clone the repository

```bash
git clone https://github.com/Rana490/ourAPI2026.git
cd ourAPI2026
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

Using PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, the following command can temporarily allow activation in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains the Python packages required by the application.

## ▶️ Running the Application

Start the Flask development server with:

```bash
python app.py
```

The API should become accessible at:

**Base URL:** `http://127.0.0.1:5000`

Keep the terminal running while sending requests. Press `Ctrl + C` to stop the server.

> **Note:** Flask's development server is intended for local development and testing, not production deployment.

---

## 📡 API Documentation

All endpoints use the base URL:

```text
http://127.0.0.1:5000
```

Requests containing a body should generally use the following header:

```http
Content-Type: application/json
```

### 1. Authentication endpoints

| Method | Endpoint | Description | Expected response |
|---|---|---|---|
| POST | `/auth/token` | Authenticate and obtain tokens | `200 OK` |
| POST | `/auth/refresh` | Obtain a new access token | `200 OK` |

### 2. Student endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/students` | Retrieve all students | Required |
| GET | `/students/<student_id>` | Retrieve a student by ID | Required |
| POST | `/students` | Create a new student | Not required in the current implementation |
| PUT | `/students/<student_id>` | Update an existing student | Required |
| DELETE | `/students/<student_id>` | Delete a student | Required |

### 3. Report endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/reports` | Retrieve all reports | Not required in the current implementation |
| GET | `/reports/<report_id>` | Retrieve a report by ID | Not required in the current implementation |
| POST | `/reports` | Create a new report | Not required in the current implementation |
| PUT | `/reports/<report_id>` | Update an existing report | Not required in the current implementation |
| DELETE | `/reports/<report_id>` | Delete a report | Not required in the current implementation |

**HTTP method summary**

| Method | Purpose |
|---|---|
| GET | Read resources |
| POST | Create a resource |
| PUT | Update an existing resource |
| DELETE | Remove a resource |

The authentication requirements above describe the current application implementation. They can be changed if the API is extended or deployed in a more restrictive environment.

---

## 🔐 Authentication

The API uses signed tokens to protect selected student endpoints.

### Step 1: Obtain tokens

Send a `POST` request to:

```text
/auth/token
```

Example JSON request:

```json
{
  "username": "student",
  "password": "change-me"
}
```

A successful response contains an access token and a refresh token. For example, the access-token lifetime is configured to 15 minutes and the refresh-token lifetime to 7 days in the current implementation.

Example response structure:

```json
{
  "access_token": "<access-token>",
  "refresh_token": "<refresh-token>",
  "expires_in": 900
}
```

The token values above are placeholders. Use the actual tokens returned by your application.

### Step 2: Access a protected endpoint

To retrieve students, include the access token in the HTTP `Authorization` header:

```http
Authorization: Bearer <access-token>
```

For example:

```text
GET /students
```

Requests with missing, invalid, or expired access tokens should be rejected.

### Step 3: Refresh an access token

Send a `POST` request to:

```text
/auth/refresh
```

Request body:

```json
{
  "refresh_token": "<your-refresh-token>"
}
```

If the refresh token is valid and has not expired, the API returns a new access token.

**Security note:** The username and password shown above are demonstration credentials. They must be replaced with secure configuration before deployment.

---

## 🧩 Data Models

### Student

The `Student` class represents a student record.

| Attribute | Description | Example |
|---|---|---|
| `ID_S` | Unique student identifier | `1` |
| `FN` | First name | `"Sara"` |
| `LN` | Last name | `"Ben Ali"` |
| `DMjr` | Student field stored as an integer in the current implementation | `1` |
| `Level` | Student's academic level | `4` |

Example JSON representation:

```json
{
  "ID_S": 1,
  "FN": "Sara",
  "LN": "Ben Ali",
  "DMjr": 1,
  "Level": 4
}
```

### Report

The `Report` class represents an academic report.

| Attribute | Description | Example |
|---|---|---|
| `ID_R` | Unique report identifier | `1` |
| `Title` | Report title | `"Flask API Report"` |
| `Type` | Report category or type | `"Technical"` |
| `K1` | First report keyword | `"Python"` |
| `K2` | Second report keyword | `"Flask"` |
| `K3` | Third report keyword | `"REST API"` |
| `Release_Date` | Report release date | `"2026-10-20"` |

Example JSON representation:

```json
{
  "ID_R": 1,
  "Title": "Flask API Report",
  "Type": "Technical",
  "K1": "Python",
  "K2": "Flask",
  "K3": "REST API",
  "Release_Date": "2026-10-20"
}
```

The examples illustrate the expected data structure; actual values depend on the records stored in the application.

### Current data storage

The current implementation stores student and report records in Python lists.

This approach is suitable for learning and testing. However, the records are held in memory, meaning changes are not permanently stored and may disappear when the application restarts.

A future version could use a relational database such as SQLite or PostgreSQL.

---

## ✏️ Example Requests

### Create a student

**Request**

```http
POST /students
Content-Type: application/json
```

```json
{
  "FN": "Amira",
  "LN": "Mansour",
  "DMjr": 1,
  "Level": 4
}
```

A successful creation returns `201 Created` and the new student record.

### Update a student

**Request**

```http
PUT /students/1
Authorization: Bearer <access-token>
Content-Type: application/json
```

```json
{
  "Level": 3
}
```

The example updates the student's academic level. Include the required access token when testing this protected endpoint.

### Create a report

**Request**

```http
POST /reports
Content-Type: application/json
```

```json
{
  "Title": "Industrial Biotechnology Report",
  "Type": "Academic",
  "K1": "Biotechnology",
  "K2": "Fermentation",
  "K3": "Industrial Processes",
  "Release_Date": "2026-10-20"
}
```

Use the exact field names expected by the application.

### Delete a report

**Request**

```http
DELETE /reports/1
```

A successful deletion returns `204 No Content` in the current implementation.

---

## ⚠️ Error Handling

The API returns HTTP status codes to indicate the result of a request.

| Status code | Meaning | Example situation |
|---|---|---|
| `200 OK` | Request completed successfully | Retrieving or updating a record |
| `201 Created` | Resource created successfully | Creating a student or report |
| `204 No Content` | Request succeeded without a response body | Deleting a record |
| `400 Bad Request` | Invalid or incomplete request | Missing required student fields |
| `401 Unauthorized` | Authentication failed | Missing, invalid, or expired access token |
| `404 Not Found` | Resource or route not found | Requesting a nonexistent student or report |
| `405 Method Not Allowed` | HTTP method is not supported for the route | Sending an unsupported method |
| `500 Internal Server Error` | Unexpected server-side error | Unhandled application exception |

Example error response:

```json
{
  "error": "Student not found"
}
```

The precise error message depends on the endpoint and the error-handling logic implemented in `app.py`.

---

## 🧪 Testing the API

Postman can be used to test the endpoints manually.

Recommended test scenarios:

| Test | Request | Expected result |
|---|---|---|
| Retrieve all reports | `GET /reports` | `200 OK` |
| Retrieve an existing report | `GET /reports/1` | `200 OK` |
| Retrieve a nonexistent report | `GET /reports/999` | `404 Not Found` |
| Retrieve students without a token | `GET /students` | `401 Unauthorized` |
| Retrieve students with a valid token | `GET /students` | `200 OK` |
| Create a student with missing fields | `POST /students` | `400 Bad Request` |
| Update an existing student with a valid token | `PUT /students/1` | `200 OK` |
| Delete an existing report | `DELETE /reports/1` | `204 No Content` |
| Refresh a valid refresh token | `POST /auth/refresh` | `200 OK` |

For token-protected requests, first obtain a valid access token from `/auth/token`.

If automated tests are added to the project, they can also be executed from the terminal. For example:

```bash
python -m unittest
```

---

## 🛡️ Security Considerations

The project introduces basic authentication concepts, but several improvements are recommended before production use.

- **Secret management:** Store the signing secret and credentials in environment variables or a secure secrets manager.
- **Password protection:** Use securely hashed passwords and avoid storing plaintext credentials.
- **Token expiration:** Validate token signatures, token types, and expiration times on every protected request.
- **Access control:** Apply authentication and authorization consistently to sensitive endpoints.
- **Input validation:** Validate field types, allowed values, and date formats.
- **HTTPS:** Use HTTPS when deploying the API outside a local development environment.
- **Debug mode:** Disable Flask debug mode in production.
- **Persistent storage:** Use a database with appropriate access controls and backup procedures.

The current application is a learning project and should not be considered production-secure without these improvements.

---

## 🚀 Future Improvements

Potential extensions include:

1. **Database integration:** Replace in-memory lists with SQLite or PostgreSQL.
2. **Automated testing:** Add unit tests and integration tests for every endpoint.
3. **API documentation:** Generate interactive documentation using OpenAPI and Swagger.
4. **Pagination and filtering:** Support large datasets and more flexible queries.
5. **Improved authentication:** Add stronger credential handling and more complete token validation.
6. **Role-based access control:** Define permissions for administrators, students, and other users.
7. **Logging and monitoring:** Record important application events and errors.
8. **Deployment:** Deploy the API using a production WSGI server and HTTPS.

---

## 👩‍💻 Author and Project Information

| Field | Information |
|---|---|
| Project | Student & Report Management REST API |
| Type | Educational software development project |
| Backend | Python / Flask |
| Communication format | JSON over HTTP |
| Version control | Git / GitHub |
| Repository | [Rana490/ourAPI2026](https://github.com/Rana490/ourAPI2026) |

---

## 📄 License

This project was developed for educational purposes. No specific open-source license is declared at this time.

