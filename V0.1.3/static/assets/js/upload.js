// Fonction pour gérer l'upload de fichier
function handleFileUpload(fileInputId, imageType) {
    // Sélectionne l'élément input file
    const fileInput = document.getElementById(fileInputId);
    
    // Ajoute un écouteur d'événement pour détecter quand un fichier est sélectionné
    fileInput.addEventListener('change', function(event) {
        // Récupère le fichier sélectionné
        const file = event.target.files[0];
        
        // Crée un objet FormData pour envoyer le fichier
        const formData = new FormData();
        formData.append('file', file);
        formData.append('type', imageType);
        
        // Envoie une requête POST au serveur
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())  // Convertit la réponse en JSON
        .then(data => {
            if (data.success) {
                // Si l'upload est réussi, met à jour l'image affichée
                const imgElement = document.querySelector(imageType === 'pfp' ? '.pfp' : '.banner img');
                imgElement.src = data.url + '?' + new Date().getTime();  // Ajoute un timestamp pour éviter le cache
            } else {
                // Affiche une erreur si l'upload a échoué
                alert('Erreur lors de l\'upload : ' + data.error);
            }
        })
        .catch(error => {
            // Gère les erreurs de réseau ou autres
            console.error('Erreur:', error);
            alert('Une erreur est survenue lors de l\'upload.');
        });
    });
}

// Configure les uploads pour la photo de profil et la bannière
handleFileUpload('pfp-upload', 'pfp');
handleFileUpload('banner-upload', 'banner');

// Ajoute des écouteurs d'événements pour ouvrir le sélecteur de fichier au clic
document.querySelector('.change-pfp').addEventListener('click', function() {
    document.getElementById('pfp-upload').click();
});
document.querySelector('.change-banner').addEventListener('click', function() {
    document.getElementById('banner-upload').click();
});

console.log("HELOOO WORLDHELOOO WORLDHELOOO WORLDHELOOO WORLDHELOOO WORLDHELOOO WORLDHELOOO WORLDHELOOO WORLDHELOOO WORLDHELOOO WORLDHELOOO WORLDHELOOO WORLDHELOOO WORLD")