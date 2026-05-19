# API Testing Framework 🧪

פרויקט בדיקות API אוטומטיות בשפת Python.

## טכנולוגיות
- Python 3.x
- pytest
- requests
- allure-pytest

## מבנה הפרויקט
api_testing_project/
├── config/
│   ├── settings.py       # הגדרות גלובליות
│   └── logger.py         # הגדרות לוגים
├── clients/
│   └── api_client.py     # תקשורת עם ה־API
├── tests/
│   └── test_posts.py     # בדיקות
├── logs/                 # קבצי לוג
├── allure-results/       # תוצאות גולמיות
├── conftest.py           # הגדרות pytest
├── pytest.ini            # קונפיגורציה של pytest
└── requirements.txt      # ספריות

## התקנה

### 1. שכפל את הפרויקט
git clone <repository-url>
cd api_testing_project

### 2. צור סביבה וירטואלית
python -m venv venv
venv\Scripts\activate

### 3. התקן ספריות
pip install -r requirements.txt

## הרצת בדיקות

### הרץ את כל הבדיקות
pytest tests/ -v

### הרץ עם דו"ח Allure
pytest tests/ -v --alluredir=allure-results
allure serve allure-results

### הרץ בדיקות ספציפיות לפי class
pytest tests/ -v -k "TestGetPosts"
pytest tests/ -v -k "TestCreatePost"

## ה־API שנבדק
https://jsonplaceholder.typicode.com

| Endpoint      | Method | תיאור                  |
|---------------|--------|------------------------|
| /posts        | GET    | שליפת כל הפוסטים       |
| /posts/{id}   | GET    | שליפת פוסט בודד        |
| /posts        | POST   | יצירת פוסט חדש         |
| /posts/{id}   | PUT    | עדכון פוסט קיים        |
| /posts/{id}   | DELETE | מחיקת פוסט             |