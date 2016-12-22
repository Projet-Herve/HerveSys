$(document).ready(function() {
    // Lorsque je soumets le formulaire
    $('#chatbot').on('submit', function(e) {
        e.preventDefault(); // J'empêche le comportement par défaut du navigateur, c-à-d de soumettre le formulaire
        var $this = $(this); // L'objet jQuery du formulaire
 
        // Je récupère les valeurs
        var chatbottext = $('#chatbottext').val();

        // Je vérifie une première fois pour ne pas lancer la requête HTTP
        // si je sais que mon PHP renverra une erreur
        if(chatbottext != '') {
            $(".messages").append('<p class="me">'+chatbottext+"</p>");
            // Envoi de la requête HTTP en mode asynchrone
            $.ajax({
                url: $this.attr('action'), // Le nom du fichier indiqué dans le formulaire
                type: "POST", // La méthode indiquée dans le formulaire (get ou post)
                data: $this.serialize(), // Je sérialise les données (j'envoie toutes les valeurs présentes dans le formulaire)
                success: function(json) { // Je récupère la réponse du fichier PHP
                    log>(json); // J'affiche cette réponse
                    
                    if(json.reponses.text != ''){
                        $(".messages").append("<p>"+json.reponses.text+"</p>");
                    }
                    if(json.reponses.html != ''){
                        $(".messages").append("<p>"+json.reponses.html+"</p>");
                    }
                    
                }
            });
        }
    });
});