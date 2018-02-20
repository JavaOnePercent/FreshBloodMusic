var isFull = false;
var is_liked = false;
$(function() {

	$("#playButton").click(function(){
		if(document.getElementById("audio").paused)
		{
		    startPlaying();
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
	    if(isFull)
		    $("#playButton").animate({width: '+=7px', height: '+=7px'}, 50);
		else
	        $("#playButton").animate({width: '+=2px', height: '+=2px', left: '-=1px', top: '-=1px'}, 50);
	});
	$("#playButton").mouseleave(function(){
	    if(isFull)
		    $("#playButton").animate({width: '-=7px', height: '-=7px'}, 50);
		else
		    $("#playButton").animate({width: '-=2px', height: '-=2px', left: '+=1px', top: '+=1px'}, 50);
	});
	$("#nextButton").mouseenter(function(){
	    if(isFull)
	        $("#nextButton").animate({width: '+=7px', height: '+=7px'}, 50);
	    else
	        $("#nextButton").animate({width: '+=2px', height: '+=2px', left: '-=1px', top: '-=1px'}, 50);
	});
	$("#nextButton").mouseleave(function(){
	    if(isFull)
		    $("#nextButton").animate({width: '-=7px', height: '-=7px'}, 50);
		else
		    $("#nextButton").animate({width: '-=2px', height: '-=2px', left: '+=1px', top: '+=1px'}, 50);
	});
	$("#previousButton").mouseenter(function(){
		$("#previousButton").animate({width: '+=7px', height: '+=7px'}, 50);
	});
	$("#previousButton").mouseleave(function(){
		$("#previousButton").animate({width: '-=7px', height: '-=7px'}, 50);
	});
	$("#dropdown").mouseenter(function(){
		$("#dropdown").animate({width: '+=4px', height: '+=4px', right: '-=2px', top: '-=2px'}, 50);
	});
	$("#dropdown").mouseleave(function(){
		$("#dropdown").animate({width: '-=4px', height: '-=4px', right: '+=2px', top: '+=2px'}, 50);
	});

	$("#mainlogo").mouseenter(function(){
	    if(!is_liked)
	    {
	        $("#like").css('visibility', 'visible');
	        if(isFull)
	        {
		        $("#mainlogo").animate({width: '+=10px', height: '+=10px'}, 100);
		        $("#mainlogo").css('box-shadow', '1px 5px 28px #ff3079');
		    }
		    else
		        $("#mainlogo").animate({width: '+=4px', height: '+=4px', right: '-=2px', top: '-=2px'}, 100);
		}
	});
	$("#mainlogo").mouseleave(function(){
	    if(!is_liked)
	    {
	        $("#like").css('visibility', 'hidden');
	        if(isFull)
	        {
		        $("#mainlogo").animate({width: '-=10px', height: '-=10px'}, 100);
		        $("#mainlogo").css('box-shadow', '0px 4px 28px black');
		    }
		    else
		        $("#mainlogo").animate({width: '-=4px', height: '-=4px', right: '+=2px', top: '+=2px'}, 100);
		}
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

    $("#mainlogo").click(function() {
        if(is_liked == false)
        {
            var varData = {
		    	current_track: trackID.current
		    };

		    var jsonData = JSON.stringify(varData);
            sendJSON('like/', jsonData, successfulLikeFunc);
        }
    });

    function successfulLikeFunc(data)
    {
        if(data.result == "success")
        {
            is_liked = true;
            if(isFull)
            {
		        $("#mainlogo").animate({width: '-=10px', height: '-=10px'}, 100);
		        $("#mainlogo").css('box-shadow', '0px 4px 28px black');
		    }
		    else
		        $("#mainlogo").animate({width: '-=4px', height: '-=4px', right: '+=2px', top: '+=2px'}, 100);
        }
    }

    $("#menuPic").click(function() {
        $("#menuDropdown").fadeToggle(100);
    });

    $("#menuDropdown").mouseleave(function() {
        $("#menuDropdown").fadeToggle(100);
    });

    var allowChangeTime = false;
    $("#progress").mousedown(function(event){ //управление временем проигрывания currentTime
        allowChangeTime = true;
        clearInterval(timerId);
    });

    /*$("#progress").mouseup(function(event){ //управление временем проигрывания currentTime
        if(allowChangeTime)
        {
            var audio = $("audio").get(0);
            var seconds = event.pageX / $("#progress").width() * audio.duration;
            //$("#trackname").text(Number(seconds));
            audio.currentTime = seconds;
            allowChangeTime = false;
            timerId = setInterval(progressBar, 500);
        }
    });*/

    $("body").mousemove(function(event){ //управление временем проигрывания currentTime
        if(allowChangeTime)
        {
            //$("#trackname").text(event.pageX / $("#progress").width());
            //$("#progressBarLine").animate({width: event.pageX / $("#progress").width() * 100 + "%"}, 0);
            var seconds = event.pageX / $("#progress").width() * audio.duration;
            $("#progressBarLine").animate({width: event.pageX + "px"}, 0);
            setCurrentTime(seconds);
        }
    });

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
        if(allowChangeTime)
        {
            var audio = $("audio").get(0);
            var seconds = event.pageX / $("#progress").width() * audio.duration;
            //$("#trackname").text(audio.currentTime + "   " + seconds);

            audio.currentTime = Number(seconds);      //задание текущего времени проигрывания currentTime
            $("#progressBarLine").animate({width: event.pageX + "px"}, 0);
            timerId = setInterval(progressBar, 500);
            setCurrentTime(seconds);
        }
        allowChangeTime = false;
	});


    function makeMove(pageX) //передвижение ползунка громкости
    {
        //var offset = $("#ball").offset();
        var volOffset = $("#volume").offset();
        //var move = pageX - volOffset.left - $("#volume").width() / 2;
        //$("#ball").animate({left: move + "px", right: (-move) + "px"}, 0);
        var move = pageX - volOffset.left - 10;
        $("#ball").animate({left: move + "px"}, 0);

        $("#fillingLine").css("width", (pageX - volOffset.left) + "px");
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

    $("#dropdown").click(function(event){
        var source = null;
        var button = null;
        $('#prevlogo').attr("style", "");
        if(isFull)
        {
            source = "/static/mainapp/css/audioSmall.css";
            isFull = false;
            button = "/static/mainapp/images/dropdown.png";

            $('#prevlogo').css('visibility', 'hidden');
            //$('#nextlogo').css('visibility', 'hidden');
        }
        else
        {
            source = "/static/mainapp/css/audioFull.css";
            isFull = true;
            button = "/static/mainapp/images/closeDropdown.png";

            if($('#prevlogo').attr('src') != undefined)
                $('#prevlogo').css('visibility', 'visible');
            else
                $('#prevlogo').css('visibility', 'hidden');

            $('#maintoprevlogo').attr('src', $('#logo').attr('src'));
        }

        $("#dropdown").attr('src', button);
        $("#playerCSS").attr('href', source);

        $('#playButton').attr("style", "");
        $('#nextButton').attr("style", "");
        $('#mainlogo').attr("style", "");
        $('#nextlogo').attr("style", "");

        makeMove($("audio").get(0).volume * $("#volume").width() + $("#volume").offset().left);

        var volPer = $("audio").get(0).volume*100;
        $("#ball").animate({left: volPer - 7 + "%"}, 0);
        //$("#ball").animate({left: "-=10px"}, 0);
        $("#fillingLine").css("width", volPer + "%");

        //$('#dropdown').attr("style", "");
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
		    //alert(data.is_liked);
		    if(data.is_liked == true)
		    {
		        is_liked = true;
		        $("#like").css("visibility", "visible");
		    }
		    else
		    {
		        is_liked = false;
		        $("#like").css("visibility", "hidden");
		    }
			//alert(trackID.current + " " + trackID.next);
		}
	});

	$("#nextButton").click(nextTrack);
		//alert(jqxhr.responseText);

	$('audio').bind("ended", nextTrack);
    $('audio').bind("durationchange", setTrackLength);

    function nextTrack(){
        $("#like").css("visibility", "hidden");
		var varData = {
			current_track: trackID.current,
			next_track: trackID.next
		};

		var jsonData = JSON.stringify(varData);
		//alert(jsonData);
		sendJSON('next/', jsonData, nextTrackSuccessFunc); //////////////////////////////////////////////////////
	};
});

function nextTrackSuccessFunc(data) {         //функция успеха после получения следующего трека
	//alert(data.performer_name + " lol " + data.track_name);
	$("#trackname").text(data.track_name);
	$("#performername").text(data.performer_name);
	//$("title").text(data.track_name);
	$("#audio").attr("src", data.file_link);
	//$("#logo").attr("src", data.logo_link);
	//$("#nextlogo").attr("src", data.nextlogo_link)
	startPlaying();
	trackID.current = data.current_id;
	trackID.next = data.next_id;
	$("#progressBarLine").animate({width: 0 + "%"}, 100);
	$("title").text(data.track_name);
	//alert(trackID.current + " " + trackID.next);
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
}

function sendJSON(Url, jsonData, successFunc)
{
    var csrftoken = getCookie('csrftoken');
    $.ajax({
	type: "POST",
	url: Url,
	dataType: 'json',
	contentType: 'application/json',
	data: jsonData,
	async: true,
	headers: {
              "X-CSRFToken": csrftoken
	},
	success: successFunc
	})
};

var logo = null;
var globalData = null;

function nextTrackAnimation() {
      $("#mainlogo").css('visibility', 'hidden');  //главный вырубаем
      $("#prevlogo").animate({left: '-180%', right: '0', opacity: '0.0'}, 400);  //предыдущий улетает назад
      $("#prevlogo").animate({left: '-100%', right: '0', opacity: '0.3'}, 0); //предыдущий возвращается на свое место
	  $("#nextlogo").animate({width: '40%', height: '40%', left: '0', right: '0', opacity: '1'}, 400); //следующий двигается на место главного
	  $("#maintoprevlogo").css('visibility', 'visible');  //врубаем тот который съезжает с главного на предыдущий
      $("#maintoprevlogo").animate({width: '25%', height: '25%', left: '-100%', right: '0', opacity: '0.3'}, 400); //он двигается с главного назад
      setTimeout("$('#maintoprevlogo').css('visibility', 'hidden');", 400);//вырубаем прыгающий с главного назад
      logo = $("#logo").attr("src");
      $("#logo").attr("src", globalData.logo_link);   //меняем картинку на главном
      setTimeout("$('#maintoprevlogo').attr('src', globalData.logo_link);", 400);//меняем картинку на съезжаеющем с главного назад
      setTimeout("$('#mainlogo').css('visibility', 'visible'); $('#prevlogo').css('visibility', 'visible');", 400); //главный и предыдущий врубаем
      $("#nextlogo").animate({width: '25%', height: '25%', left: '', right: '-100%', opacity: '0.3'}, 0); //следующий прыгает на свое место
      setTimeout('$("#prevlogo").attr("src", logo);', 400);
      setTimeout('$("#nextlogo").attr("src", globalData.nextlogo_link);', 400); //меняем картинку на следующем

      setTimeout("$('#maintoprevlogo').animate({width: '40%', height: '40%', left: '0', right: '0', opacity: '1.0'}, 0);", 500); //возвращаем его на место главного
      setTimeout('if(is_liked) $("#like").css("visibility", "visible");', 400);
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

function progressBar()
{
    var audio = $("audio").get(0);
    var currTime = audio.currentTime;
    var progress = currTime / audio.duration * 100;
    $("#progressBarLine").animate({width: progress + "%"}, 250);
    mins = Math.floor(currTime / 60);
    secs = (currTime % 60).toFixed();
    $("#playedTime").text(mins + ":" + ((secs < 10) ? '0' + secs : secs));
}

var timerId = null;

function startPlaying(){
    //setTrackLength();
    clearInterval(timerId);
    timerId = setInterval(progressBar, 500);
    //
	$("#audio").trigger('play');
	//$("#playButton").fadeToggle(0);
	$("#playButton").attr("src", "/static/mainapp/images/pauseButton.png");
}

function setCurrentTime(seconds) { //установка таймера на текущее время
    //var progress = seconds / audio.duration * 100;
    mins = Math.floor(seconds / 60);
    secs = (seconds % 60).toFixed();
    $("#playedTime").text(mins + ":" + ((secs < 10) ? '0' + secs : secs));
}

function setTrackLength() {
    duration = $("audio").get(0).duration;
    mins = Math.floor(duration / 60);
    secs = duration % 60;
    $("#trackLength").text(mins + ":" + secs.toFixed());
}