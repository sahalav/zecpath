# Zecpath API Documentation

## Introduction
This project implements authentication using Django REST Framework with JWT.

---

## Authentication Flow
1. User Signup
2. User Login → receives access & refresh token
3. Use access token for protected APIs
4. Refresh token when access token expires

---

## API Endpoints

### 1. Signup
- URL: `/api/signup/`
- Method: POST
- Description: Create new user

Example:
{
  "email": "test@gmail.com",
  "password": "1234",
  "role": "candidate"
}

---

### 2. Login
- URL: `/api/login/`
- Method: POST
- Description: Get JWT tokens

Response:
{
  "access": "token",
  "refresh": "token"
}

---

### 3. Profile (Protected)
- URL: `/api/profile/`
- Method: GET
- Auth: Bearer Token required

---

### 4. User List (Pagination & Search)
- URL: `/api/users/`
- Method: GET

Examples:
- `/api/users/?page=1`
- `/api/users/?search=gmail`

---

### 5. Resume Upload
- URL: `/api/resume/upload/`
- Method: POST
- Auth: Required
- Type: form-data (file upload)

---

## Features Implemented
- JWT Authentication
- Role-based access (Admin, Employer, Candidate)
- Pagination
- Search
- Resume upload

---

## Tech Stack
- Django
- Django REST Framework
- JWT (SimpleJWT)

---

## GitHub Repository
https://github.com/sahalav/zecpath