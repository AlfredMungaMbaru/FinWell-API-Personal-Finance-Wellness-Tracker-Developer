# FinWell API – Personal Finance Wellness Tracker

## Overview
FinWell API is a comprehensive backend service for tracking personal finances, helping users manage transactions, budgets, and financial wellness with JWT authentication and interactive API documentation.

## Features
- User authentication & registration (JWT-based)
- Categorize transactions (income/expense)
- Budget planning with spending tracking
- Financial reports & analytics
- Interactive API documentation with Swagger UI

## Tech Stack
- Python
- Django
- Django REST Framework
- Django REST Framework SimpleJWT
- drf-spectacular (OpenAPI/Swagger)
- PostgreSQL (production), SQLite (development)

## Installation
1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables (see `.env.example`)
5. Run migrations: `python manage.py migrate`

## Running the Project
- Start the development server: `python manage.py runserver`
- Access the API documentation at: `http://127.0.0.1:8000/api/docs/`

### CORS Configuration
The API includes CORS (Cross-Origin Resource Sharing) support for frontend integration:
- **Development**: All origins are allowed (`CORS_ALLOW_ALL_ORIGINS = True`)
- **Production**: Configure specific allowed origins in `settings.py`:
  ```python
  CORS_ALLOWED_ORIGINS = [
      "http://localhost:3000",
      "https://yourdomain.com",
  ]
  ```
- CORS headers include support for Authorization, Content-Type, and other common headers

## API Documentation

### Interactive Documentation
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/` - Interactive API testing interface
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/` - Alternative documentation view
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/` - Raw JSON/YAML schema

### Authentication Workflow for Swagger
1. **Register a user**: `POST /api/register/`
2. **Get JWT token**: `POST /api/token/`
3. **Authorize in Swagger**: Click "Authorize" button in Swagger UI
4. **Enter token**: Paste `Bearer <your_access_token>` in the authorization field
5. **Test protected endpoints**: Now you can test all authenticated endpoints

### Quick Start Example
```bash
# 1. Register a new user
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "securepass123"}'

# 2. Get JWT token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "securepass123"}'

# 3. Use the token in subsequent requests
curl -X GET http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Bearer <your_access_token>"
```


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