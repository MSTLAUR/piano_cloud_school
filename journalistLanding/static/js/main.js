// ============================================
// NAVIGATION SCROLL EFFECT
// ============================================
let lastScrollY = 0;
const nav = document.getElementById('main-nav');

window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  
  if (scrollY > 20) {
    nav.classList.remove('nav-default');
    nav.classList.add('nav-scrolled');
  } else {
    nav.classList.remove('nav-scrolled');
    nav.classList.add('nav-default');
  }
  
  lastScrollY = scrollY;
});

// ============================================
// MOBILE MENU TOGGLE
// ============================================
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const menuIcon = mobileMenuBtn.querySelector('.menu-icon');
const closeIcon = mobileMenuBtn.querySelector('.close-icon');

mobileMenuBtn.addEventListener('click', () => {
  const isOpen = mobileMenu.classList.contains('active');
  
  if (isOpen) {
    mobileMenu.classList.remove('active');
    menuIcon.style.display = 'block';
    closeIcon.style.display = 'none';
  } else {
    mobileMenu.classList.add('active');
    menuIcon.style.display = 'none';
    closeIcon.style.display = 'block';
  }
});

// Close mobile menu when clicking a link
const mobileMenuLinks = document.querySelectorAll('.mobile-menu-link, .mobile-menu .btn');
mobileMenuLinks.forEach(link => {
  link.addEventListener('click', () => {
    mobileMenu.classList.remove('active');
    menuIcon.style.display = 'block';
    closeIcon.style.display = 'none';
  });
});

// ============================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    
    // Skip if it's just "#"
    if (href === '#') {
      e.preventDefault();
      return;
    }
    
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      const navHeight = nav.offsetHeight;
      const targetPosition = target.offsetTop - navHeight - 20;
      
      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
    }
  });
});

// ============================================
// FAQ ACCORDION
// ============================================
let currentOpenFaq = 0; // First FAQ is open by default

function toggleFaq(index) {
  const faqButton = document.querySelectorAll('.faq-button')[index];
  const faqWrapper = faqButton.querySelector('.faq-question-wrapper');
  const faqAnswer = faqButton.querySelector('.faq-answer');
  const faqToggle = document.getElementById(`faq-toggle-${index}`);
  
  // If clicking the currently open FAQ, close it
  if (currentOpenFaq === index && faqWrapper.classList.contains('active')) {
    faqWrapper.classList.remove('active');
    faqAnswer.classList.remove('active');
    faqToggle.textContent = '+';
    currentOpenFaq = null;
    return;
  }
  
  // Close previously open FAQ
  if (currentOpenFaq !== null) {
    const prevButton = document.querySelectorAll('.faq-button')[currentOpenFaq];
    const prevWrapper = prevButton.querySelector('.faq-question-wrapper');
    const prevAnswer = prevButton.querySelector('.faq-answer');
    const prevToggle = document.getElementById(`faq-toggle-${currentOpenFaq}`);
    
    prevWrapper.classList.remove('active');
    prevAnswer.classList.remove('active');
    prevToggle.textContent = '+';
  }
  
  // Open clicked FAQ
  faqWrapper.classList.add('active');
  faqAnswer.classList.add('active');
  faqToggle.textContent = '−';
  currentOpenFaq = index;
}

// Initialize first FAQ as open
document.addEventListener('DOMContentLoaded', () => {
  const firstFaqWrapper = document.querySelector('.faq-button .faq-question-wrapper');
  const firstFaqAnswer = document.querySelector('.faq-button .faq-answer');
  const firstFaqToggle = document.getElementById('faq-toggle-0');
  
  if (firstFaqWrapper && firstFaqAnswer && firstFaqToggle) {
    firstFaqWrapper.classList.add('active');
    firstFaqAnswer.classList.add('active');
    firstFaqToggle.textContent = '−';
  }
});

// ============================================
// HERO FORM SUBMIT
// ============================================
let heroFormSubmitting = false;

function handleHeroFormSubmit(event) {
  event.preventDefault();

  if (heroFormSubmitting) return;

  const form = event.target;
  const email = form.querySelector('input[type="email"]').value;
  const submitBtn = form.querySelector('button[type="submit"]');
  const csrftoken = getCookie('csrftoken');
  const originalBtnText = submitBtn.textContent;

  // Set loading state
  heroFormSubmitting = true;
  submitBtn.textContent = '...';
  submitBtn.disabled = true;

  // Submit to waitlist endpoint
  fetch('/jl/waitlist/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'X-Requested-With': 'XMLHttpRequest',
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `email=${encodeURIComponent(email)}`
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Show success state
      submitBtn.textContent = '✓ Done!';

      // Reset form
      form.reset();

      // Redirect to thank you page
      setTimeout(() => {
        window.location.href = data.redirect_url || '/thanks/';
      }, 1500);
    } else {
      // Show error
      submitBtn.textContent = 'Error - Try Again';
      setTimeout(() => {
        submitBtn.textContent = originalBtnText;
        submitBtn.disabled = false;
        heroFormSubmitting = false;
      }, 2000);
    }
  })
  .catch((error) => {
    console.error('Error:', error);
    submitBtn.textContent = 'Error - Try Again';
    setTimeout(() => {
      submitBtn.textContent = originalBtnText;
      submitBtn.disabled = false;
      heroFormSubmitting = false;
    }, 2000);
  });
}

// ============================================
// WAITLIST FORM SUBMIT
// ============================================
let waitlistSubmitting = false;

function handleWaitlistSubmit(event) {
  event.preventDefault();

  if (waitlistSubmitting) return;

  const form = event.target;
  const email = form.querySelector('input[type="email"]').value;
  const submitBtn = document.getElementById('waitlist-submit');
  const csrftoken = getCookie('csrftoken');

  // Set loading state
  waitlistSubmitting = true;
  submitBtn.textContent = '...';
  submitBtn.disabled = true;

  // Submit to Django backend
  fetch('/jl/waitlist/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'X-Requested-With': 'XMLHttpRequest',
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `email=${encodeURIComponent(email)}`
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Show success state
      submitBtn.textContent = '✓ Done!';

      // Reset form
      form.reset();

      // Redirect to thank you page
      setTimeout(() => {
        window.location.href = data.redirect_url || '/thanks/';
      }, 1500);
    } else {
      // Show error
      submitBtn.textContent = 'Error - Try Again';
      setTimeout(() => {
        submitBtn.textContent = 'Join →';
        submitBtn.disabled = false;
        waitlistSubmitting = false;
      }, 2000);
    }
  })
  .catch((error) => {
    console.error('Error:', error);
    submitBtn.textContent = 'Error - Try Again';
    setTimeout(() => {
      submitBtn.textContent = 'Join →';
      submitBtn.disabled = false;
      waitlistSubmitting = false;
    }, 2000);
  });
}

// ============================================
// INTERSECTION OBSERVER FOR SCROLL ANIMATIONS
// ============================================
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animated');
      // Optional: unobserve after animation
      // observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe all elements with animation classes
document.addEventListener('DOMContentLoaded', () => {
  const animatedElements = document.querySelectorAll('.fade-in, .fade-in-up');
  animatedElements.forEach(el => {
    el.classList.add('animate-on-scroll');
    observer.observe(el);
  });
});

// ============================================
// PREVENT LAYOUT SHIFT ON LOAD
// ============================================
window.addEventListener('load', () => {
  document.body.style.visibility = 'visible';
});

// ============================================
// CSRF TOKEN HELPER FOR DJANGO FORMS
// ============================================
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// If you want to make actual AJAX requests to Django:
function submitFormAjax(url, formData) {
  const csrftoken = getCookie('csrftoken');
  
  fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData)
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

// ============================================
// UTILITY: DEBOUNCE FUNCTION
// ============================================
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ============================================
// HANDLE WINDOW RESIZE
// ============================================
const handleResize = debounce(() => {
  // Close mobile menu on resize to desktop
  if (window.innerWidth >= 768 && mobileMenu.classList.contains('active')) {
    mobileMenu.classList.remove('active');
    menuIcon.style.display = 'block';
    closeIcon.style.display = 'none';
  }
}, 250);

window.addEventListener('resize', handleResize);

// ============================================
// KEYBOARD NAVIGATION FOR ACCESSIBILITY
// ============================================
document.addEventListener('keydown', (e) => {
  // Close mobile menu with Escape key
  if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
    mobileMenu.classList.remove('active');
    menuIcon.style.display = 'block';
    closeIcon.style.display = 'none';
    mobileMenuBtn.focus();
  }
});

// ============================================
// TAILWIND CONFIG COLORS (for reference)
// ============================================
const colors = {
  paper: '#FFFBEB',
  ink: '#1E1B4B',
  slate: '#64748B',
  electric: '#4F46E5',
  'hot-pink': '#EC4899',
  lime: '#BEF264',
  sunny: '#FDE047'
};

// Export colors for use in other scripts if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { colors };
}