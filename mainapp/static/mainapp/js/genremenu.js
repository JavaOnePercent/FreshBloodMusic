$(function() {
    $(".janr").click(function() {
        var kek = "";
        genre(kek, this);
    });
});

function genre(kek, obj = null){
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
                for(var i=$(".music").length; i < arrLen-1; i++)  //добавление элементов, в случае если на странице их меньше, чем пришло с сервера
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

genre("1");

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

/*function nextTrackSuccessFunc(data) {         //функция успеха после получения следующего трека
	$("#trackname").text(data.track_name);
	$("#performername").text(data.performer_name);
	$("#audio").attr("src", data.file_link);
	startPlaying();
	trackID.current = data.current_id;
	trackID.next = data.next_id;
	$("#progressBarLine").animate({width: 0 + "%"}, 50);
	$("title").text(data.track_name);

	globalData = data;

	if(data.is_liked == true)
	{
	    is_liked = true;
	}
	else
	{
	    is_liked = false;
		$("#like").css("visibility", "hidden");
	}

	if(isFull)
	    nextTrackAnimation();
	else
	{
	    if(is_liked) $("#like").css("visibility", "visible");
	    logo = $("#logo").attr("src");
	    $("#logo").attr("src", globalData.logo_link);
        $("#prevlogo").attr("src", logo);
        $("#nextlogo").attr("src", globalData.nextlogo_link);
	}
}*/

/*jQuery(document).ready(function ($) {
    $('.view').click(changeView);
    function changeView() {
        $.ajax({
            type: "GET",
            url: "/app/change_view/",
            data:{
                'view':$(this).attr('data-v'),
            },
            dataType: "html",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    location.reload();
                }
            }
       });
    }
});*/
