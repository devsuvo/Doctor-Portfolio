# Dr. Tanvir Ahmed Chowdhury | Medicine & Diabetes Specialist in Sylhet

A modern, high-performance, mobile-responsive medical doctor portfolio and appointment management website built with **Python (Flask)**, modern Tailwind CSS, and SQLite.

---

## 🌟 Key Features

### 1. Fully Mobile Responsive UI
- **Mobile First Design**: Touch-friendly navigation drawer, optimized typography, and responsive grid layouts.
- **Mobile Quick Action Bar**: Floating bottom navigation bar on mobile devices (Call Now, Chamber, Tips, Book Slot) for one-tap patient access.
- **Smooth Animations**: Glassmorphism navigation, pulse availability indicators, card hover lifts, and modal dialogs.

### 2. Comprehensive Sections Included
- **SEO Optimized Head**: Dynamic meta tags, OpenGraph previews, and Schema.org `Physician` JSON-LD structured data for Google indexing.
- **Navbar**: Logo (`Dr. Tanvir Ahmed`), full navigation menu, quick call button, and responsive appointment modal triggers.
- **Hero Section**: Qualifications badge (`MBBS, FCPS, MD`), bold headline, dual CTAs, stats grid (12+ Years, 15,000+ Patients, 4.9/5 Rating, 8+ Publications), and doctor visual card with verified BM&DC status.
- **Trust Strip**: Evidence-Based Treatment, Unhurried Consultations, Follow-up Support, and Patient Privacy Guaranteed.
- **About Preview**: Clinical philosophy, hospital credentials, and link to detailed biography.
- **Services Preview (6 Areas of Expertise)**:
  1. Diabetes Management (Type 1, Type 2, Gestational)
  2. Thyroid Disorders (Hypo/Hyperthyroidism, Nodules)
  3. Hypertension & Heart Health
  4. Obesity & Weight Management
  5. General Medicine
  6. Preventive Health Check-up
- **Why Patients Choose Dr. Tanvir**: 4 pillars (Time for every patient 15-20 mins, Clear explanations, Evidence-based care, Continued support).
- **How It Works**: 3-step intuitive booking process.
- **Interactive South Asian BMI & Diabetes Risk Tool**: Real-time WHO South Asian cutoff calculator with tailored clinical recommendations.
- **Testimonials Preview**: Verified patient reviews (Abdul Karim, Farhana Akter, Rafiul Islam) with full star ratings.
- **Health Tips Preview**: Doctor's wellness articles with dedicated reading pages.
- **Chamber & Visiting Schedule**: Popular Medical Centre, Zindabazar Point, Sylhet (Room 304, Sat-Thu 4:30 PM - 9:30 PM).
- **CTA Banner & Footer**: Full legal disclaimer, contact numbers, and reception access.

### 3. Patient Appointment Serial System
- **Real-Time Booking API**: `/api/book` with validation, date selector restrictions (prevents past dates), and slot selection.
- **Digital Serial Slip (`/confirmation/<ref_code>`)**: Generates printable and screenshot-ready patient serial tokens (e.g. `DOC-2026-XXXX`).
- **Receptionist Dashboard (`/admin`)**: Doctor and chamber assistant panel to monitor all booked appointments, patient phone numbers, and incoming inquiries.

---

## 🚀 How to Run the Website

### Step 1: Open Terminal in the Project Directory
```powershell
cd "c:\Users\Hexa's\Desktop\DESK\My Project\PYTHON\Web Python\Doctor Portfolio"
```

### Step 2: (Optional) Install Dependencies
Dependencies are listed in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### Step 3: Run the Application
```powershell
python run.py
```
Or directly:
```powershell
python app.py
```

### Step 4: Open in Your Browser
- **Patient Website**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Reception / Admin Panel**: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)

---

## 📁 Project Directory Structure
```
Doctor Portfolio/
├── app.py                     # Flask web app routes and controllers
├── models.py                  # SQLite database engine and data models
├── run.py                     # Easy local execution launcher
├── requirements.txt           # Python dependencies
├── appointments.db            # SQLite database (auto-generated)
├── README.md                  # Project documentation
├── static/
│   ├── css/
│   │   └── custom.css         # Glassmorphism, animations, print rules
│   ├── js/
│   │   └── main.js            # Mobile drawer, modal, AJAX booking, BMI tool
│   └── images/
│       ├── doctor-portrait.svg # High-definition doctor portrait graphic
│       └── chamber-location.svg # Sylhet chamber illustration
└── templates/
    ├── base.html              # Layout, navbar, mobile drawer, modal, footer
    ├── index.html             # Landing page with all sections
    ├── about.html             # Full doctor profile and philosophy
    ├── services.html          # All 6 medical services in depth
    ├── experience.html        # Experience timeline, research papers, degrees
    ├── chamber.html           # Chamber schedule, room 304, visiting hours
    ├── reviews.html           # Verified reviews and submission form
    ├── health_tips.html       # Articles list
    ├── article_detail.html    # Full article reader
    ├── book.html              # Dedicated appointment booking page
    ├── contact.html           # Chamber contact and inquiry form
    └── admin.html             # Chamber reception management dashboard
```

---

## 🏥 Chamber Details
- **Doctor**: Dr. Tanvir Ahmed Chowdhury
- **Degrees**: MBBS, FCPS (Medicine), MD (Endocrinology)
- **BM&DC Reg. No**: A-00000
- **Chamber**: Popular Medical Centre, Zindabazar Point, Sylhet 3100
- **Location**: 3rd Floor, Room No. 304
- **Visiting Hours**: Saturday – Thursday: 4:30 PM – 9:30 PM (Friday Closed)
- **Serial Hotline**: +880 1700-000000

