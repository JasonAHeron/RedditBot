/*
 * RedditBot -- Javascript application
 */
(function($, Q){

    // var api_url = 'http://reddit.jheron.io/gen';
    var api_url = 'http://localhost:5000/gen';
    $('#gen-container').hide();

    // async post request
    function generate_code (data) {
        var deferred = Q.defer();

        $.post(api_url, data, function(res){
            console.log(res);
            deferred.resolve(res);
        });

        return deferred.promise;
    }

    // handle the form submission -- perform it asyncronously
    $('#btn-bot-form-submit').click(function(e){
        e.preventDefault();


        // get form control values
        var type_box;
        if ("1" === $('input[name=comment]:checked').val()) {
            type_box = "comment"
        } else if ("1" === $('input[name=title]:checked').val()) {
            type_box = "title"
        } else if ("1" === $('input[name=title_comment]:checked').val()) {
            type_box = "title_comment"
        }

        var action_box;
        if ("1" === $('input[name=print]:checked').val()) {
            action_box = "print"
        } else if ("1" === $('input[name=message]:checked').val()) {
            action_box = "message"
        } else if ("1" === $('input[name=respond]:checked').val()) {
            action_box = "respond"
        }

        var data = {
            subreddits  : $('#ctrl-subreddits').val(),
            searchwords : $('#ctrl-searchwords').val(),
            frequency   : $('#ctrl-frequency').val(),
            recipient   : $('#ctrl-recipient').val(),
            type        : type_box,
            action      : action_box
        };

        // start by hiding the container

        generate_code(data)
            .then(function(data){

                $('#gen-code')
                    .html(data.botcode);

                $('#btn-gen-file').attr('href', 'static/bots/'+data.hashcode+'.py');
                $('#gen-container').show();
                $('#gen-alert-nocode').hide();

            });
    });

})(jQuery, Q);