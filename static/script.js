// JavaScript for MLOps Learning Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initializeAnimations();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize progress tracking
    initializeProgressTracking();
    
    // Initialize form validation
    initializeFormValidation();
});

// Animation initialization
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
    
    // Add slide animations to level cards
    const levelCards = document.querySelectorAll('.level-card');
    levelCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
        if (index % 2 === 0) {
            card.classList.add('slide-in-left');
        } else {
            card.classList.add('slide-in-right');
        }
    });
}

// Tooltip initialization
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Progress tracking
function initializeProgressTracking() {
    // Save progress when user interacts with content
    const contentAreas = document.querySelectorAll('.module-content');
    contentAreas.forEach(area => {
        area.addEventListener('scroll', debounce(saveProgress, 1000));
    });
    
    // Track time spent on page
    let startTime = Date.now();
    window.addEventListener('beforeunload', function() {
        const timeSpent = Date.now() - startTime;
        saveTimeSpent(timeSpent);
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Utility functions
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

function saveProgress() {
    // This would normally save progress to the backend
    console.log('Progress saved');
}

function saveTimeSpent(timeSpent) {
    // This would normally send time spent data to the backend
    console.log('Time spent:', timeSpent, 'ms');
}

// Quiz functionality
function submitQuiz(formData) {
    const submitButton = document.querySelector('#quiz-form button[type="submit"]');
    const originalText = submitButton.innerHTML;
    
    submitButton.innerHTML = '<span class="spinner"></span> Checking...';
    submitButton.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
        
        // Show results
        const resultsDiv = document.getElementById('quiz-results');
        if (resultsDiv) {
            resultsDiv.style.display = 'block';
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
    }, 2000);
}

// Module completion
function completeModule() {
    const completeButton = document.querySelector('button[onclick="completeModule()"]');
    const originalText = completeButton.innerHTML;
    
    completeButton.innerHTML = '<span class="spinner"></span> Completing...';
    completeButton.disabled = true;
    
    // Add loading state to the card
    const card = completeButton.closest('.card');
    card.classList.add('loading');
    
    // Simulate API call
    setTimeout(() => {
        completeButton.innerHTML = originalText;
        completeButton.disabled = false;
        card.classList.remove('loading');
        
        // Show success message
        showSuccessMessage('Module completed successfully! 🎉');
    }, 1500);
}

// Success message display
function showSuccessMessage(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Achievement notification
function showAchievementNotification(achievement) {
    const notification = document.createElement('div');
    notification.className = 'achievement-notification position-fixed';
    notification.style.top = '20px';
    notification.style.left = '20px';
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        <div class="card border-warning">
            <div class="card-body d-flex align-items-center">
                <div class="achievement-badge me-3">${achievement.badge_icon}</div>
                <div>
                    <h6 class="mb-1">Achievement Unlocked!</h6>
                    <p class="mb-0 text-muted">${achievement.name}</p>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Progress bar animation
function animateProgressBar(progressBar, targetValue) {
    let currentValue = 0;
    const increment = targetValue / 100;
    
    const timer = setInterval(() => {
        currentValue += increment;
        progressBar.style.width = Math.min(currentValue, targetValue) + '%';
        
        if (currentValue >= targetValue) {
            clearInterval(timer);
        }
    }, 20);
}

// Smooth scrolling for anchor links
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

// Code syntax highlighting (basic)
function highlightCode() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        // This is a basic implementation
        // In a real app, you'd use a library like Prism.js or highlight.js
        block.style.fontFamily = 'Fira Code, Monaco, Consolas, monospace';
    });
}

// Initialize code highlighting
highlightCode();

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit forms
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeForm = document.querySelector('form:focus-within');
        if (activeForm) {
            const submitButton = activeForm.querySelector('button[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                submitButton.click();
            }
        }
    }
    
    // Escape to close modals/alerts
    if (e.key === 'Escape') {
        const activeAlert = document.querySelector('.alert.show');
        if (activeAlert) {
            const closeButton = activeAlert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }
    }
});

// Performance monitoring
function trackPerformance() {
    // Track page load time
    window.addEventListener('load', function() {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log('Page load time:', loadTime, 'ms');
        
        // Send to analytics (placeholder)
        if (loadTime > 3000) {
            console.warn('Slow page load detected');
        }
    });
}

// Initialize performance tracking
trackPerformance();

// Accessibility improvements
function improveAccessibility() {
    // Add focus indicators for keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
    
    // Add skip links for screen readers
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Skip to main content';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        background: #000;
        color: #fff;
        padding: 8px;
        text-decoration: none;
        z-index: 10000;
    `;
    
    skipLink.addEventListener('focus', function() {
        this.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', function() {
        this.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
}

// Initialize accessibility improvements
improveAccessibility();
