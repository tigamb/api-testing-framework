# API Testing Framework 🧪

פרויקט בדיקות API אוטומטיות מקצה לקצה בשפת Python.

---

## טכנולוגיות

| כלי | שימוש |
|-----|-------|
| Python 3.11 | שפת תכנות |
| pytest | הרצת בדיקות |
| requests | תקשורת HTTP |
| allure-pytest | דוחות ויזואליים |
| python-dotenv | משתני סביבה |
| pytest-html | דוח HTML |
| yagmail | שליחת מייל |
| Docker | הרצה ב־container |
| GitHub Actions | CI/CD בענן |

---

## מבנה הפרויקט

```
api_testing_project/
│
├── .github/
│   └── workflows/
│       └── tests.yml          ← GitHub Actions
│
├── config/
│   ├── __init__.py
│   ├── settings.py            ← הגדרות גלובליות + .env
│   └── logger.py              ← הגדרות לוגים
│
├── clients/
│   ├── __init__.py
│   └── api_client.py          ← תקשורת עם API + error handling
│
├── tests/
│   ├── __init__.py
│   ├── test_posts.py          ← בדיקות Posts
│   ├── test_users.py          ← בדיקות Users
│   ├── test_comments.py       ← בדיקות Comments + E2E
│   ├── test_auth.py           ← בדיקות Authentication
│   ├── test_data_driven.py    ← בדיקות Data-Driven מ־CSV
│   └── test_performance.py    ← בדיקות ביצועים
│
├── test_data/
│   ├── login_data.csv         ← נתוני בדיקות התחברות
│   └── posts_data.csv         ← נתוני בדיקות פוסטים
│
├── utils/
│   ├── __init__.py
│   ├── csv_reader.py          ← קריאת נתונים מ־CSV
│   └── email_reporter.py      ← שליחת דוח במייל
│
├── postman/
│   └── api_testing.postman_collection.json  ← Postman Collection
│
├── logs/                      ← קבצי לוג (לא ב־GitHub)
├── allure-results/            ← תוצאות גולמיות (לא ב־GitHub)
│
├── .env                       ← משתני סביבה (לא ב־GitHub)
├── .env.example               ← דוגמה למשתנים
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── conftest.py                ← fixtures
├── pytest.ini                 ← קונפיגורציה
├── requirements.txt           ← ספריות
└── README.md
```

---

## התקנה

### 1. שכפל את הפרויקט
```bash
git clone https://github.com/tigamb/api-testing-framework.git
cd api-testing-framework
```

### 2. צור סביבה וירטואלית
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. התקן ספריות
```bash
pip install -r requirements.txt
```

### 4. הגדר משתני סביבה
העתק את `.env.example` ל־`.env` ומלא את הערכים:
```bash
copy .env.example .env
```

```
BASE_URL=https://jsonplaceholder.typicode.com
REQRES_URL=https://reqres.in/api
REQRES_API_KEY=your_api_key_here
TIMEOUT=10
EMAIL_SENDER=your_gmail@gmail.com
EMAIL_RECEIVER=your_gmail@gmail.com
EMAIL_PASSWORD=your_app_password
```

---

## הרצת בדיקות

### הרץ את כל הבדיקות
```bash
pytest tests/ -v
```

### הרץ עם דוח Allure
```bash
pytest tests/ -v --alluredir=allure-results
allure serve allure-results
```

### הרץ עם דוח HTML
```bash
pytest tests/ -v --html=report.html --self-contained-html
```

### הרץ קובץ ספציפי
```bash
pytest tests/test_posts.py -v
pytest tests/test_auth.py -v
pytest tests/test_performance.py -v
```

### הרץ בדיקות לפי class
```bash
pytest tests/ -v -k "TestGetPosts"
pytest tests/ -v -k "TestAuthentication"
pytest tests/ -v -k "TestPerformance"
```

---

## הרצה עם Docker

### בנה את ה־image
```bash
docker build -t api-testing .
```

### הרץ בדיקות ב־container
```bash
docker run --rm \
  -v ${PWD}/allure-results:/app/allure-results \
  api-testing \
  pytest tests/ -v --alluredir=allure-results
```

### הרץ עם Docker Compose
```bash
docker compose up --build
```

---

## ה־APIs שנבדקים

### JSONPlaceholder
```
https://jsonplaceholder.typicode.com
```

| Endpoint | Method | תיאור |
|----------|--------|-------|
| /posts | GET | שליפת כל הפוסטים |
| /posts/{id} | GET | שליפת פוסט בודד |
| /posts | POST | יצירת פוסט חדש |
| /posts/{id} | PUT | עדכון פוסט קיים |
| /posts/{id} | DELETE | מחיקת פוסט |
| /users | GET | שליפת כל המשתמשים |
| /users/{id} | GET | שליפת משתמש בודד |
| /users/{id}/posts | GET | פוסטים של משתמש |
| /comments | GET | שליפת כל התגובות |
| /posts/{id}/comments | GET | תגובות של פוסט |

### Reqres
```
https://reqres.in/api
```

| Endpoint | Method | תיאור |
|----------|--------|-------|
| /login | POST | התחברות |
| /register | POST | הרשמה |
| /users | GET | שליפת משתמשים |

---

## סוגי הבדיקות

| סוג | תיאור |
|-----|-------|
| Happy Path | תרחישים תקינים |
| Negative | תרחישים שגויים ומקרי קצה |
| E2E Flow | שרשרת של מספר endpoints |
| Parametrize | ריצות מרובות עם קלטים שונים |
| Data-Driven | נתונים מקובץ CSV |
| Authentication | טוקנים ואבטחה |
| Performance | זמני תגובה ועקביות |

---

## מספרים

| | כמות |
|---|---|
| קבצי בדיקות | 6 |
| בדיקות סה"כ | ~80 |
| APIs שנבדקו | 2 |
| סוגי בדיקות | 7 |

---

## GitHub Actions

הבדיקות רצות אוטומטית בענן בכל `git push` ל־`main`.

הגדר את ה־Secrets הבאים ב־GitHub:
```
REQRES_API_KEY  ← API Key של reqres.in
```

---

## Postman Collection

ייבא את הקובץ `postman/api_testing.postman_collection.json` ל־Postman
לקבלת כל הבקשות מאורגנות ומוכנות לשימוש.
