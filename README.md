# 🌱 GreenSprig - Django Web Application

GreenSprig is a Django-based platform promoting eco-conscious posts, community interactions, and seasonal gardening knowledge.

## 🚀 Features

- User authentication (signup/login)
- Post creation, editing, and deletion
- Commenting and liking posts
- Category tagging (e.g., seasons)
- Favorites system
- Profile management
- Educational resources section

## 🛠️ Tech Stack

- Python 3.8+
- Django 3.x/4.x
- SQLite (default)
- Taggit for tagging
- Bootstrap (frontend)

## ⚙️ Local Setup

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd greensprig_app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the app** at `http://127.0.0.1:8000/`

## 🧪 Run Tests

```bash
python manage.py test
```

## 🐳 Run with Docker

1. **Build Docker image**
   ```bash
   docker build -t greensprig-app .
   ```

2. **Run container**
   ```bash
   docker run -d -p 8000:8000 greensprig-app
   ```

## 📂 Directory Structure

```
greensprig_app/
├── manage.py
├── greensprig/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── plants/
│   ├── models.py
│   ├── views.py
│   ├── tests.py
│   └── ...
├── templates/
│   ├── home.html
│   └── ...
├── static/
└── requirements.txt
```

## 📄 License

MIT License – Feel free to use, extend, and contribute!