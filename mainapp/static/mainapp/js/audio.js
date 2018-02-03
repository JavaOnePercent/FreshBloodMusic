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

	$("#playButton").mouseenter(function(){
		$("#playButton").animate({width: '+=7px', height: '+=7px'}, 50);
	});
	$("#playButton").mouseleave(function(){
		$("#playButton").animate({width: '-=7px', height: '-=7px'}, 50);
	});
	$("#nextButton").mouseenter(function(){
		$("#nextButton").animate({width: '+=7px', height: '+=7px'}, 50);
	});
	$("#nextButton").mouseleave(function(){
		$("#nextButton").animate({width: '-=7px', height: '-=7px'}, 50);
	});
	$("#previousButton").mouseenter(function(){
		$("#previousButton").animate({width: '+=7px', height: '+=7px'}, 50);
	});
	$("#previousButton").mouseleave(function(){
		$("#previousButton").animate({width: '-=7px', height: '-=7px'}, 50);
	});
	$("#logo").mouseenter(function(){
		$("#logo").animate({width: '+=10px', height: '+=10px'}, 100);
		$("#like").css('visibility', 'visible');

	});
	$("#logo").mouseleave(function(){
		$("#logo").animate({width: '-=10px', height: '-=10px'}, 100);
		$("#like").css('visibility', 'hidden');
	});

	$("#nextButton").click(function(){
        nextTrackAnimation();

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

	$("#previousButton").click(function(){
		
	});
});


function nextTrackAnimation() {
      $("#logo").css('visibility', 'hidden');  //главный вырубаем
	  $("#nextlogo").animate({width: '40%', height: '40%', left: '0', right: '0', opacity: '1'}, 400); //следующий двигается на место главного
	  $("#prevlogo").css('visibility', 'visible');  //врубаем предыдущий
      $("#prevlogo").animate({width: '25%', height: '25%', left: '-100%', right: '0', opacity: '0.3'}, 400); //предыдущий двигается с главного назад
      $("#logo").attr("src", "/static/mainapp/images/Cover1.jpg");   //меняем картинку на главном
      setTimeout("$('#logo').css('visibility', 'visible');", 400); //главный врубаем
      $("#nextlogo").animate({width: '25%', height: '25%', left: '', right: '-100%', opacity: '0.3'}, 0); //следующий прыгает на свое место
       setTimeout('$("#nextlogo").attr("src", "/static/mainapp/images/Cover2.jpg")', 400); //меняем картинку на следующем
}

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
