# FinWell API – Personal Finance Wellness Tracker

## Overview
FinWell API is a comprehensive backend service for tracking personal finances, helping users manage transactions, budgets, and financial wellness with JWT authentication and interactive API documentation.

## Features
- User authentication & registration (JWT-based)
- Categorize transactions (income/expense)
- Budget planning with spending tracking
- **Budget Alerts**: Real-time warnings when spending approaches or exceeds budget limits
- Financial reports & analytics with date filtering
- **Currency Conversion**: Live exchange rates for international transactions
- Interactive API documentation with Swagger UI
- **Optimized Performance**: Database query optimization with select_related/prefetch_related

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

## Enhanced Features (Milestone 6)

### Budget Alerts
When creating or updating transactions, the API automatically checks if spending is approaching or exceeding budget limits:

**Alert Thresholds:**
- **Near Limit**: 80% of budget used
- **Exceeded**: Over 100% of budget used

**Example Transaction Response with Alert:**
```json
{
  "id": 5,
  "category": {
    "id": 1,
    "name": "Food",
    "type": "expense"
  },
  "amount": "50.00",
  "date": "2025-08-27",
  "description": "Lunch",
  "budget_alert": {
    "type": "near_limit",
    "message": "Caution: You have used 85.0% of your Food budget. Spent: 850.0, Budget: 1000.0"
  }
}
```

### Currency Conversion
Convert amounts between different currencies using live exchange rates:

`GET /api/convert/?amount=100&from=USD&to=KES`

**Response:**
```json
{
  "amount": 100,
  "from": "USD",
  "to": "KES",
  "converted_amount": 13000,
  "rate": 130
}
```

### Reports & Analytics
Enhanced reporting with date filtering:

**Financial Summary:**
`GET /api/reports/summary/?month=8&year=2025`

**Financial Health Score:**
`GET /api/reports/health-score/`

**Response:**
```json
{
  "score": 75,
  "message": "Good job! You're within most of your budgets."
}
```

### Performance Optimizations
- Database queries optimized with `select_related()` and `prefetch_related()`
- Reduced N+1 query problems for transactions and budgets
- Enhanced API response times for large datasets

## Testing
Run the comprehensive test suite:
```bash
python manage.py test
python manage.py test tests_milestone6  # Enhanced features tests
```