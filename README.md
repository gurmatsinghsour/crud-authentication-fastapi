# **API Readme**
This document provides information about the API application and its usage.

# Introduction
This API provides a simple RESTful interface for managing user data. It allows creating, reading, updating, and deleting users.

# Requirements

Python (version 3.10 or higher)
MongoDB (version 4.4 or higher)

# Installation

1. Clone this repository using the command git clone https://github.com/gurmatsinghsour/API-.
2. Navigate to the project directory using the command **cd API-**.
3. Install the required dependencies using the command **pip install -r requirements.txt**.
4. Create a .env file in the root directory of the project, and add the following environment variables with your own values

```
PORT=3000
DB_URL=mongodb://localhost:27017/
```

Note: You can replace 3000 with any available port of your choice. Similarly, you can replace mongodb://localhost:27017/users with the URL of your MongoDB server.

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
