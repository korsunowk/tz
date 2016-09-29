/**
 * Created by 1 on 26.03.2016.
 */

$('.js-captcha-refresh').click(function(){
        $form = $(this).parents('form');

        $.getJSON($(this).data('url'), {}, function(json) {
            // This should update your captcha image src and captcha hidden input
        });

        return false;
    });