$(document).ready(function(){
    // toastr settings
    toastr.options = {
        "debug": false,
        "positionClass": "toast-bottom-right",
        "onclick": null,
        "fadeIn": 300,
        "fadeOut": 1000,
        "timeOut": 5000,
        "extendedTimeOut": 1000
    }

    // Light - Dark Mode
    $('#toggle-mode, #sb-toggle-mode').click(function(e){
        e.preventDefault();
        $('body').toggleClass('darkmode');
        mode = $('body').hasClass('darkmode') ? 'dark' : 'light';
        $(this).removeClass('active');
        if(mode == 'dark'){
            $(this).addClass('active');
            $('.sb-uimode.active .text-dm').css('display', 'none');
            $('.sb-uimode.active .text-lm').css('display', 'inline');
        }else{
            $('.sb-uimode .text-dm').css('display', 'inline');
            $('.sb-uimode .text-lm').css('display', 'none');
        }
        localStorage.setItem("uiMode", mode);
    });


    // Get more category in home page
    $('.category_block .c_b-list .item-more').click(function(e){
        $('.category_block .c_b-list .item:nth-of-type(n+22)').css('display', 'block');
        $('.c_b-list').addClass('active');
    });
    // Get more category in sidebar
    $('.sidebar_menu-sub .sub-menu .nav-item.nav-more').click(function(e){
        $('#sidebar_menu .sidebar_menu-list>.nav-item .nav>.nav-item:nth-of-type(n+11)').css('display', 'block');
        $('.sidebar_menu-sub .sub-menu').addClass('active');
    });


    // Search bar
    $('.search-content input.search-input').focus(function(e){
        $('.search-content .search-result-pop').show()
    })
    $('body').click(function(e){
        if ($(e.target).hasClass('search-input') == false) { 
            $('.search-content .search-result-pop').hide();
        }
    })
    // var keepFocus = false;
    // function hideList(){
    //     if(!keepFocus){
    //         $('.search-content .search-result-pop').hide();
    //     }
    // }
    // $('.search-content input.search-input').blur(function() {
    //     keepFocus = false;
    //     window.setTimeout(hideList, 200);
    // }).focus(function(){
    //     keepFocus = true;
    // });

    // Modal auth
    $(document).on('click', '.link-highlight', function(e) {
        e.stopPropagation();
        var attrStep = $(this).attr('data-show');
        $(this).parents('.tab-pane').removeClass('active');
        $(attrStep).removeClass('fade');
        $(attrStep).addClass('active');
    });

    // Ajax login
    $('#login-form').submit(function(e){
        e.preventDefault()

        var csrftoken = jQuery('[name=csrfmiddlewaretoken]').val();
        var form = $(this);
        var $noti = $('#login-noti');
        var $loading = $('#login-loading');

        $noti.hide()
        $noti.empty()
        $noti.removeClass('alert-danger');
        $noti.removeClass('alert-success');

        $loading.show();

        $.ajax({
            url: form.attr("action"),
            method: form.attr("method"),
            data: {
                'form': form.serialize(),
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                var parsed_data = JSON.parse(response);
                $loading.hide();
                if(parsed_data.errorCode == 1){
                    $noti.addClass('alert-success');
                    location.reload();
                }else{
                    $noti.addClass('alert-danger');
                    $noti.show();
                    $noti.text(parsed_data.message);
                }
            },
            error: function(response){
                $loading.hide();
                location.reload();
            }
        });
    })

    // Ajax register
    $('#register-form').submit(function(e){
        e.preventDefault()

        var csrftoken = jQuery('[name=csrfmiddlewaretoken]').val();
        var form = $(this);
        var $noti = $('#register-noti');
        var $loading = $('#register-loading');

        $noti.hide()
        $noti.empty()
        $noti.removeClass('alert-danger');
        $noti.removeClass('alert-success');

        $loading.show();

        $.ajax({
            url: form.attr("action"),
            method: form.attr("method"),
            data: {
                'form': form.serialize(),
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                var parsed_data = JSON.parse(response);
                $loading.hide();
                if(parsed_data.errorCode == 1){
                    $noti.addClass('alert-success');
                    $noti.show();
                    $noti.text(parsed_data.message);
                }else{
                    $noti.addClass('alert-danger');
                    $noti.show();
                    $noti.text(parsed_data.message);
                }
            },
            error: function(response){
                $loading.hide();
                location.reload();
            }
        });
    });

    // Ajax forgot password
    $('#forgot-form').submit(function(e){
        e.preventDefault()

        var csrftoken = jQuery('[name=csrfmiddlewaretoken]').val();
        var form = $(this);
        var $noti = $('#forgot-noti');
        var $loading = $('#forgot-loading');

        $noti.hide()
        $noti.empty()
        $noti.removeClass('alert-danger');
        $noti.removeClass('alert-success');

        $loading.show();

        $.ajax({
            url: form.attr("action"),
            method: form.attr("method"),
            data: {
                'form': form.serialize(),
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                var parsed_data = JSON.parse(response);
                $loading.hide();
                if(parsed_data.errorCode == 1){
                    $noti.addClass('alert-success');
                    $noti.show();
                    $noti.text(parsed_data.message);
                }else{
                    $noti.addClass('alert-danger');
                    $noti.show();
                    $noti.text(parsed_data.message);
                }
            },
            error: function(response){
                $loading.hide();
                console.log(response);
                location.reload();
            }
        });
    });

    // Ajax reset password
    $('#reset-form').submit(function(e){
        e.preventDefault()

        var csrftoken = jQuery('[name=csrfmiddlewaretoken]').val();
        var form = $(this);
        var $noti = $('#reset-noti');
        var $loading = $('#reset-loading');

        $noti.hide()
        $noti.empty()
        $noti.removeClass('alert-danger');
        $noti.removeClass('alert-success');

        $loading.show();

        $.ajax({
            url: form.attr("action"),
            method: form.attr("method"),
            data: {
                'form': form.serialize(),
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                var parsed_data = JSON.parse(response);
                $loading.hide();
                if(parsed_data.errorCode == 1){
                    $noti.addClass('alert-success');
                    $noti.show();
                    $noti.text(parsed_data.message);
                }else{
                    $noti.addClass('alert-danger');
                    $noti.show();
                    $noti.text(parsed_data.message);
                }
            },
            error: function(response){
                $loading.hide();
                console.log(response);
                location.reload();
            }
        });
    });


    // search chapter
    $('.search-reading-item').on('input', function(e){
        number = $(this).val();
        var container = $('#en-chapters');
        container.find('li').removeClass('highlight');
        liElement = $("#en-chapters li[data-number='" + number +"']");
        if(liElement.length){
            var scrollTo = liElement.offset().top - container.offset().top + container.scrollTop();
            $('#en-chapters').animate({ 
                scrollTop: scrollTo
            }, 'medium');
            liElement.addClass('highlight');
        }
    });

    $('#dropdown-chapters').on('shown.bs.dropdown', function(e){
        var $container = $('.rt-chap #en-chapters');
        var $liElement = $container.find('li.active');;
        if($liElement.length){
            var scrollTo = $liElement.offset().top - $container.offset().top + $container.scrollTop();
            $container.animate({ 
                scrollTop: scrollTo
            }, 'medium');
        }
    });


    // sidebar
    $('#mobile_menu, #sidebar_menu_bg, .toggle-sidebar').click(function(e){
        $('#sidebar_menu').toggleClass('active');
        $('#sidebar_menu_bg').toggleClass('active');
    });

    $('#mobile_search').click(function(e){
        $('#search').toggleClass('active');
    });

    $('.detail-toggle').click(function(e){
        $(this).toggleClass('active');
        $('.anis-content').toggleClass('active');
    })
});