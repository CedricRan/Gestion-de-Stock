function switchWindow(windowId) {
    // 1. Désactiver tous les onglets dans la sidebar
    const links = document.querySelectorAll('.nav-links li');
    links.forEach(link => link.classList.remove('active'));

    // 2. Cacher toutes les fenêtres HTML
    const windows = document.querySelectorAll('.window');
    windows.forEach(win => win.classList.remove('active'));

    // 3. Activer la fenêtre demandée
    document.getElementById(`window-${windowId}`).classList.add('active');

    // 4. Mettre en surbrillance le bouton cliqué dans la sidebar
    // On cherche le li qui contient le bon attribut ou texte
    const eventTarget = event.currentTarget;
    if (eventTarget) {
        eventTarget.classList.add('active');
    }

    // 🎯 RECHARGEMENT DES DONNÉES À LA VOLÉE
    // Dès qu'on ouvre une fenêtre, on appelle ton API pour avoir les données fraîches !
    if (windowId === 'stocks') {
        chargerStocksUrgents();
    } else if (windowId === 'anomalies') {
        chargerAnomalies();
    } else if (windowId === 'dashboard') {
        chargerDashboardGeneral();
    }
}

// Exemple de fonction de chargement connectée à ta nouvelle route Python
async function chargerStocksUrgents() {
    const response = await fetch('/stocks/by-urgency');
    const stocks = await response.json();
    
    const container = document.getElementById('stocks-list');
    // Construit ton tableau HTML ici avec la variable "stocks"
    container.innerHTML = `
        <table class="stock-table">
            </table>
    `;
}
