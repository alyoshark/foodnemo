'use strict';

$(function() {
    $('.plus1').on('click', function() {
        var last = parseInt($(this).prev().val()) || 0;
        $(this).prev().val(last + 1);
        return false;
    });

    $('.minus1').on('click', function() {
        var last = parseInt($(this).next().val()) || 0;
        if (last > 0) {
            $(this).next().val(last - 1);
        }
        return false;
    });
})
