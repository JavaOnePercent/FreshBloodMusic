$(function() {
	$("#playButton").click(function(){
		if(document.getElementById("audio").paused)
		{
			$("#audio").trigger('play');
			//$("#playButton").fadeToggle(0);
			$("#playButton").attr("src", "/static/mainapp/images/pauseButton.png");
			//$("#playButton").fadeToggle(500);
		}
		//$("#playButton").animate({visibility: 'hidden'}, 100);
		else
		{
			$("#audio").trigger('pause');
			//$("#playButton").fadeToggle(0);
			$("#playButton").attr("src", "/static/mainapp/images/playButton.png");
			
			//$("#playButton").fadeToggle(500);
		}
	});
});

$(function() {
	$("#playButton").mouseenter(function(){
		$("#playButton").animate({width: '+=7px', height: '+=7px'}, 50);
	});
});

$(function() {
	$("#playButton").mouseleave(function(){
		$("#playButton").animate({width: '-=7px', height: '-=7px'}, 50);
	});
});

$(function() {
	$("#nextButton").mouseenter(function(){
		$("#nextButton").animate({width: '+=7px', height: '+=7px'}, 50);
	});
});

$(function() {
	$("#nextButton").mouseleave(function(){
		$("#nextButton").animate({width: '-=7px', height: '-=7px'}, 50);
	});
});

$(function() {
	$("#previousButton").mouseenter(function(){
		$("#previousButton").animate({width: '+=7px', height: '+=7px'}, 50);
	});
});

$(function() {
	$("#previousButton").mouseleave(function(){
		$("#previousButton").animate({width: '-=7px', height: '-=7px'}, 50);
	});
});

$(function() {
	$("#logo").mouseenter(function(){
		$("#logo").animate({width: '+=10px', height: '+=10px'}, 100);
		
	});
});

$(function() {
	$("#logo").mouseleave(function(){
		$("#logo").animate({width: '-=10px', height: '-=10px'}, 100);
	});
});

$(function() {
	$("#nextButton").click(function(){
		var trackName = document.getElementById("trackname").innerHTML.split(" - ");
		var performerName = trackName[0];
		trackName = trackName[1];
		//document.getElementById("trackname").innerHTML = trackName + "_" + performerName;
		
		var varData = {
			track_name: trackName,
			performer_name: performerName
		};
		
		var jsonData = JSON.stringify(varData);
		var csrftoken = getCookie('csrftoken');
		//alert(jsonData);
		var jqxhr = $.ajax({
			type: "POST",
			url: 'next/',
			dataType: 'json',
			contentType: 'application/json',
			data: jsonData,
			async: false,
			headers: {
                "X-CSRFToken": csrftoken
			},
			success: function(data) {
				//alert(data.performer_name + " lol " + data.track_name);
				$("#trackname").text(data.performer_name + " - " + data.track_name);
				$("#audio").attr("src", data.file_link);
				$("#audio").trigger('play');
				$("#playButton").attr("src", "/static/audioplayer/pauseButton.png");
			}
		});
		//alert(jqxhr.responseText);
	});
});

$(function() {
	$("#previousButton").click(function(){
		
	});
});

// using jQuery
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
