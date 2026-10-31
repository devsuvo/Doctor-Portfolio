/* Main JavaScript for Dr. Tanvir Ahmed Chowdhury Medical Website */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide icons if available
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // 1. Mobile Menu Drawer Functionality
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const closeMobileMenuBtn = document.getElementById('close-mobile-menu-btn');
  const mobileMenuDrawer = document.getElementById('mobile-menu-drawer');
  const mobileMenuBackdrop = document.getElementById('mobile-menu-backdrop');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

  function openMobileMenu() {
    if (!mobileMenuDrawer) return;
    mobileMenuDrawer.classList.remove('translate-x-full');
    mobileMenuBackdrop.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  }

  function closeMobileMenu() {
    if (!mobileMenuDrawer) return;
    mobileMenuDrawer.classList.add('translate-x-full');
    mobileMenuBackdrop.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }

  if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', openMobileMenu);
  if (closeMobileMenuBtn) closeMobileMenuBtn.addEventListener('click', closeMobileMenu);
  if (mobileMenuBackdrop) mobileMenuBackdrop.addEventListener('click', closeMobileMenu);

  mobileNavLinks.forEach(link => {
    link.addEventListener('click', closeMobileMenu);
  });

  // 2. Appointment Booking Modal Functionality
  const bookingModal = document.getElementById('booking-modal');
  const modalCloseBtns = document.querySelectorAll('.close-booking-modal');
  const openModalBtns = document.querySelectorAll('.open-booking-modal-btn');
  const modalServiceSelect = document.getElementById('modal-service-type');

  function openBookingModal(defaultService = '') {
    if (!bookingModal) return;
    if (defaultService && modalServiceSelect) {
      modalServiceSelect.value = defaultService;
    }
    bookingModal.classList.remove('hidden');
    bookingModal.classList.add('flex');
    document.body.classList.add('overflow-hidden');
  }

  function closeBookingModal() {
    if (!bookingModal) return;
    bookingModal.classList.add('hidden');
    bookingModal.classList.remove('flex');
    document.body.classList.remove('overflow-hidden');
  }

  openModalBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const service = btn.getAttribute('data-service') || '';
      openBookingModal(service);
    });
  });

  modalCloseBtns.forEach(btn => {
    btn.addEventListener('click', closeBookingModal);
  });

  if (bookingModal) {
    bookingModal.addEventListener('click', (e) => {
      if (e.target === bookingModal) {
        closeBookingModal();
      }
    });
  }

  // Escape key closes modals and mobile drawer
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeMobileMenu();
      closeBookingModal();
    }
  });

  // 3. Set Minimum Date on Date Inputs to Today
  const dateInputs = document.querySelectorAll('input[type="date"]');
  const today = new Date().toISOString().split('T')[0];
  dateInputs.forEach(input => {
    input.min = today;
    if (!input.value) {
      input.value = today;
    }
  });

  // 4. AJAX Booking Forms Handler (Modal & Inline Page Forms)
  const bookingForms = document.querySelectorAll('.ajax-booking-form');
  bookingForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn.innerHTML;

      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
        Confirming Slot...
      `;

      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());

      try {
        const response = await fetch('/api/book', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.success) {
          form.reset();
          closeBookingModal();
          // Redirect to confirmation slip page
          window.location.href = `/confirmation/${result.ref_code}`;
        } else {
          showToast(result.error || 'Failed to book appointment. Please check details.', 'error');
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnText;
        }
      } catch (err) {
        console.error(err);
        showToast('Network error. Please call +880 1700-000000 directly.', 'error');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }
    });
  });

  // 5. Toast Notification System
  function showToast(message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    const bgColor = type === 'success' ? 'bg-teal-600' : 'bg-rose-600';
    toast.className = `${bgColor} text-white px-5 py-3.5 rounded-xl shadow-xl flex items-center gap-3 text-sm font-medium transform transition-all duration-300 translate-y-4 opacity-0 pointer-events-auto`;
    toast.innerHTML = `
      <span>${type === 'success' ? '✓' : '⚠️'}</span>
      <span>${message}</span>
    `;

    container.appendChild(toast);

    requestAnimationFrame(() => {
      toast.classList.remove('translate-y-4', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
    });

    setTimeout(() => {
      toast.classList.remove('translate-y-0', 'opacity-100');
      toast.classList.add('translate-y-4', 'opacity-0');
      setTimeout(() => toast.remove(), 300);
    }, 4500);
  }

  window.showToast = showToast;

  // 6. Interactive BMI & Diabetes Risk Calculator
  const bmiForm = document.getElementById('bmi-calculator-form');
  if (bmiForm) {
    bmiForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const weight = parseFloat(document.getElementById('bmi-weight').value);
      const heightCm = parseFloat(document.getElementById('bmi-height').value);
      const resultCard = document.getElementById('bmi-result-card');
      const scoreEl = document.getElementById('bmi-score');
      const badgeEl = document.getElementById('bmi-badge');
      const adviceEl = document.getElementById('bmi-advice');

      if (!weight || !heightCm || weight <= 0 || heightCm <= 0) {
        showToast('Please enter valid weight and height numbers', 'error');
        return;
      }

      const heightM = heightCm / 100;
      const bmi = (weight / (heightM * heightM)).toFixed(1);

      scoreEl.innerText = bmi;
      resultCard.classList.remove('hidden');

      // Asian-specific BMI cutoffs (WHO South Asian Guidelines)
      if (bmi < 18.5) {
        badgeEl.innerText = 'Underweight';
        badgeEl.className = 'px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800';
        adviceEl.innerText = 'Nutritional support & endocrine evaluation recommended to assess metabolic balance.';
      } else if (bmi >= 18.5 && bmi < 23.0) {
        badgeEl.innerText = 'Optimal / Healthy Range (South Asian)';
        badgeEl.className = 'px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800';
        adviceEl.innerText = 'Great job! Maintain regular physical activity and annual fasting glucose screenings.';
      } else if (bmi >= 23.0 && bmi < 27.5) {
        badgeEl.innerText = 'Overweight / Increased Risk';
        badgeEl.className = 'px-3 py-1 rounded-full text-xs font-bold bg-orange-100 text-orange-800';
        adviceEl.innerText = 'South Asian physiology carries elevated visceral fat risk. Consider a preventive diabetes & lipid screen.';
      } else {
        badgeEl.innerText = 'Obesity / High Metabolic Risk';
        badgeEl.className = 'px-3 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800';
        adviceEl.innerText = 'Increased risk for Type 2 diabetes & hypertension. Medically supervised weight management is strongly advised.';
      }
    });
  }
});

