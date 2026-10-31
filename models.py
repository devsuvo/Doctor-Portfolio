import sqlite3
import os
import random
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'appointments.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ref_code TEXT UNIQUE NOT NULL,
            patient_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            appointment_date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            service_type TEXT NOT NULL,
            patient_type TEXT DEFAULT 'New Consultation',
            notes TEXT,
            status TEXT DEFAULT 'Confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Contact inquiries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            subject TEXT,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            location TEXT NOT NULL,
            rating INTEGER NOT NULL,
            condition TEXT NOT NULL,
            review_text TEXT NOT NULL,
            is_featured INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Health Articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            read_time TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            content TEXT NOT NULL,
            published_date TEXT NOT NULL,
            author TEXT DEFAULT 'Dr. Tanvir Ahmed Chowdhury'
        )
    ''')

    conn.commit()

    # Seed initial reviews
    cursor.execute('DELETE FROM reviews WHERE id <= 8')
    seed_reviews = [
        (
            "Md. Abdul Karim",
            "Sylhet",
            5,
            "Diabetes",
            "I had been struggling with high sugar levels for years. After following Dr. Tanvir's plan, my numbers are finally under control. He explains everything patiently.",
            1
        ),
        (
            "Farhana Akter",
            "Zindabazar",
            5,
            "Thyroid",
            "Very polite and attentive doctor. He took time to understand my thyroid problem and I felt better within weeks.",
            1
        ),
        (
            "Rafiul Islam",
            "Ambarkhana",
            5,
            "Diabetes",
            "Highly recommended for diabetes care. The follow-up advice made a real difference for my father.",
            1
        ),
        (
            "Shamsun Nahar",
            "Subidbazar",
            5,
            "Hypertension",
            "My blood pressure was always high and I was scared. Doctor sir explained everything calmly and now I feel much safer.",
            1
        ),
        (
            "Jahangir Alam",
            "Mirabazar",
            5,
            "General Medicine",
            "He never rushes. I could ask all my questions and got clear answers. A rare quality in a doctor.",
            1
        ),
        (
            "Nusrat Jahan",
            "Upashahar",
            5,
            "Weight Management",
            "I lost 11 kg in 5 months with his guidance, without any extreme diet. Very grateful.",
            1
        ),
        (
            "Kamrul Hasan",
            "Shahjalal Upashahar",
            5,
            "General Medicine",
            "Professional, humble and very knowledgeable. The whole family consults him.",
            1
        ),
        (
            "Sabina Yasmin",
            "Moulvibazar",
            5,
            "Diabetes",
            "Online follow-up saved me a long trip. Very convenient and he still gave full attention.",
            1
        )
    ]
    cursor.executemany('''
        INSERT INTO reviews (patient_name, location, rating, condition, review_text, is_featured)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', seed_reviews)

    # Seed initial articles
    cursor.execute('DELETE FROM articles')
    seed_articles = [
        (
            "7-simple-habits-blood-sugar-control",
            "7 Simple Habits to Keep Your Blood Sugar in Control",
            "Diabetes",
            "4 min",
            "Managing diabetes does not have to be complicated. These seven everyday habits can make a big difference.",
            """Managing blood sugar is mostly about consistency. Here are seven habits that help:

1. **Eat at regular times.** Skipping meals can cause sugar levels to swing up and down.
2. **Control portion size of rice and other carbohydrates.** Fill half your plate with vegetables.
3. **Walk for 30 minutes daily.** Even a brisk walk after meals helps lower sugar.
4. **Drink enough water** throughout the day.
5. **Sleep 7-8 hours.** Poor sleep affects blood sugar.
6. **Take medicines exactly as prescribed.** Never stop on your own.
7. **Check your sugar regularly** and keep a record to show your doctor.

Small, steady changes work better than sudden strict diets. If your sugar remains high despite these habits, please consult your doctor.

---
*Disclaimer: This article is for general awareness only and does not replace personal medical advice.*""",
            "October 2026"
        ),
        (
            "thyroid-problems-6-early-signs",
            "Thyroid Problems: 6 Early Signs You Should Not Ignore",
            "Thyroid",
            "3 min",
            "Thyroid problems often develop slowly. Knowing the early signs can help you get treated sooner.",
            """Thyroid problems are common, especially among women. Watch for these signs:

1. **Unexplained weight gain or weight loss**
2. **Constant tiredness even after rest**
3. **Hair fall and dry skin**
4. **Feeling unusually cold or hot**
5. **Irregular menstrual cycle**
6. **Swelling or fullness in the front of the neck**

Having one of these does not always mean thyroid disease, but if you notice several together, a simple blood test can confirm the cause. Early treatment is simple and effective.

---
*Disclaimer: This article is for general awareness only and does not replace personal medical advice.*""",
            "October 2026"
        ),
        (
            "high-blood-pressure-silent-problem",
            "High Blood Pressure: The Silent Problem and How to Prevent It",
            "Hypertension",
            "4 min",
            "High blood pressure rarely shows symptoms, which is why regular checking matters.",
            """High blood pressure is often called a silent condition because many people feel completely normal while their pressure is high. Over time, it can damage the heart, brain and kidneys.

### How to lower your risk:
1. **Reduce salt in cooking** and avoid extra salt on food.
2. **Limit processed and packaged snacks.**
3. **Maintain a healthy weight.**
4. **Exercise regularly.**
5. **Avoid smoking** and limit tobacco products.
6. **Check your blood pressure** at least once a year, and more often after age 40.

If your readings are repeatedly above normal, do not delay a doctor's visit.

---
*Disclaimer: This article is for general awareness only and does not replace personal medical advice.*""",
            "October 2026"
        ),
        (
            "fasting-and-diabetes-safe-guide",
            "Fasting and Diabetes: A Safe Guide",
            "Diabetes",
            "5 min",
            "Many people with diabetes want to fast safely. Here is what to keep in mind.",
            """If you have diabetes and plan to fast, speak with your doctor well before the fasting period begins. Your medicine timing and dose may need adjustment.

### Key points:
1. **Eat a balanced meal at suhoor** with slow-digesting foods.
2. **Break your fast gently**, avoiding too many sweets and fried foods.
3. **Drink plenty of water** between iftar and suhoor.
4. **Know the warning signs:** extreme weakness, sweating, shaking, confusion. Break your fast immediately if you feel these.
5. **Do not stop or change medicines** without medical advice.

---
*Disclaimer: This article is for general awareness only and does not replace personal medical advice.*""",
            "October 2026"
        )
    ]
    cursor.executemany('''
        INSERT INTO articles (slug, title, category, read_time, excerpt, content, published_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', seed_articles)

    conn.commit()
    conn.close()

def generate_ref_code():
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    suffix = "".join(random.choices(chars, k=5))
    return f"DOC-2026-{suffix}"

def create_appointment(patient_name, phone, email, appointment_date, time_slot, service_type, patient_type, notes):
    conn = get_db_connection()
    cursor = conn.cursor()
    ref_code = generate_ref_code()
    cursor.execute('''
        INSERT INTO appointments (ref_code, patient_name, phone, email, appointment_date, time_slot, service_type, patient_type, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (ref_code, patient_name, phone, email, appointment_date, time_slot, service_type, patient_type, notes))
    conn.commit()
    conn.close()
    return ref_code

def get_appointment_by_ref(ref_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments WHERE ref_code = ?', (ref_code,))
    appointment = cursor.fetchone()
    conn.close()
    return appointment

def get_all_appointments(limit=100):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments ORDER BY id DESC LIMIT ?', (limit,))
    appointments = cursor.fetchall()
    conn.close()
    return appointments

def add_contact(name, phone, email, subject, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts (name, phone, email, subject, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, phone, email, subject, message))
    conn.commit()
    conn.close()

def get_all_contacts(limit=50):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts ORDER BY id DESC LIMIT ?', (limit,))
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def get_reviews(featured_only=False, limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    if featured_only:
        cursor.execute('SELECT * FROM reviews WHERE is_featured = 1 ORDER BY id DESC LIMIT ?', (limit,))
    else:
        cursor.execute('SELECT * FROM reviews ORDER BY id DESC LIMIT ?', (limit,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews

def add_review(patient_name, location, rating, condition, review_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reviews (patient_name, location, rating, condition, review_text, is_featured)
        VALUES (?, ?, ?, ?, ?, 1)
    ''', (patient_name, location, rating, condition, review_text))
    conn.commit()
    conn.close()

def get_articles(limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles ORDER BY id ASC LIMIT ?', (limit,))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_article_by_slug(slug):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles WHERE slug = ?', (slug,))
    article = cursor.fetchone()
    conn.close()
    return article

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")

