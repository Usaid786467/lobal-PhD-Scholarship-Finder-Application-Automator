# 📡 API Documentation

Complete API reference for the PhD Application Automator backend.

**Base URL:** `http://localhost:5000/api`

## Authentication

All API endpoints (except `/auth/register` and `/auth/login`) require JWT authentication.

### Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## 🔐 Authentication Endpoints

### Register User

```http
POST /api/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "name": "John Doe",
  "research_interests": ["Deep Learning", "Manufacturing"],
  "target_countries": ["USA", "UK", "Canada"],
  "phone": "+1234567890",
  "country": "USA"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "research_interests": ["Deep Learning", "Manufacturing"],
    "target_countries": ["USA", "UK", "Canada"]
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Login

```http
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Login successful",
  "user": {...},
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Get Current User

```http
GET /api/auth/me
```

**Response:** `200 OK`
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "research_interests": ["Deep Learning"],
    "has_cv": false
  }
}
```

---

## 🎓 University Endpoints

### List Universities

```http
GET /api/universities?page=1&per_page=20&country=USA&scholarship=true&search=MIT
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 20, max: 100)
- `country` (optional): Filter by country
- `scholarship` (optional): Filter by scholarship availability (true/false)
- `search` (optional): Search in name

**Response:** `200 OK`
```json
{
  "success": true,
  "universities": [
    {
      "id": 1,
      "name": "Massachusetts Institute of Technology",
      "country": "USA",
      "city": "Cambridge",
      "website": "https://mit.edu",
      "has_scholarship": true,
      "scholarship_details": "Full tuition + $40,000 stipend",
      "research_areas": ["AI", "Robotics", "Aerospace"],
      "professor_count": 45
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "total_pages": 8
}
```

### Get Single University

```http
GET /api/universities/1?include_professors=true
```

**Response:** `200 OK`
```json
{
  "success": true,
  "university": {
    "id": 1,
    "name": "MIT",
    "professors": [...]
  }
}
```

### Create University

```http
POST /api/universities
```

**Request Body:**
```json
{
  "name": "Stanford University",
  "country": "USA",
  "city": "Stanford",
  "website": "https://stanford.edu",
  "has_scholarship": true,
  "scholarship_details": "Full funding available",
  "research_areas": ["AI", "ML", "Robotics"]
}
```

---

## 👨‍🏫 Professor Endpoints

### List Professors

```http
GET /api/professors?page=1&university_id=1&accepting_students=true&search=machine learning
```

**Query Parameters:**
- `page` (optional): Page number
- `per_page` (optional): Items per page
- `university_id` (optional): Filter by university
- `accepting_students` (optional): Filter by student acceptance
- `search` (optional): Search in name and research interests

**Response:** `200 OK`
```json
{
  "success": true,
  "professors": [
    {
      "id": 1,
      "name": "Dr. Jane Smith",
      "title": "Professor",
      "email": "jsmith@mit.edu",
      "department": "Mechanical Engineering",
      "research_interests": ["Deep Learning", "Computer Vision"],
      "accepting_students": true,
      "h_index": 45,
      "match_score": null
    }
  ],
  "total": 50,
  "page": 1
}
```

### Create Professor

```http
POST /api/professors
```

**Request Body:**
```json
{
  "university_id": 1,
  "name": "Dr. John Doe",
  "title": "Associate Professor",
  "email": "jdoe@university.edu",
  "department": "Computer Science",
  "research_interests": ["Machine Learning", "AI"],
  "accepting_students": true
}
```

---

## 📝 Application Endpoints

### List User Applications

```http
GET /api/applications?status=sent&page=1
```

**Query Parameters:**
- `status` (optional): Filter by status (draft, sent, delivered, opened, replied, etc.)
- `professor_id` (optional): Filter by professor
- `university_id` (optional): Filter by university

**Response:** `200 OK`
```json
{
  "success": true,
  "applications": [
    {
      "id": 1,
      "professor_id": 1,
      "university_id": 1,
      "status": "sent",
      "applied_date": "2024-01-15T10:30:00",
      "match_score": 85.5
    }
  ],
  "total": 10
}
```

### Create Application

```http
POST /api/applications
```

**Request Body:**
```json
{
  "professor_id": 1,
  "university_id": 1,
  "custom_message": "I am particularly interested in your recent work on...",
  "priority": 1
}
```

### Update Application Status

```http
PATCH /api/applications/1/status
```

**Request Body:**
```json
{
  "status": "replied",
  "response_content": "Thank you for your interest. Please apply through..."
}
```

---

## 📧 Email Endpoints

### List Emails

```http
GET /api/emails?status=draft&page=1
```

**Response:** `200 OK`
```json
{
  "success": true,
  "emails": [
    {
      "id": 1,
      "application_id": 1,
      "to_email": "professor@university.edu",
      "subject": "PhD Opportunity - Research Collaboration",
      "status": "draft",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### Create Email

```http
POST /api/emails
```

**Request Body:**
```json
{
  "application_id": 1,
  "to_email": "professor@university.edu",
  "to_name": "Dr. Smith",
  "subject": "PhD Application",
  "body": "Dear Professor Smith, ..."
}
```

### Email Batches

```http
GET /api/emails/batches
POST /api/emails/batches
GET /api/emails/batches/1
PUT /api/emails/batches/1
DELETE /api/emails/batches/1
```

---

## 📊 Analytics Endpoints

### Dashboard Statistics

```http
GET /api/analytics/dashboard
```

**Response:** `200 OK`
```json
{
  "success": true,
  "statistics": {
    "total_applications": 25,
    "applications_sent": 20,
    "applications_replied": 5,
    "response_rate": 25.0,
    "total_emails": 30,
    "emails_sent": 20,
    "emails_opened": 15,
    "open_rate": 75.0,
    "by_status": {
      "draft": 5,
      "sent": 10,
      "replied": 5
    }
  }
}
```

### Trends Data

```http
GET /api/analytics/trends?days=30
```

**Response:** `200 OK`
```json
{
  "success": true,
  "trends": {
    "applications_per_day": [
      {"date": "2024-01-01", "count": 3},
      {"date": "2024-01-02", "count": 5}
    ],
    "emails_per_day": [...]
  }
}
```

---

## 👤 User Profile Endpoints

### Get Profile

```http
GET /api/user
```

### Update Profile

```http
PUT /api/user
```

**Request Body:**
```json
{
  "name": "John Updated",
  "phone": "+1234567890",
  "country": "USA"
}
```

### Get Preferences

```http
GET /api/user/preferences
```

### Update Preferences

```http
PUT /api/user/preferences
```

**Request Body:**
```json
{
  "email_notifications": true,
  "daily_limit": 50,
  "auto_approve": false
}
```

### Get Research Profile

```http
GET /api/user/research-profile
```

**Response:** `200 OK`
```json
{
  "success": true,
  "profile": {
    "research_interests": ["Deep Learning", "Manufacturing"],
    "target_countries": ["USA", "UK", "Canada"]
  }
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "error": "Error Type",
  "message": "Detailed error message"
}
```

### Common Status Codes

- `200 OK`: Success
- `201 Created`: Resource created
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: No permission
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `500 Internal Server Error`: Server error

---

## Rate Limiting

Default rate limits:
- **100 requests per hour** per user
- Can be configured in backend/.env

---

## Examples

### Complete Registration & Login Flow

```bash
# 1. Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123",
    "name": "Test User",
    "research_interests": ["AI", "ML"]
  }'

# Extract access_token from response

# 2. Get current user
curl http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 3. Create university
curl -X POST http://localhost:5000/api/universities \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MIT",
    "country": "USA",
    "has_scholarship": true
  }'

# 4. Get dashboard stats
curl http://localhost:5000/api/analytics/dashboard \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## WebSocket Events (Future)

Coming soon: Real-time updates for email sending progress, application status changes, etc.

---

## Pagination

All list endpoints support pagination:

```http
GET /api/universities?page=2&per_page=50
```

Response includes:
- `total`: Total number of items
- `page`: Current page
- `per_page`: Items per page
- `total_pages`: Total number of pages

---

## Filtering & Search

Most list endpoints support filtering and search:

```http
GET /api/universities?country=USA&search=technology&scholarship=true
GET /api/professors?university_id=1&accepting_students=true
GET /api/applications?status=sent&professor_id=5
```

---

For more examples, see the QUICKSTART.md guide!
