document.getElementById('themeToggle').addEventListener('click', () => {
    const body = document.body;
    const isDark = body.classList.toggle('dark-theme');
    
    // Update Monaco editor theme
    if (window.editor) {
        monaco.editor.setTheme(isDark ? 'vs-dark' : 'vs');
    }

    // Update theme toggle icon
    const icon = document.querySelector('#themeToggle i');
    icon.classList.remove('fa-moon', 'fa-sun');
    icon.classList.add(isDark ? 'fa-sun' : 'fa-moon');

    // Store preference
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// Load saved theme preference
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.getElementById('themeToggle').click();
    }
});
