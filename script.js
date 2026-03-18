// Scroll reveal
const reveals = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('visible'), i * 80);
    }
  });
}, { threshold: 0.1 });
reveals.forEach(r => observer.observe(r));

// Cookies
const banner = document.getElementById('cookiesBanner');
const accepted = localStorage.getItem('cookies_accepted');
if (accepted) banner.classList.add('hidden');

document.getElementById('cookiesAccept').addEventListener('click', () => {
  localStorage.setItem('cookies_accepted', 'all');
  banner.classList.add('hidden');
});

document.getElementById('cookiesDecline').addEventListener('click', () => {
  localStorage.setItem('cookies_accepted', 'essential');
  banner.classList.add('hidden');
});

document.getElementById('cookie-settings').addEventListener('click', (e) => {
  e.preventDefault();
  localStorage.removeItem('cookies_accepted');
  banner.classList.remove('hidden');
});
