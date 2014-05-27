/*
 * RedditBot -- Javascript application
 */
(function($, Q){

    var api_url = 'http://reddit.jheron.io/';

    $('#gen-container').hide();

    // async post request
    function generate_code (data) {
        var deferred = Q.defer();

        $.post(api_url, data, function(res){
            deferred.resolve(res);
        });

        return deferred.promise;
    }

    // handle the form submission -- perform it asyncronously
    $('#btn-bot-form-submit').click(function(e){
        e.preventDefault();

        // get form control values
        var data = {
            subreddits  : $('#ctrl-subreddits').val(),
            searchwords : $('#ctrl-searchwords').val(),
            frequency   : $('#ctrl-frequency').val(),
            recipient   : $('#ctrl-recipient').val(),
            type        : "title",
            action      : "print"
        };

        // start by hiding the container

        generate_code(data)
            .then(function(data){

                $('#gen-code')
                    .html(data);

                $('#gen-container').show();

            });
    });

})(jQuery, Q);