// Smooth Scrolling
const smoothScroll = (target, duration) => {
    const targetElement = document.querySelector(target);
    const targetPosition = targetElement.getBoundingClientRect().top;
    const startPosition = window.pageYOffset;
    const startTime = null;

    const ease = (t, b, c, d) => {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    };

    const animation = currentTime => {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const run = ease(timeElapsed, startPosition, targetPosition, duration);
        window.scrollTo(0, run);
        if (timeElapsed < duration) requestAnimationFrame(animation);
    };

    requestAnimationFrame(animation);
};

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        smoothScroll(this.getAttribute('href'), 1000);
    });
});

// Navigation Active State
const navLinks = document.querySelectorAll('nav a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navLinks.forEach(nav => nav.classList.remove('active'));
        link.classList.add('active');
    });
});

// Dynamic Content Loading
const loadContent = async (url, target) => {
    try {
        const response = await fetch(url);
        const data = await response.json();
        document.querySelector(target).innerHTML = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error('Error loading content:', error);
    }
};

// Example usage
// loadContent('/api/insights', '#insights');
