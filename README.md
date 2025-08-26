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

### Create Category
`POST /api/categories/` (Auth required)
**Headers:**
`Authorization: Bearer <access_token>`
**Request:**
```json
{
  "name": "Groceries",
  "type": "expense"
}
```
**Response:**
```json
{
  "id": 1,
  "name": "Groceries",
  "type": "expense"
}
```

### List Categories
`GET /api/categories/` (Auth required)
**Headers:**
`Authorization: Bearer <access_token>`
**Response:**
```json
[
  {
    "id": 1,
    "name": "Groceries",
    "type": "expense"
  },
  {
    "id": 2,
    "name": "Salary",
    "type": "income"
  }
]
```

### Create Transaction
`POST /api/transactions/` (Auth required)
**Headers:**
`Authorization: Bearer <access_token>`
**Request:**
```json
{
  "category_id": 1,
  "amount": 25.50,
  "date": "2025-08-24",
  "description": "Supermarket shopping"
}
```
**Response:**
```json
{
  "id": 1,
  "category": {
    "id": 1,
    "name": "Groceries",
    "type": "expense"
  },
  "amount": "25.50",
  "date": "2025-08-24",
  "description": "Supermarket shopping"
}
```

### List Transactions
`GET /api/transactions/` (Auth required)
**Headers:**
`Authorization: Bearer <access_token>`
**Response:**
```json
[
  {
    "id": 1,
    "category": {
      "id": 1,
      "name": "Groceries",
      "type": "expense"
    },
    "amount": "25.50",
    "date": "2025-08-24",
    "description": "Supermarket shopping"
  }
]
```

### Create Budget
`POST /api/budgets/` (Auth required)
**Headers:**
`Authorization: Bearer <access_token>`
**Request:**
```json
{
  "category_id": 1,
  "amount": 500.00,
  "period": "2025-08"
}
```
**Response:**
```json
{
  "id": 1,
  "category": {
    "id": 1,
    "name": "Food",
    "type": "expense"
  },
  "amount": "500.00",
  "period": "2025-08",
  "total_spent": "120.50",
  "remaining": "379.50"
}
```

### List Budgets with Spending
`GET /api/budgets/` (Auth required)
**Headers:**
`Authorization: Bearer <access_token>`
**Response:**
```json
[
  {
    "id": 1,
    "category": {
      "id": 1,
      "name": "Food",
      "type": "expense"
    },
    "amount": "500.00",
    "period": "2025-08",
    "total_spent": "120.50",
    "remaining": "379.50"
  },
  {
    "id": 2,
    "category": {
      "id": 2,
      "name": "Transportation",
      "type": "expense"
    },
    "amount": "200.00",
    "period": "2025-08",
    "total_spent": "50.00",
    "remaining": "150.00"
  }
]
```

### Update Budget
`PUT /api/budgets/{id}/` (Auth required)
**Headers:**
`Authorization: Bearer <access_token>`
**Request:**
```json
{
  "category_id": 1,
  "amount": 600.00,
  "period": "2025-08"
}
```
**Response:**
```json
{
  "id": 1,
  "category": {
    "id": 1,
    "name": "Food",
    "type": "expense"
  },
  "amount": "600.00",
  "period": "2025-08",
  "total_spent": "120.50",
  "remaining": "479.50"
}
```