# 🚀 FastAPI Address Book

A production-ready REST API for managing addresses with geolocation features. This application allows you to store, retrieve, and query addresses with support for proximity-based searches using latitude/longitude coordinates.

## ✨ Features

- **Complete CRUD Operations**: Create, read, update, and delete addresses
- **Geolocation Search**: Find addresses within a specified radius from given coordinates
- **Robust Validation**: Pydantic models ensure data integrity
- **SQL Database**: SQLite persistence with SQLModel ORM
- **RESTful API**: Clean, intuitive endpoints following REST conventions
- **Auto-generated Documentation**: Interactive API docs with Swagger UI and ReDoc
- **Docker Support**: Easy containerized deployment
- **Production-ready**: Structured logging, configuration management, error handling

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- (Optional) Docker & Docker Compose

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd fastapi_address_book
```

### 2. Set Up Virtual Environment

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the project root:

```env
APP_NAME="FastAPI Address Book"
DATABASE_URL="sqlite:///./addresses.db"
LOG_LEVEL="INFO"
```

## 🏃‍♂️ Running the Application

### Development Mode

```bash
uvicorn apps.main:app --host 0.0.0.0 --port 8000 --reload
```

Or:

```bash
python -m apps.main
```

### Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **API Base URL**: http://localhost:8000

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t fastapi-address-book .
  or
docker build --no-cache
```

### Run the Container

```bash
docker run -p 8000:8000 fastapi-address-book
```

### Docker Compose

```bash
docker compose up -d
docker compose down
```

**Docker Prune command**

```bash
docker system prune -a
docker volume prune -a
```

## 📚 API Reference

All endpoints return JSON responses. Successful responses use appropriate HTTP status codes (200, 201, 204). Errors return detailed JSON error messages.

### Base URL

```
http://localhost:8000
```

### Endpoints

#### 1. Create Address

**POST** `/addresses`

Create a new address entry.

**Request Body:**

```json
{
  "name": "Home",
  "street": "123 Main Street",
  "city": "Berlin",
  "state": "Berlin",
  "country": "Germany",
  "latitude": 52.52,
  "longitude": 13.405,
  "postal_code": "10115",
  "building_number": "123",
  "apartment": "Apt 4B"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Home",
  "street": "123 Main Street",
  "city": "Berlin",
  "state": "Berlin",
  "country": "Germany",
  "latitude": 52.52,
  "longitude": 13.405,
  "postal_code": "10115",
  "building_number": "123",
  "apartment": "Apt 4B",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

#### 2. Get Address by ID

**GET** `/addresses/{id}`

Retrieve a specific address by its ID.

**Path Parameters:**

- `id` (integer): Address ID

**Example:**

```
GET /addresses/1
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Home",
  "street": "123 Main Street",
  "city": "Berlin",
  "state": "Berlin",
  "country": "Germany",
  "latitude": 52.52,
  "longitude": 13.405,
  "postal_code": "10115",
  "building_number": "123",
  "apartment": "Apt 4B",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

#### 3. Update Address

**PATCH** `/addresses/{id}`

Partially update an existing address.

**Path Parameters:**

- `id` (integer): Address ID

**Request Body:**

```json
{
  "city": "New Berlin",
  "postal_code": "10116"
}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Home",
  "street": "123 Main Street",
  "city": "New Berlin",
  "state": "Berlin",
  "country": "Germany",
  "latitude": 52.52,
  "longitude": 13.405,
  "postal_code": "10116",
  "building_number": "123",
  "apartment": "Apt 4B",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

---

#### 4. Delete Address

**DELETE** `/addresses/{id}`

Remove an address from the database.

**Path Parameters:**

- `id` (integer): Address ID

**Example:**

```
DELETE /addresses/1
```

**Response:** `204 No Content`

---

#### 5. Get Nearby Addresses

**GET** `/addresses/nearby`

Find addresses within a specified radius from given coordinates.

**Query Parameters:**

- `latitude` (float, required): Center point latitude (-90 to 90)
- `longitude` (float, required): Center point longitude (-180 to 180)
- `radius_km` (float, optional): Search radius in kilometers (default: 5)
- `limit` (integer, optional): Maximum number of results (default: 20, max: 100)
- `offset` (integer, optional): Pagination offset (default: 0)

**Example:**

```
GET /addresses/nearby?latitude=52.5200&longitude=13.4050&radius_km=10&limit=10
```

**Response:** `200 OK`

```json
[
  {
    "address": {
      "id": 1,
      "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Home",
      "street": "123 Main Street",
      "city": "Berlin",
      "state": "Berlin",
      "country": "Germany",
      "latitude": 52.52,
      "longitude": 13.405,
      "postal_code": "10115",
      "building_number": "123",
      "apartment": "Apt 4B",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    },
    "distance_km": 0.0
  },
  {
    "address": {
      "id": 2,
      "uuid": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
      "name": "Office",
      "street": "456 Business Ave",
      "city": "Berlin",
      "state": "Berlin",
      "country": "Germany",
      "latitude": 52.53,
      "longitude": 13.41,
      "postal_code": "10117",
      "building_number": "456",
      "apartment": null,
      "created_at": "2024-01-15T11:30:00Z",
      "updated_at": "2024-01-15T11:30:00Z"
    },
    "distance_km": 1.2
  }
]
```

---

#### 6. Search Addresses (Advanced)

**POST** `/addresses/search`

Advanced search with flexible filtering criteria.

**Request Body:**

```json
{
  "latitude": -89.999,
  "longitude": -179.999,
  "distance_km": 1.0,
  "limit": 100,
  "name_contains": "Research",
  "city": "McMurdo Station"
}
```

**Response:** `200 OK`

```json
[
  {
    "address": {
      "id": 3,
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
      "created_at": "2024-01-15T12:30:00Z",
      "updated_at": "2024-01-15T12:30:00Z"
    },
    "distance_km": 0.111
  }
]
```

## 🗂️ Project Structure

```
fastapi_address_book/
├── apps/
│   ├── __init__.py          # Package initialization
│   ├── main.py             # FastAPI application instance
│   ├── config.py           # Configuration management
│   ├── database.py         # Database setup and session management
│   ├── logger.py           # Logging configuration
│   ├── models.py           # SQLModel database models
│   ├── schemas.py          # Pydantic schemas for validation
│   ├── crud.py             # CRUD operations
│   ├── utils.py            # Utility functions
│   └── geo_service.py      # Geolocation calculations
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── .env.example           # Environment variables template
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable       | Description                                 | Default                    |
| -------------- | ------------------------------------------- | -------------------------- |
| `APP_NAME`     | Application name                            | "FastAPI Address Book"     |
| `DATABASE_URL` | Database connection URL                     | "sqlite:///./addresses.db" |
| `LOG_LEVEL`    | Logging level (DEBUG, INFO, WARNING, ERROR) | "INFO"                     |

### Database

The application uses SQLite by default for simplicity. For production, consider switching to PostgreSQL with PostGIS for better geolocation performance.

## 🧪 Testing the API

### Using cURL

Create an address:

```bash
curl -X POST "http://localhost:8000/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Location",
    "street": "123 Test Street",
    "city": "Test City",
    "state": "Test State",
    "country": "Test Country",
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

Find nearby addresses:

```bash
curl "http://localhost:8000/addresses/nearby?latitude=40.7128&longitude=-74.0060&radius_km=5"
```

### Using Python (requests library)

```python
import requests

# Create address
response = requests.post("http://localhost:8000/addresses", json={
    "name": "Python Test",
    "street": "456 Python Ave",
    "city": "Code City",
    "state": "Debug State",
    "country": "Testland",
    "latitude": 40.7589,
    "longitude": -73.9851
})
print(response.json())
```

## 🚀 Deployment

### Production Considerations

1. **Database**: Switch from SQLite to PostgreSQL with PostGIS extension
2. **Authentication**: Add JWT or API key authentication
3. **Caching**: Implement Redis for frequently accessed data
4. **Monitoring**: Add health checks and metrics endpoints
5. **Security**: Enable CORS, rate limiting, and input sanitization

### Deployment Options

**Option 1: Traditional Server**

```bash
# Install production dependencies
pip install -r requirements.txt

python -m apps.main

# Run with production server
uvicorn apps.main:app --host 0.0.0.0 --port 8000 \
  --workers 4 \
  --log-level warning
```

**Option 2: Docker in Production**

```bash
docker run -d \
  --name address-book \
  -p 8000:8000 \
  -v ./data:/app/data \
  -e DATABASE_URL="sqlite:///./data/addresses.db" \
  fastapi-address-book
```

## 📈 Future Enhancements

- [ ] User authentication and authorization
- [ ] Pagination for all list endpoints
- [ ] PostgreSQL with PostGIS support
- [ ] Database migrations with Alembic
- [ ] Comprehensive test suite
- [ ] Rate limiting
- [ ] API versioning
- [ ] WebSocket support for real-time updates
- [ ] Export/import functionality (CSV, JSON)
- [ ] Address verification via external APIs
- [ ] Batch operations for bulk address management

## 🐛 Troubleshooting

### Common Issues

1. **Database connection errors**
   - Ensure the database file is writable
   - Check DATABASE_URL in .env file

2. **Import errors**
   - Verify virtual environment is activated
   - Run `pip install -r requirements.txt` again

3. **Port already in use**
   - Change port: `--port 8080`
   - Find and kill process using port 8000

4. **Geolocation queries not returning results**
   - Verify latitude (-90 to 90) and longitude (-180 to 180) ranges
   - Check that addresses have valid coordinates

### Getting Help

Check the logs for detailed error messages:

```bash
# View application logs
docker logs <container_id>

# Or check the console output if running locally
```

## 📄 License

This project is available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework
- [SQLModel](https://sqlmodel.tiangolo.com/) for the ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- The Haversine formula for distance calculations

---

**Happy Coding!** 🎉
