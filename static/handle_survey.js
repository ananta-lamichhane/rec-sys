$(document).ready(function(){

   /* $('#done-button').on('click', function(event){ // signals the survey is done.
        $.ajax({
         data: {
            done: 1,
            formtype: 1
        },
        url: '/survey',
        type: 'post'
        });
        event.preventDefault();
    });

    });*/


    $('#add-user-submit').on('click', function(event){ // signals the survey is done.
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

     var item_no=1 //keep track of how many elements are already displayed reset of each complete reload of the page.
    $('form').on('submit', function(event){ //sends POST request without refreshing the page.
    event.preventDefault();

        var rating =  $('#rating-slider').val(); // extract values from the form data
        var imdb_id = $('#imdbid').val();
        var checkbox = $('#poster-checkbox:checked').val();
        var checkbox_value = 0
        if(checkbox == 'on'){
            checkbox_value= 1;
        }

        if(item_no >= 10){ // reload to recommendations after 10 survey questions are asked.
            window.location = '/recommendations';
         }


        $.ajax({
            data: { //send back to backend (flask)
                rating: rating, // rating from the rating slider
                imdb_id: imdb_id, //current imdb id so that we can calculate next
                formtype: 2, //we want to distinguish between submission of ratings and other forms
                next_item: item_no, //keep track of how many items are already displayed
                dont_know: checkbox_value
            },
            url: '/survey',
            type: 'POST'
        })
        .done(function(data){ //when post request was successful do the following
         if(item_no >= 10){ // reload to recommendations after 10 survey questions are asked.
            window.location = '/recommendations';
         }else{
            item_no ++;
            curr = item_no -1;
            $('#survey-poster').attr('src', data['poster']); //update src attribute of the image with new URI
            $('#imdbid').attr('value', data['imdb_id']); //update IMDB ID of the movie
            var title_and_year = '' + data['title'] + '' + ' (' + data['year'] +')';
            $('#title-and-year').text(title_and_year); // update title and year which appears over the movie poster
            $('#plot-text').text(data['plot']);
            console.log("Director(s): "+ data['director']);
            $('#director-name').text('Director(s): ' + data['director']);
            $('#writer-name').text('Writer(s) ' + data['writer']);
            $('#genre').text('Genre: '+ data['genre']);
            $('#rating-output').text('0'); // reset output of the slider
            $('#rating-slider').val(0); // reset slider value
            $('#image-number').text(item_no); //increase item number
            $('#poster-checkbox').prop('checked',false); //reset checkbox
         }
        });

      //prevent form being submitted automatically after pressing submit
    });

});