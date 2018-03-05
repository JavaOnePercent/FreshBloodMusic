function permormer() {
        $.ajax({
            type: "POST",
            url: "best_performer/",
            dataType: "json",
            cache: false,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (data) {
                //alert(data.names + " " + data.images);
                var arrNames = data.names.toString().split(',');
                var arrImages = data.images.toString().split(',');
                var counter = 0;
                var arrLen = arrNames.length;
                if (data.names.toString() === "") arrLen = 0;
                if (arrLen > 0) {
                    $(".compositor").css("display", "block");
                }
                for (var i = $(".compositor").length; i < arrLen; i++)  //добавление элементов, в случае если на странице их меньше, чем пришло с сервера
                {
                    $(".compositor").clone().appendTo(".compositors");
                }
                for (var i = $(".compositor").length - 1; i >= arrLen; i--)  //удаление элементов, в случае если на странице их слишком много
                {
                    if (i === 0) {
                        $(".compositor").css("display", "none");
                    }
                    else
                        $($(".compositor")[i]).remove();
                }
                for (var i = 0; i < arrNames.length; i++) {
                    $($(".compositor-name")[i]).text(jQuery.trim(arrNames[i]));
                    $($(".compositor-avatar")[i]).attr("src", "/static/mainapp/performer_sources/" + jQuery.trim(arrImages[i]));
                }
            }
        });
}

permormer();

var csrftoken = getCookie('csrftoken');

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}