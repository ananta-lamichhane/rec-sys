$(document).ready(function(){


    $('#recommendation-rating-first').on('submit', function(event){ // signals the survey is done.

    var rating =  $('#slider-recom-rating').val(); // extract values from the form data
    var reclist_id1 = $('#reclist_id1').val()
    console.log("first rating submit"+ "rating : " + rating + " reclist_id1: "+reclist_id1)
      $.ajax({
         data: {
            rating: rating,
            reclist_id : reclist_id1
        },
        url: '/recommendations',
        type: 'post'
        });
        event.preventDefault();

    });

    $('#recommendation-rating-second').on('submit', function(event){ // signals the survey is done.
    var rating =  $('#slider-recom-rating-2').val(); // extract values from the form data
    var reclist_id2 = $('#reclist_id2').val()
    console.log("first rating submit"+ "rating : " + rating + " reclist_id2: "+reclist_id2)
      $.ajax({
         data: {
            rating: rating,
            reclist_id : reclist_id2
        },
        url: '/recommendations',
        type: 'POST'
        })
        .done(function(data){
            console.log("bye");
            window.location = '/bye';
        });
        event.preventDefault();

    });

});