# **API Readme**
This document provides information about the API application and its usage.

# Introduction
This repository contains a RESTful API built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. The API provides endpoints for user authentication, data retrieval, and data manipulation.

# Requirements

- Python (version 3.10 or higher)
- MongoDB (version 4.4 or higher)
- Pip

# Installation

1. Clone this repository using the following command:
```git clone https://github.com/gurmatsinghsour/API-.```
2. Navigate to the project directory using the command:
```cd fastapi-mongodb-api```
3. Install the required Python packages using the pip command:
```pip install -r requirements.txt```

### **Running the API**
To start the API server, run the following command in the project directory:
``` 
uvicorn main:app --reload
```
The **--reload** flag enables auto-reloading of the application when changes are made to the code.
<br><br> OR <br><br>
Execute the following command:
```
python main.py
```

Note: you can replace **mongodb://localhost:27017/users** with the URL of your MongoDB server.

Start the application by executing the main.py file.

# API Endpoints

The following endpoints are available:

### **GET /users**
This endpoint returns a list of all users.

Response
```
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": "611f177e57ee053920c6d1f4",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "createdAt": "2021-08-19T17:50:38.727Z",
        "updatedAt": "2021-08-19T17:50:38.727Z"
    },
    {
        "id": "611f1a9b57ee053920c6d1f5",
        "name": "Jane Doe",
        "email": "janedoe@example.com",
        "createdAt": "2021-08-19T18:04:11.729Z",
        "updatedAt": "2021-08-19T18:04:11.729Z"
    }
]
```
### **POST /users**

This endpoint creates a new user.

**Request**


```
POST /users
Content-Type: application/json

{
    "name": "John Doe",
    "email": "johndoe@example.com"
}

```

**Response**

```

HTTP/1.1 201 Created
Content-Type: application/json

{
    "id": "611f177e57ee053920c6d1f4",
    "name": "John Doe",
    "email": "johndoe@example.com",
    "createdAt": "2021-08-19T17:50:38.727Z",
    "updatedAt": "2021-08-19T17:50:38.727Z"
}

```
### **GET /users/:id**
This endpoint returns a single user by ID.

Response

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "611f177e57ee053920c6d1f4",
    "name": "John Doe",
    "email": "johndoe@example.com",
    "createdAt": "2021-08-19T17:50:38.727Z",
    "updatedAt": "2021-08-19T17:50:38.727Z"
}

```

## **PUT /users/:id**
This endpoint updates a user by ID.

Request


```PUT /users/611f177e57ee053920c6d1f4```

# Authentication
To perform CRUD (Create, Read, Update, Delete) operations on the /users and /posts endpoints, users must be authenticated by providing an authentication token in the request header. The token can be obtained by signing in to an existing account using the /users/login endpoint.

# Sign-in, Sign-up, and Reset Password

The API supports user authentication through sign-in, sign-up, and reset password functions. Users can sign up for a new account by providing their username and password. The API stores the password in a hashed format using the bcrypt library, which is a one-way cryptographic hash function.

Upon successful registration, the API returns an authentication token that the user can use to access protected endpoints.

To sign in to an existing account, the user must provide their username and password. The API verifies the provided password by hashing it using bcrypt and comparing it to the stored hashed password. If the credentials are valid, the API returns an authentication token that can be used to access protected endpoints.

If a user forgets their password, they can reset it by navigating to the reset password link and then providing the required details.

# FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. It is designed to be easy to use and understand, while also providing high performance and scalability.

FastAPI uses the OpenAPI standard (formerly known as Swagger) to provide a well-documented API that can be easily consumed by other applications. It also provides automatic data validation and serialization, making it easier to build reliable and robust APIs.

In this project, FastAPI is used to define and implement the API endpoints, as well as handle authentication and data storage using MongoDB.

# Contribution
Contributions are welcome! If you find a bug or have a feature request, please create an issue on the repository. If you would like to contribute code, please fork the repository and submit a pull request.
