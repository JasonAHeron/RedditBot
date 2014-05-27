/*
 * RedditBot -- Javascript application
 */
(function($, Q){

    // async post request
    function generate_code (data) {
        var deferred = Q.defer();
        $.post('', function(res){
            console.log('returned');
            deferred.resolve(res);
        });
        return deferred.promise();
    }

    // handle the form submission -- perform it asyncronously
    $('#search-form').submit(function(e){
        e.preventDefault();

        console.log("HOWDY");

        // get form control values
        var data = {
            subreddits  : 'a, b',
            searchwords : 'a, b',
            frequency   : 20,
            recipient   : 'nickswift498',
            type        : 'comment'
        };

        generate_code(data)
            .then(function(data){
                console.log(data);
            });
    });

})(jQuery, Q);