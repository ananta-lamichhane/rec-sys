$(document).ready(function(){

<<<<<<< HEAD
    $('#done-button').on('click', function(event){ // signals the survey is done.
=======
   /* $('#done-button').on('click', function(event){ // signals the survey is done.
>>>>>>> 0edd2ec24e59cc1e475a18d2264926289737cbae
        $.ajax({
         data: {
            done: 1,
            formtype: 1
        },
        url: '/survey',
        type: 'post'
        });
        event.preventDefault();

<<<<<<< HEAD
    });
=======
    });*/
>>>>>>> 0edd2ec24e59cc1e475a18d2264926289737cbae

        $('#reset-button').on('click', function(event){ // signals the survey is done.
        $.ajax({
         data: {
            done: 1,
            formtype: 3
        },
        url: '/survey',
        type: 'post'
        });
        event.preventDefault();

    });


    $('form').on('submit', function(event){ //sends POST request without refreshing the page.
        var imdb_id= $(this).attr('id');

        //var imdb_id = $('#imdb_id').val();
        console.log(imdb_id);
        var rating =  $('#rating'+imdb_id).val();
        console.log(rating);

        $.ajax({
            data: {
                rating: rating,
                imdb_id: imdb_id,
                formtype: 2
            },
            url: '/survey',
            type: 'POST'
        })
        .done(function(data){

        });

        event.preventDefault(); //prevent form being submitted automatically after pressing submit
    });

});