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
        var type_;
        if ($('input[name=comment]:checked').val() === 1){
            type_ = "comment"
        } else if ($('input[name=title]:checked').val() === 1){
            type_ = "title"
        } else if ($('input[name=title_comment]:checked').val() === 1){
            type_ = "title_comment"
        }

        var action_;
        if ($('input[name=print]:checked').val() === 1){
            action_ = "print"
        } else if ($('input[name=message]:checked').val() === 1){
            action_ = "message"
        } else if ($('input[name=respond]:checked').val() === 1){
            action_ = "respond"
        }

        console.log("type: " + type_);
        console.log("action: " + action_);

        var data = {
            subreddits  : $('#ctrl-subreddits').val(),
            searchwords : $('#ctrl-searchwords').val(),
            frequency   : $('#ctrl-frequency').val(),
            recipient   : $('#ctrl-recipient').val(),
            type        : type_,
            action      : action_
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
                    hash        = CryptoJS.MD5(subreddits+searchwords+$('#ctrl-recipient').val()+type_+action_);

                $('#btn-gen-file').attr('href', 'http://reddit.jheron.io/static/bots/'+hash+'.py');
                $('#gen-container').show();
                $('#gen-alert-nocode').hide();

            });
    });

})(jQuery, Q, CryptoJS);