function topmonth() {
        $.ajax({
            type: "POST",
            url: "top_month/",
            dataType: "json",
            cache: false,
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (data) {
                //alert(data.name_track + " " + data.like_track);
                $($(".track-top")).text(jQuery.trim(data.name_track));
                $($(".rating-top")).text("Понравилась: " + jQuery.trim(data.like_track));
                $($(".performer-top")).text(jQuery.trim(data.performer_track));
                $($(".img")).attr("src", "/static/mainapp/album_sources/" + jQuery.trim(data.image_track));


            }
        });
}

topmonth();

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