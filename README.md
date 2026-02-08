# 📘 FastAPI Address Book — Complete Documentation

Welcome to the **FastAPI Address Book** project!
This application provides a clean, modular, production-style API for managing addresses including geolocation filtering.

This README includes:

- 🚀 Project Overview
- 📦 Folder Structure
- 🛠 Installation & Setup
- ▶️ Running the Application
- 🔥 API Endpoints (Full List with Examples)
- 🧩 Environment Variables
- 🐳 Docker Instructions
- 📝 Future Improvements

---

# 🚀 **1. Project Overview**

This project is a FastAPI-based Address Book application where users can:

- Create, update, delete addresses.
- Store address details including latitude/longitude.
- Validate all address fields via Pydantic.
- Query nearby addresses based on distance and coordinates.
- Use SQLModel + SQLite for persistence.
- Explore all APIs via Swagger docs.

---

# 📦 **2. Folder Structure**

```
fastapi_address_book/
├── apps/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── logger.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── utils.py
|   |__ geo_service.py
├── requirements.txt
├── Dockerfile
|--
└── README.md
```

---

# 🛠 **3. Installation & Setup**

## **Prerequisites**

- Python 3.9+
- pip package manager
- (Optional) Docker

---

## **3.1 Clone the Repository**

```bash
git clone <your_repo_url>
cd fastapi_address_book
```

---

## **3.2 Create a Virtual Environment**

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## **3.3 Install Dependencies**

```bash
pip install -r requirements.txt
```

If you see an error related to `BaseSettings`, install:

```bash
pip install pydantic-settings
```

---

## **3.4 Configure Environment Variables**

Create `.env` file:

```env
APP_NAME="FastAPI Address Book"
DATABASE_URL="sqlite:///./addresses.db"
LOG_LEVEL="INFO"
```

---

# ▶️ **4. Running the Application**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  or
python -m apps.main
```

Now visit:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

# 🔥 **5. API Endpoints (Full List)**

### Base URL:

```
http://localhost:8000
```

---

## **5.1 Create Address**

### **POST /addresses**

**Request Body:**

```json
{
  "name": "Home",
  "street": "123 Main Street",
  "city": "Berlin",
  "state": "Berlin",
  "country": "Germany",
  "latitude": 52.52,
  "longitude": 13.405
}
```

**Response:** `201 CREATED`

---

## **5.2 Get Address by ID**

### **GET /addresses/{id}**

**Example:**

```
GET /addresses/1
```

---

## **5.3 Update Address (Partial)**

### **PATCH /addresses/{id}**

```json
{
  "city": "New Berlin"
}
```

---

## **5.4 Delete Address**

### **DELETE /addresses/{id}**

Returns: `204 NO CONTENT`

---

## **5.5 Get Nearby Addresses**

### **GET /addresses/nearby?latitude=52.52&longitude=13.405&radius_km=10**

Parameters:

- `latitude` (required)
- `longitude` (required)
- `radius_km` (default 5 km)
- `limit` (default 20)
- `offset` (default 0)

**Example:**

```
GET /addresses/nearby?latitude=52.52&longitude=13.405&radius_km=10
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Home",
    "street": "123 Main Street",
    "city": "Berlin",
    "state": "Berlin",
    "country": "Germany",
    "latitude": 52.52,
    "longitude": 13.405
  }
]
```

## **5.6 Search Address**

### **POST /addresses/search**

Parameters:

**Example:**

```
POST /addresses/search
```

**Request Body:**

```json
{
  "latitude": -90,
  "longitude": -180,
  "distance_km": 1,
  "limit": 100
}
```

**Response:**

````json
[
  {
    "address": {
      "id": 1,
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Antarctic Research Station",
      "street": "Ice Shelf Road",
      "city": "McMurdo Station",
      "state": "Ross Dependency",
      "country": "Antarctica",
      "latitude": -89.999,
      "longitude": -179.999,
      "postal_code": "00001",
      "building_number": "1",
      "apartment": "Lab A",
      "created_at": "2026-02-08T06:31:43.534Z",
      "updated_at": "2026-02-08T06:31:43.534Z"
    },
    "distance_km": 0.111
  }
]

---


---
# 🐳 **6. Running Locally**
```bash
uvicorn apps.main:app --host 0.0.0.0 --port 8000 --reload
 or
python -m apps.main
````

# 🐳 **7. Running with Docker**

### Build image:

```bash
docker build -t fastapi-address-book .
```

### Run container:

```bash
docker run -p 8000:8000 fastapi-address-book
```

Access at:

```
http://localhost:8000/docs
```

---

# 🧩 **8. Technologies Used**

- FastAPI
- SQLModel (SQLAlchemy ORM + Pydantic models)
- SQLite
- Pydantic v2
- Uvicorn
- Docker

---

# 📝 **9. Future Improvements**

✔ Add authentication (JWT or API key)
✔ Add pagination for all list endpoints
✔ Switch SQLite to PostgreSQL with PostGIS
✔ Add Alembic migrations
✔ Add unit tests with pytest

---

# 🎉 You're Ready to Use the API!

If you need a **GitHub Repository**, **Postman Collection**, or **ZIP export**, just let me know!
