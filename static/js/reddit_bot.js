/*
 * RedditBot -- Javascript application
 */
(function($, Q){

    var api_url = 'http://reddit.jheron.io/';

    // async post request
    function generate_code (data) {
        var deferred = Q.defer();

        $.post(api_url, data, function(res){
            console.log('returned');
            deferred.resolve(res);
        });

        return deferred.promise();
    }

    // handle the form submission -- perform it asyncronously
    $('#btn-bot-form-submit').click(function(e){
        e.preventDefault();

        // get form control values
        var data = {
            subreddits  : 'a, b',
            searchwords : 'a, b',
            frequency   : 20,
            recipient   : 'user',
            type        : 'title',
            action      : 'print'
        };

        generate_code(data)
            .then(function(data){
                console.log(data);
            });
    });

})(jQuery, Q);