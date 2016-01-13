'use strict';

$(function() {

    var order_detail = {};

    var gen_dish_payable = function() {
            var e = this;
            var name = $(e).find('.dish-name').html(),
                count = parseInt($(e).find('.dish-count').val()),
                price = parseFloat(
                            $(e).find('.price')
                                .html()
                                .split('$')[1]
                                .split('!')[0]
                        );
            return {
                name: name,
                count: count,
                price: price * count
            };
        },

        gen_dish_summary = function() {
            var subtotal = this.price.toFixed(2);
            var summary = '<p>' +
                '<span>' +
                    this.count + ' x ' + this.name +
                '</span>' +
                '<span class="pull-right">$ ' + subtotal + '</span>' +
                '</p>';
            return summary;
        },

        gen_all = function(dishes) {
            var all_summary = dishes.map(gen_dish_summary).get().join(' '),
                total_sum = dishes.map(function() { return this.price; }).get().reduce(function(a, b) { return a + b; });
            $('.per-dish').html(all_summary);
            $('.payable').html('Total: $ ' + total_sum.toFixed(2));
        },

        validate_field = function(obj, name, lo_bound, hi_bound) {
            return obj[name] && obj[name].length > lo_bound && obj[name].length <= hi_bound;
        },

        validate_contact = function(contact) {
            var has_phone = validate_field(contact, 'phone', 0, 8),
                has_name = validate_field(contact, 'name', 0, 32),
                has_location = validate_field(contact, 'location', 0, 32),
                has_zip = validate_field(contact, 'zipcode', 0, 6),
                has_slot = validate_field(contact, 'slot', 0, 1);
            return has_phone && has_name &&
                has_location && has_zip && has_slot;
        },

        get_contact_detail = function() {
            var phone = $('#phone'). val(),
                name = $('#name').val(),
                zipcode = $('#zip-code').val(),
                location = $('#location').val(),
                slot = $('input[name="deliver-time"]:checked').val(),
                remark = $('#remark').val();
            var contact = {
                phone: phone,
                name: name,
                zipcode: zipcode,
                location: location,
                slot: slot,
                remark: remark
            };
            console.log(contact);
            if (validate_contact(contact)) {
                order_detail.contact = contact;
                console.log(order_detail);
                $.ajax({
                    type: 'POST',
                    url: '/test/',
                    data: JSON.stringify(order_detail),
                    contentType: "application/json",
                }).done(function() { // data, status, jq) {
                    // console.log(data);
                    $('.order-done').html('<h2 class="pulled-left">&#10004; Sent</h2>');
                    alert("Thank you! You've successfully placed your order :)");
                    window.location.reload();
                }).fail(function(jq, status) {
                    console.log(jq, status);
                    alert("Sorry, we are having some technical issues, please come back in a while");
                });
            }
        };

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

    $('.order-done').click(function() {
        var dishes = $('.dish-preview')
            .map(gen_dish_payable)
            .filter(function() { return this.count > 0; });
        if (dishes.length > 0) {
            $('#order-choice').hide();
            $('body').scrollTop();
            $('#contact-detail').show().offset().top;
            $('body').scrollTop(0);
            order_detail.dishes = dishes.get();
            gen_all(dishes);
        }
        return false;
    });

    $('#submit-order').on('click', get_contact_detail);

    $('.trademark').on('click', function() {
        location.reload();
        // $('.dish-count').val(0);
        // $('#contact-detail').hide();
        // $('#order-choice').show();
    });

    $('#closed-modal').modal('show');
})
