$(function() {
    $(".janr").click(function() {
        $.ajax({
            type: "POST",
            url: "change_genre/",
            data: {
                gn:$(this).attr("name")
            },
            dataType: "json",
            cache: false,
            headers: {
              "X-CSRFToken": csrftoken
	        },
            success: function(data) {
                var brr;
                var crr;
                var j = 0;
                var k = 0;
                var arr = data.toString().split(',');
                for(var i = 0; i < arr.lastIndexOf(); i++)
                    if(i % 2 == 0){
                        brr[j] = arr(i);
                        j++;
                    }
                    else {
                        crr[k] = arr(i);
                        k++;
                    }

                //alert(arr[0]);
                for(var i = 0; i < brr.lastIndexOf(); i++) {
                    $($(".music-name").get(i)).text(brr[i]);
                    //document.getElementsByClassName(".music-name").get[i].innerText(brr[i]);
                    $($(".cover").get(i)).attr("src", "/static/mainapp/album_sources/" + crr[i]);
                }
            }
        });
    });

});


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
