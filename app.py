import os
import markdown
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from models import (
    init_db,
    create_appointment,
    get_appointment_by_ref,
    get_all_appointments,
    add_contact,
    get_all_contacts,
    get_reviews,
    add_review,
    get_articles,
    get_article_by_slug
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dr-tanvir-portfolio-sylhet-secret-key-2026')

@app.template_filter('render_markdown')
def render_markdown(text):
    if not text:
        return ''
    return markdown.markdown(text)

# Initialize SQLite database on launch
init_db()

@app.route('/')
def index():
    featured_reviews = get_reviews(featured_only=True, limit=6)
    latest_articles = get_articles(limit=3)
    return render_template(
        'index.html',
        active_page='home',
        reviews=featured_reviews,
        articles=latest_articles
    )

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/services')
def services():
    return render_template('services.html', active_page='services')

@app.route('/services/diabetes')
def service_diabetes():
    return render_template('service_diabetes.html', active_page='services')

@app.route('/services/thyroid')
def service_thyroid():
    return render_template('service_thyroid.html', active_page='services')

@app.route('/services/hypertension')
def service_hypertension():
    return render_template('service_hypertension.html', active_page='services')

@app.route('/services/obesity')
def service_obesity():
    return render_template('service_obesity.html', active_page='services')

@app.route('/experience')
def experience():
    return render_template('experience.html', active_page='experience')

@app.route('/chamber')
def chamber():
    return render_template('chamber.html', active_page='chamber')

@app.route('/reviews')
def reviews():
    all_reviews = get_reviews(featured_only=False, limit=30)
    return render_template('reviews.html', active_page='reviews', reviews=all_reviews)

@app.route('/reviews/submit', methods=['POST'])
def submit_review():
    patient_name = request.form.get('patient_name', '').strip()
    location = request.form.get('location', '').strip()
    rating = int(request.form.get('rating', 5))
    condition = request.form.get('condition', 'General Medicine').strip()
    review_text = request.form.get('review_text', '').strip()

    if not patient_name or not review_text:
        flash('Please fill in your name and feedback description.', 'error')
        return redirect(url_for('reviews'))

    add_review(patient_name, location or 'Sylhet', rating, condition, review_text)
    flash('Thank you! Your feedback has been submitted successfully.', 'success')
    return redirect(url_for('reviews'))

@app.route('/health-tips')
def health_tips():
    articles = get_articles(limit=20)
    return render_template('health_tips.html', active_page='health_tips', articles=articles)

@app.route('/health-tips/<slug>')
def article_detail(slug):
    slug_aliases = {
        'managing-fasting-blood-sugar': '7-simple-habits-blood-sugar-control',
        'hypothyroidism-vs-hyperthyroidism': 'thyroid-problems-6-early-signs',
        'the-silent-killer-blood-pressure': 'high-blood-pressure-silent-problem'
    }
    target_slug = slug_aliases.get(slug, slug)
    article = get_article_by_slug(target_slug)
    if not article:
        flash('Article not found.', 'error')
        return redirect(url_for('health_tips'))
    return render_template('article_detail.html', active_page='health_tips', article=article)

@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')

@app.route('/faq')
def faq():
    return render_template('faq.html', active_page='faq')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html', active_page='')

@app.route('/terms')
def terms():
    return render_template('terms.html', active_page='')

@app.route('/contact/submit', methods=['POST'])
def contact_submit():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', 'General Query').strip()
    message = request.form.get('message', '').strip()

    if not name or not phone or not message:
        flash('Please provide your name, phone number, and message.', 'error')
        return redirect(url_for('contact'))

    add_contact(name, phone, email, subject, message)
    flash('Your message has been sent to our chamber reception. We will get back to you shortly.', 'success')
    return redirect(url_for('contact'))

@app.route('/book')
def book():
    return render_template('book.html', active_page='book')

@app.route('/api/book', methods=['POST'])
def api_book():
    data = request.get_json(silent=True) or request.form.to_dict()
    
    patient_name = data.get('patient_name', '').strip() or data.get('full_name', '').strip()
    phone = data.get('phone', '').strip() or data.get('phone_number', '').strip()
    email = data.get('email', '').strip()
    appointment_date = data.get('appointment_date', '').strip() or data.get('preferred_date', '').strip()
    time_slot = data.get('time_slot', '').strip() or data.get('preferred_time', '5:00 PM - 6:00 PM').strip()
    service_type = data.get('service_type', '').strip() or data.get('reason', 'General Consultation').strip()
    patient_type = data.get('patient_type', 'Chamber Visit').strip()
    age = data.get('age', '').strip()
    notes = data.get('notes', '').strip()

    if age:
        notes = f"Age: {age}. " + notes
    if data.get('reason') and data.get('reason') != service_type:
        notes = f"Reason: {data.get('reason')}. " + notes

    if not patient_name or not phone or not appointment_date:
        return jsonify({
            'success': False,
            'error': 'Patient name, phone number, and appointment date are required.'
        }), 400

    ref_code = create_appointment(
        patient_name=patient_name,
        phone=phone,
        email=email,
        appointment_date=appointment_date,
        time_slot=time_slot,
        service_type=service_type,
        patient_type=patient_type,
        notes=notes
    )

    return jsonify({
        'success': True,
        'ref_code': ref_code,
        'message': 'Appointment confirmed successfully!'
    })

@app.route('/confirmation/<ref_code>')
def appointment_confirmation(ref_code):
    appointment = get_appointment_by_ref(ref_code)
    if not appointment:
        flash('Appointment reference code not found.', 'error')
        return redirect(url_for('book'))
    return render_template('confirmation.html', appointment=appointment)

@app.route('/admin')
def admin_panel():
    appointments = get_all_appointments(limit=100)
    contacts = get_all_contacts(limit=50)
    return render_template('admin.html', active_page='admin', appointments=appointments, contacts=contacts)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', active_page='404'), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Dr. Tanvir Ahmed Chowdhury Medical Portfolio running on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)

