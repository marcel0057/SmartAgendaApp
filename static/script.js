// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    // Demander la permission pour les notifications
    if (Notification.permission !== 'granted') {
        Notification.requestPermission();
    }

    // Vérifier les rendez-vous pour les notifications
    function checkRendezVous() {
        fetch('/api/rendezvous')
            .then(response => {
                if (response.status === 401) {
                    window.location.href = '/login';
                    return;
                }
                return response.json();
            })
            .then(rendezvous => {
                const today = new Date();
                const tomorrow = new Date(today);
                tomorrow.setDate(today.getDate() + 1);
                const tomorrowStr = tomorrow.toISOString().split('T')[0];

                rendezvous.forEach(rdv => {
                    if (rdv.date === tomorrowStr) {
                        new Notification(`Rappel : ${rdv.titre} demain à ${rdv.heure}`);
                        // Ajouter à la section des rappels dans dashboard.html
                        const eventList = document.querySelector('.event-list');
                        if (eventList) {
                            const eventItem = document.createElement('li');
                            eventItem.className = 'event-item';
                            eventItem.innerHTML = `
                                <span class="event-time">${rdv.heure}</span>
                                <div>
                                    <div class="event-title">${rdv.titre}</div>
                                    <div class="event-location">${rdv.description || 'Aucune description'}</div>
                                    <audio controls src="/static/audio/reminder_${rdv.id}.mp3"></audio>
                                </div>
                            `;
                            eventList.appendChild(eventItem);
                        }
                    }
                });
            })
            .catch(error => console.error('Erreur lors de la récupération des rendez-vous:', error));
    }

    // Vérifier toutes les 24h
    setInterval(checkRendezVous, 24 * 60 * 60 * 1000);
    checkRendezVous();
});