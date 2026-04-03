# ZenAIStore

## Setup Instructions

Base url will like this  : http://127.0.0.1:8000/api/

### 1. Clone the repository
```
git clone <your-repo-url>
cd ZenAIStore
```

### 2. Create and activate a virtual environment
```
python3 -m venv room
source room/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Create a `.env` file
Copy `.env.example` to `.env` and fill in your secrets:
```
cp .env.example .env
```

### 5. Run migrations
```
python manage.py migrate
```

### 6. Start Redis (for Celery)
```
redis-server
```

### 7. Start Celery worker
```
celery -A core worker --loglevel=info --concurrency=4
```

### 8. Run the development server
```
python manage.py runserver
```

### 9. Access the API docs (Swagger)
python manage.py collectstatic
Visit: http://localhost:8000/swagger/  
or

Post man collection 

https://www.postman.com/mniloy695-1283389/workspace/zenaistore/collection/47036725-e956f20c-394f-49aa-8746-559a0b5e9f81?action=share&source=copy-link&creator=47036725

---

## API Documentation

- Interactive Swagger UI: `/swagger/`
- Redoc: `/redoc/`
- All endpoints are JWT protected unless otherwise noted.

---

## Environment Variables
See `.env.example` for required variables.

---

## Testing
```
python manage.py test
```

---

## Project Structure

  
- `accounts/` - Custom user model and authentication
- `product/` - Product API, Celery tasks, AI integration
- `core/` - Django settings, celery config

---

## Contact
For questions, contact maintainer@example.com
