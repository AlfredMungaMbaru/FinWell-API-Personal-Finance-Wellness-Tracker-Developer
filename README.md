# FinWell API – Personal Finance Wellness Tracker

## Overview
FinWell API is a backend service for tracking personal finances, helping users manage transactions, budgets, and financial wellness.

## Features
- User authentication & registration
- Categorize transactions (income/expense)
- Budget planning
- Financial reports & analytics

## Tech Stack
- Python
- Django
- Django REST Framework
- PostgreSQL (production), SQLite (development)

## Installation
1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables (see `.env.example`)
5. Run migrations: `python manage.py migrate`

## Running the Project
- Start the development server: `python manage.py runserver`


## API Endpoints

### Register
`POST /api/register/`
**Request:**
```json
{
	"username": "johndoe",
	"email": "john@example.com",
	"password": "yourpassword"
}
```
**Response:**
```json
{
	"id": 1,
	"username": "johndoe",
	"email": "john@example.com"
}
```

### Login
`POST /api/login/`
**Request:**
```json
{
	"username": "johndoe",
	"password": "yourpassword"
}
```
**Response:**
```json
{
	"refresh": "<refresh_token>",
	"access": "<access_token>"
}
```

### Get Profile
`GET /api/profile/` (Auth required)
**Headers:**
`Authorization: Bearer <access_token>`
**Response:**
```json
{
	"id": 1,
	"username": "johndoe",
	"email": "john@example.com",
	"first_name": "",
	"last_name": ""
}
```

### Update Profile
`PUT /api/profile/` (Auth required)
**Headers:**
`Authorization: Bearer <access_token>`
**Request:**
```json
{
	"first_name": "John",
	"last_name": "Doe"
}
```
**Response:**
```json
{
	"id": 1,
	"username": "johndoe",
	"email": "john@example.com",
	"first_name": "John",
	"last_name": "Doe"
}
```
