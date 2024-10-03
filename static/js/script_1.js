document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript is working!");
});

document.addEventListener('DOMContentLoaded', function () {
    const relay1Button = document.getElementById('activateRelay1');
    const relay2Button = document.getElementById('activateRelay2');
    const statusRelay1 = document.getElementById('statusRelay1');
    const statusRelay2 = document.getElementById('statusRelay2');

    relay1Button.addEventListener('click', function () {
        fetch('/activate_relay?relay_number=1')
            .then(response => response.json())
            .then(data => {
                if (data.message.includes("activé")) {
                    statusRelay1.textContent = 'Status: Activé';
		 // After 1 second, revert to "Désactivé"
                    setTimeout(() => {
                        statusRelay1.textContent = 'Status: Désactivé';
                    }, 1000); // 1000 ms = 1 second
                } else {
                    statusRelay1.textContent = 'Status: Erreur';
                }
            })
            .catch(error => {
                statusRelay1.textContent = 'Status: Erreur lors de la requête';
            });
    });

    relay2Button.addEventListener('click', function () {
        fetch('/activate_relay?relay_number=2')
            .then(response => response.json())
            .then(data => {
                if (data.message.includes("activé")) {
                    statusRelay2.textContent = 'Status: Activé';
                } else {
                    statusRelay2.textContent = 'Status: Erreur';
                }
            })
            .catch(error => {
                statusRelay2.textContent = 'Status: Erreur lors de la requête';
            });
    });
});

