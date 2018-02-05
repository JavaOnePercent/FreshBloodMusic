$(function() {
	$("#playButton").click(function(){
		if(document.getElementById("audio").paused)
		{
		    var timerId = setInterval(progressBar, 1000);
			$("#audio").trigger('play');
			//$("#playButton").fadeToggle(0);
			$("#playButton").attr("src", "/static/mainapp/images/pauseButton.png");
			//$("#playButton").fadeToggle(500);
		}
		//$("#playButton").animate({visibility: 'hidden'}, 100);
		else
		{
		    clearInterval(timerId);
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
	$("#mainlogo").mouseenter(function(){
		$("#mainlogo").animate({width: '+=10px', height: '+=10px'}, 100);
		$("#like").css('visibility', 'visible');

	});
	$("#mainlogo").mouseleave(function(){
		$("#mainlogo").animate({width: '-=10px', height: '-=10px'}, 100);
		$("#like").css('visibility', 'hidden');
	});

    var volume = $("audio").get(0).volume;

    $("#speaker").click(function() {
        var vol = $("audio").get(0).volume;
        var volOffset = $("#volume").offset().left;
        if(vol != 0.0)
        {
            makeMove(volOffset);
            volume = vol;
            $("#speaker").attr("src", "/static/mainapp/images/speaker0.png");
            $("audio").get(0).volume = 0.0;
        }
        else
        {
            makeMove(volOffset + volume*$("#volume").width())
            $("audio").get(0).volume = volume;
            if(volume <= 0.33)
            $("#speaker").attr("src", "/static/mainapp/images/speaker33.png");
            else if(volume <= 0.66)
            $("#speaker").attr("src", "/static/mainapp/images/speaker66.png");
            else if(volume <= 1.0)
            $("#speaker").attr("src", "/static/mainapp/images/speaker100.png");
        }
    });

    function progressBar()
    {
        var audio = $("audio").get(0);
        var progress = audio.currentTime / audio.duration * 100;
        $("#progressBar").animate({width: progress + "%"}, 0);
    }

    var allowMove = false;
    $("#draggingZone").mousedown(function(event){

        allowMove = true;
        makeMove(event.pageX);
	});

    $("#draggingZone").mouseenter(function(event){
        $("body").css("cursor", "pointer");
	});

    $("#draggingZone").mouseleave(function(event){
        $("body").css("cursor", "default");
	});

    $("#ball").mousedown(function(event){

        allowMove = true;
	});

    $("body").mouseup(function(event){
        allowMove = false;
	});

    function makeMove(pageX) //передвижение ползунка громкости
    {
        var offset = $("#ball").offset();
        var volOffset = $("#volume").offset();
        var move = pageX - offset.left - 10;
        $("#ball").css("left", "+=" + move + "px");
        $("#ball").css("right", "-=" + move + "px");
        $("#fillingLine").css("width", "+=" + move + "px");
        var volume = (pageX - volOffset.left)/$("#volume").width();
        $("audio").get(0).volume = volume;
        if(volume <= 0.01)
        {
            $("#speaker").attr("src", "/static/mainapp/images/speaker0.png");
            $("audio").get(0).volume = 0.0;
        }
        else if(volume <= 0.33)
            $("#speaker").attr("src", "/static/mainapp/images/speaker33.png");
        else if(volume <= 0.66)
            $("#speaker").attr("src", "/static/mainapp/images/speaker66.png");
        else if(volume <= 1.0)
            $("#speaker").attr("src", "/static/mainapp/images/speaker100.png");
    };

    $("#draggingZone").mousemove(function(event){
        if(allowMove) {
            makeMove(event.pageX);
        }
    });


    trackID = {
        current: null,
        next: null
    };

    var csrftoken = getCookie('csrftoken');
    $.ajax({
		type: "GET",
		url: 'first/',
		async: true,
		headers: {
            "X-CSRFToken": csrftoken
		},
		success: function(data) {
		    trackID.current = data.first_id;
		    trackID.next = data.second_id;
			//alert(trackID.current + " " + trackID.next);
		}
	});

	$("#nextButton").click(nextTrack);
		//alert(jqxhr.responseText);

	$('audio').bind("ended", nextTrack);

    function nextTrack(){


		var trackName = document.getElementById("trackname").innerHTML.split(" - ");
		var performerName = trackName[0];
		trackName = $("title").text();

		var varData = {
			current_track: trackID.current,
			next_track: trackID.next
		};

		var jsonData = JSON.stringify(varData);
		//var csrftoken = getCookie('csrftoken');
		//alert(jsonData);
		var jqxhr = $.ajax({
			type: "POST",
			url: 'next/',
			dataType: 'json',
			contentType: 'application/json',
			data: jsonData,
			async: true,
			headers: {
                "X-CSRFToken": csrftoken
			},
			success: function(data) {
				//alert(data.performer_name + " lol " + data.track_name);
				$("#trackname").text(data.performer_name + " - " + data.track_name);
				$("title").text(data.track_name)
				$("#audio").attr("src", data.file_link);
				//$("#logo").attr("src", data.logo_link);
				//$("#nextlogo").attr("src", data.nextlogo_link);
				$("#audio").trigger('play');
				$("#playButton").attr("src", "/static/mainapp/images/pauseButton.png");
				trackID.current = data.current_id;
				trackID.next = data.next_id;
				//alert(trackID.current + " " + trackID.next);
				globalData = data;
				nextTrackAnimation();
			}
		});
	};
});

var logo = null;
var globalData = null;

function nextTrackAnimation() {
      $("#mainlogo").css('visibility', 'hidden');  //главный вырубаем
      $("#prevlogo").animate({left: '-180%', right: '0', opacity: '0.0'}, 400);  //предыдущий улетает назад
      $("#prevlogo").animate({left: '-100%', right: '0', opacity: '0.3'}, 0); //предыдущий возвращается на свое место
	  $("#nextlogo").animate({width: '40%', height: '40%', left: '0', right: '0', opacity: '1'}, 400); //следующий двигается на место главного
	  $("#maintoprevlogo").css('visibility', 'visible');  //врубаем тот который съезжает с главного на предыдущий
      $("#maintoprevlogo").animate({width: '25%', height: '25%', left: '-100%', right: '0', opacity: '0.3'}, 400); //он двигается с главного назад
      logo = $("#logo").attr("src");
      $("#logo").attr("src", globalData.logo_link);   //меняем картинку на главном
      setTimeout("$('#maintoprevlogo').attr('src', globalData.logo_link);", 400);//меняем картинку на съезжаеющем с главного назад
      setTimeout("$('#mainlogo').css('visibility', 'visible'); $('#prevlogo').css('visibility', 'visible');", 400); //главный и предыдущий врубаем
      $("#nextlogo").animate({width: '25%', height: '25%', left: '', right: '-100%', opacity: '0.3'}, 0); //следующий прыгает на свое место
      setTimeout('$("#nextlogo").attr("src", globalData.nextlogo_link);', 400); //меняем картинку на следующем
      setTimeout("$('#maintoprevlogo').css('visibility', 'hidden');", 400);  //вырубаем прыгающий с главного назад
      $("#maintoprevlogo").animate({width: '40%', height: '40%', left: '0', right: '0', opacity: '1.0'}, 0); //возвращаем его на место главного
      setTimeout('$("#prevlogo").attr("src", logo);', 400);
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