import unittest
from app import app
from models import init_db

class DoctorPortfolioTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        init_db()
        self.client = app.test_client()

    def test_routes_status_code(self):
        routes = [
            '/',
            '/about',
            '/services',
            '/services/diabetes',
            '/services/thyroid',
            '/services/hypertension',
            '/services/obesity',
            '/experience',
            '/chamber',
            '/reviews',
            '/health-tips',
            '/health-tips/7-simple-habits-blood-sugar-control',
            '/health-tips/thyroid-problems-6-early-signs',
            '/health-tips/high-blood-pressure-silent-problem',
            '/health-tips/fasting-and-diabetes-safe-guide',
            '/health-tips/managing-fasting-blood-sugar',
            '/contact',
            '/faq',
            '/privacy-policy',
            '/terms',
            '/book',
            '/admin'
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with status {response.status_code}")
            print(f"[OK] Route {route} -> 200 OK")

    def test_booking_api(self):
        payload = {
            "patient_name": "Test Patient",
            "phone": "01700112233",
            "email": "patient@example.com",
            "appointment_date": "2026-11-05",
            "time_slot": "5:30 PM - 6:30 PM",
            "service_type": "Diabetes Management",
            "patient_type": "New Consultation",
            "notes": "Testing appointment booking system"
        }
        response = self.client.post('/api/book', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['ref_code'].startswith('DOC-2026-'))
        print(f"[OK] API /api/book created serial: {data['ref_code']}")

        # Test Confirmation Page with the generated reference code
        conf_response = self.client.get(f"/confirmation/{data['ref_code']}")
        self.assertEqual(conf_response.status_code, 200)
        self.assertIn(b"Booking Successful!", conf_response.data)
        print(f"[OK] Confirmation slip page loaded with ref: {data['ref_code']}")

    def test_contact_submission(self):
        response = self.client.post('/contact/submit', data={
            "name": "Rahim Ahmed",
            "phone": "01811223344",
            "email": "rahim@test.com",
            "subject": "Appointment Query",
            "message": "Can I visit on Sunday evening?"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Your message has been sent", response.data)
        print("[OK] Contact inquiry submission tested successfully.")

    def test_review_submission(self):
        response = self.client.post('/reviews/submit', data={
            "patient_name": "Sultana Begum",
            "location": "Shahjalal Uposhohor",
            "rating": "5",
            "condition": "Thyroid Disorder",
            "review_text": "Excellent doctor with clear advice."
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Your feedback has been submitted", response.data)
        print("[OK] Review submission tested successfully.")

    def test_404_page(self):
        response = self.client.get('/some-non-existent-page-url')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404 - Page Not Found", response.data)
        self.assertIn(b"The page you are looking for may have been moved or no longer exists.", response.data)
        self.assertIn(b"Back to Home", response.data)
        self.assertIn(b"Book Appointment", response.data)
        print("[OK] 404 Not Found error page tested successfully.")

if __name__ == '__main__':
    unittest.main()
