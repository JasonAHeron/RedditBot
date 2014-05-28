/*
 * RedditBot -- Javascript application
 */
(function($, Q, CryptoJS){

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

                console.log(CryptoJS);
                console.log(data);

                $('#gen-code')
                    .html(data);

                // determine hash by pulling lists apart on commas
                var subreddits  = $('#ctrl-subreddits').val().replace(',','').replace(' ', ''),
                    searchwords = $('#ctrl-searchwords').val().replace(',','').replace(' ', ''),
                    hash        = CryptoJS.MD5(subreddits+searchwords+$('#ctrl-recipient').val()+"title"+"print");

                $('#btn-gen-file').attr('href', 'http://reddit.jheron.io/static/bots/'+hash+'.py');
                $('#gen-container').show();
                $('#gen-alert-nocode').hide();

            });
    });

})(jQuery, Q, CryptoJS);