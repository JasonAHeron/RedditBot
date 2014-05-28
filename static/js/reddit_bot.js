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
        var type_box;
        if ($('input[name=comment]:checked').val() === 1){
            type_box = "comment"
        } else if ($('input[name=title]:checked').val() === 1){
            type_box = "title"
        } else if ($('input[name=title_comment]:checked').val() === 1){
            type_box = "title_comment"
        }

        var action_box;
        if (1 === $('input[name=print]:checked').val()) {
            action_box = "print"
        } else if (1 === $('input[name=message]:checked').val()) {
            action_box = "message"
        } else if (1 === $('input[name=respond]:checked').val()) {
            action_box = "respond"
        }

        console.log("type: " + type_box);
        console.log("action: " + action_box);

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

                console.log(CryptoJS);
                console.log(data);

                $('#gen-code')
                    .html(data);

                // determine hash by pulling lists apart on commas
                var subreddits  = $('#ctrl-subreddits').val().replace(',','').replace(' ', ''),
                    searchwords = $('#ctrl-searchwords').val().replace(',','').replace(' ', ''),
                    hash        = CryptoJS.MD5(subreddits+searchwords+$('#ctrl-recipient').val()+type_box+action_box);

                $('#btn-gen-file').attr('href', 'http://reddit.jheron.io/static/bots/'+hash+'.py');
                $('#gen-container').show();
                $('#gen-alert-nocode').hide();

            });
    });

})(jQuery, Q, CryptoJS);