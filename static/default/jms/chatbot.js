function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}
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
            var n = $(".messages").height();
            $('.messages').animate({ scrollTo: n }, 50);
            // Envoi de la requête HTTP en mode asynchrone
            $.ajax({
                url: $this.attr('action'), // Le nom du fichier indiqué dans le formulaire
                type: "GET", // La méthode indiquée dans le formulaire (get ou post)
                data: $this.serialize(), // Je sérialise les données (j'envoie toutes les valeurs présentes dans le formulaire)
                success: function(json) { // Je récupère la réponse du fichier PHP
                    $this.closest('form').find("input[type=text]").val("");
                    log>(json); // J'affiche cette réponse

                    if(json.reponses.text != ''){
                        $(".messages").append("<p>"+capitalize(json.reponses.text)+"</p>");
                    }
                    if(json.ERREUR){
                        $(".messages").append("<p> Hoho il y a une erreur ... => "+capitalize(json.ERREUR)+"</p>");
                    }
                    if(json.reponses.html != ''){
                        $(".messages").append(json.reponses.html);
                    }
                    if(json.reponses.links != ''){
                        $(".messages").append("<p><a href='"+json.reponses.links+"'>"+json.reponses.links+"</a></p>");
                    }
                    var n = $(".messages").height();
                    $('.messages').animate({ scrollTo: n }, 0);
                }
            });
        }
    });
});