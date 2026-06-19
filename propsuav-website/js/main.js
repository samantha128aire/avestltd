/* ============================================
   PropsUAV - Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {
  // Mobile menu toggle
  const hamburger = document.querySelector('.hamburger');
  const nav = document.querySelector('nav');

  if (hamburger) {
    hamburger.addEventListener('click', function () {
      nav.classList.toggle('active');
    });

    // Close menu when a link is clicked
    const navLinks = nav.querySelectorAll('a');
    navLinks.forEach(link => {
      link.addEventListener('click', function () {
        nav.classList.remove('active');
      });
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Form validation and submission (Formspree handles the actual submission)
  const contactForm = document.querySelector('.contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      const requiredFields = ['name', 'email', 'phone', 'acreage', 'crop'];
      let isValid = true;

      requiredFields.forEach(fieldName => {
        const field = contactForm.querySelector(`[name="${fieldName}"]`);
        if (field && !field.value.trim()) {
          field.style.borderColor = '#f57c00';
          isValid = false;
        } else if (field) {
          field.style.borderColor = '';
        }
      });

      // Basic email validation
      const emailField = contactForm.querySelector('[name="email"]');
      if (emailField && !isValidEmail(emailField.value)) {
        emailField.style.borderColor = '#f57c00';
        isValid = false;
      }

      if (!isValid) {
        e.preventDefault();
        alert('Please fill in all required fields with valid information.');
      }
    });
  }
});

// Email validation helper
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Add scroll animation for elements
function setupScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe feature cards and service cards
  document.querySelectorAll('.feature-card, .service-card, .step').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
}

// Initialize scroll animations when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupScrollAnimations);
} else {
  setupScrollAnimations();
}
