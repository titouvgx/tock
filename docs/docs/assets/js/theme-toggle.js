document.addEventListener('DOMContentLoaded', function () {
    // Ajoute un bouton pour basculer entre le mode clair et sombre
    const toggleButton = document.createElement('button');
    toggleButton.textContent = '🌙 / ☀️';
    toggleButton.style.position = 'fixed';
    toggleButton.style.bottom = '20px';
    toggleButton.style.left = '20px';
    toggleButton.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    toggleButton.style.color = 'white';
    toggleButton.style.border = 'none';
    toggleButton.style.padding = '10px';
    toggleButton.style.borderRadius = '50%';
    toggleButton.style.cursor = 'pointer';
    toggleButton.style.zIndex = '9999';
    document.body.appendChild(toggleButton);

    // Fonction pour basculer le thème
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
    }

    // Ajouter un gestionnaire d'événements pour le bouton
    toggleButton.addEventListener('click', toggleTheme);

    // Vérifier si un thème est déjà enregistré dans le localStorage
    if (localStorage.getItem('theme') === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }

    // Enregistrer le thème dans le localStorage pour la prochaine visite
    document.documentElement.addEventListener('change', function() {
        localStorage.setItem('theme', document.documentElement.getAttribute('data-theme'));
    });
});
