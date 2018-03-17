$(function() {
    $(".janr").click(function() {
        var kek = "";
        genre(kek, this);
    });
});

function genre(kek){
    if(kek == "") {
        kek = $(obj).attr("name");
    }
        $.ajax({
            type: "POST",
            url: "change_genre/",
            data: {
                gn:kek
            },
            dataType: "json",
            cache: false,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(data) {
                //alert(data.names + " " + data.images);
                var arrNames = data.names.toString().split(',');
                var arrImages = data.images.toString().split(',');
                var counter = 0;
                var arrLen = arrNames.length;
                if(data.names.toString() === "") arrLen = 0;
                 if(arrLen > 0) {
                        $(".music").css("display", "block");
                    }
                for(var i=$(".music").length; i < arrLen; i++)  // убрал тут arrLen - 1, ибо вроде не нужно//добавление элементов, в случае если на странице их меньше, чем пришло с сервера
                {

                    $(".music").clone().appendTo(".compilation");
                }
                for(var i=$(".music").length-1; i >= arrLen; i--)  //удаление элементов, в случае если на странице их слишком много
                {
                    if(i === 0)
                    {
                        $(".music").css("display", "none");
                    }
                    else
                    $($(".music")[i]).remove();
                }


                for(var i = 0; i < arrNames.length; i++) {

                        $($(".music-name")[i]).text(jQuery.trim(arrNames[i]));
                        $($(".cover")[i]).attr("src", "/static/mainapp/album_sources/" + jQuery.trim(arrImages[i]));
                }
            }
        });
}


var csrftoken = getCookie('csrftoken');

genre("1");

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
