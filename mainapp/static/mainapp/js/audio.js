var isFull = false;
var is_liked = false;
var trackLenPer = null;

$(function() {

	$("#playButton").click(function(){
		if(document.getElementById("audio").paused)
		{
		    startPlaying();
		}
		else
		{
		    clearInterval(timerId);
			$("#audio").trigger('pause');
			$("#playButton").attr("src", "/static/mainapp/images/playButton.png");
		}
	});

	/*$("#playButton").mouseenter(function(){
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
	});*/
	$("#previousButton").mouseenter(function(){
		$("#previousButton").animate({width: '+=7px', height: '+=7px'}, 50);
	});
	$("#previousButton").mouseleave(function(){
		$("#previousButton").animate({width: '-=7px', height: '-=7px'}, 50);
	});
	/*
	$("#dropdown").mouseenter(function(){
		$("#dropdown").animate({width: '+=2px', height: '+=2px', right: '-=1px', top: '-=1px'}, 50);
	});
	$("#dropdown").mouseleave(function(){
		$("#dropdown").animate({width: '-=2px', height: '-=2px', right: '+=1px', top: '+=1px'}, 50);
	});*/

	$("#mainlogo").mouseenter(function(){
	    if(!is_liked)
	    {
	        $("#like").css('visibility', 'visible');
	        if(isFull)
	        {
		        //$("#mainlogo").animate({width: '+=10px', height: '+=10px'}, 100);
		        //$("#mainlogo").css('box-shadow', '1px 5px 28px #ff3079');
		    }
		    //else
		    //    $("#mainlogo").animate({width: '+=2px', height: '+=2px', right: '-=1px', top: '-=1px'}, 100);
		}
	});
	$("#mainlogo").mouseleave(function(){
	    if(!is_liked)
	    {
	        $("#like").css('visibility', 'hidden');
	        if(isFull)
	        {
		        //$("#mainlogo").animate({width: '-=10px', height: '-=10px'}, 100);
		        //$("#mainlogo").css('box-shadow', '0px 4px 28px black');
		    }
		    //else
		    //    $("#mainlogo").animate({width: '-=2px', height: '-=2px', right: '+=1px', top: '+=1px'}, 100);
		}
	});

    var volume = $("audio").get(0).volume;

    $("#speaker").mouseenter(function() {
        if(!isFull)
            $("#volume").fadeToggle(100);

    });
    $("#speaker").click(function() {
        var vol = $("audio").get(0).volume;
        var volOffset = $("#volume").offset().left;
        if(vol != 0.0)
        {
            makeMove(volOffset);
            volume = vol;
            $("#speakerPic").attr("src", "/static/mainapp/images/speaker0.png");
            $("audio").get(0).volume = 0.0;
        }
        else
        {
            makeMove(volOffset + volume*$("#volume").width());
            $("audio").get(0).volume = volume;
            if(volume <= 0.33)
            $("#speakerPic").attr("src", "/static/mainapp/images/speaker33.png");
            else if(volume <= 0.66)
            $("#speakerPic").attr("src", "/static/mainapp/images/speaker66.png");
            else if(volume <= 1.0)
            $("#speakerPic").attr("src", "/static/mainapp/images/speaker100.png");
        }
    });

    $("#mainlogo").click(function() {
        var varData = {
                option: "",
		    	current_track: trackID.current
		    };
        if(is_liked == false)
        {
            varData.option = "add";
        }
        else
        {
            varData.option = "remove";
        }

		var jsonData = JSON.stringify(varData);
        sendJSON('like/', jsonData, successfulLikeFunc);
    });

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
            var xCoord = event.pageX - $("#player").offset().left;
            if(xCoord <= $("#player").width())
            {
                var seconds = xCoord / $("#progress").width() * audio.duration;
                $("#progressBarLine").animate({width: xCoord + "px"}, 0);
                setCurrentTime(seconds);
                timeColorChanger();
            }
        }
    });

    var allowMove = false;
    $("#draggingZone").mousedown(function(event){

        allowMove = true;
        if(isFull)
            makeMove(event.pageX);
        else
            makeMove(null, event.pageY);
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
            var xCoord = event.pageX - $("#player").offset().left;
            if(xCoord <= $("#player").width())
            {
                var seconds = xCoord / $("#progress").width() * audio.duration;
                //$("#trackname").text(audio.currentTime + "   " + seconds);

                audio.currentTime = Number(seconds);      //задание текущего времени проигрывания currentTime
                $("#progressBarLine").animate({width: xCoord + "px"}, 0);
                timerId = setInterval(progressBar, 500);
                setCurrentTime(seconds);
                timeColorChanger();
            }
        }
        allowChangeTime = false;
	});

    $("#draggingZone").mousemove(function(event){
        if(allowMove) {
            if(isFull)
                makeMove(event.pageX);
            else
                makeMove(null, event.pageY);
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
            isPlayedTimeColorChanged = false;
            isTrackLengthColorChanged = false;
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
        var likeStyle = $('#like').attr('style');
        $('*').attr("style", "");
        $('#like').attr('style', likeStyle);
        /*$('#playButton').attr("style", "");
        $('#nextButton').attr("style", "");
        $('#mainlogo').attr("style", "");
        $('#nextlogo').attr("style", "");
        $('#dropdown').attr("style", "");
        $('#progress').attr("style", "");
        $('#trackLength').attr("style", "");
        $('#playedTime').attr("style", "");
        $('#volume').attr("style", "");
        $('#line').attr("style", "");
        $('#fillingLine').attr("style", "");
        $('#ball').attr("style", "");*/

        //makeMove($("audio").get(0).volume * $("#volume").width() + $("#volume").offset().left);

        //var volPer = $("audio").get(0).volume*100;
        //$("#ball").animate({left: volPer - 7 + "%"}, 0);
        //$("#fillingLine").css("width", volPer + "%");

    });

	$("#nextButton").click(nextTrack);

	$('audio').bind("ended", nextTrack);
    $('audio').bind("durationchange", setTrackLength);

    $("#player").mouseenter(function(){
        trackLenPer = Number(99.5) - Number($("#trackLength").width() / $("#player").width() * 100);
        $("#progress").animate({height: '14px'}, 100);
        $("#trackLength").css("visibility", "visible");
        $("#playedTime").css("visibility", "visible");
    });

    $("#player").mouseleave(function(){
        trackLenPer = null;
        $("#progress").animate({height: '4px'}, 100);
        if(!isFull)
        {
            $("#trackLength").css("visibility", "hidden");
            $("#playedTime").css("visibility", "hidden");
            if($("#volume").css("display") != "none")
                $("#volume").fadeToggle(100);
        }
    });
});

function makeMove(pageX, pageY = null) //передвижение ползунка громкости
{
    var volOffset = $("#volume").offset();
    if(pageX != null)
    {
        var move = pageX - volOffset.left - 10;
        $("#ball").animate({left: move + "px"}, 0);
        $("#fillingLine").css("width", (pageX - volOffset.left) + "px");
        var volume = (pageX - volOffset.left)/$("#volume").width();
    }
    else if(pageY != null)
    {
        var move = $("#line").height() - (pageY - volOffset.top) - 10;
        $("#ball").animate({bottom: move + "px"}, 0);
        $("#fillingLine").css("height", (move + 10) + "px");
        var volume = (move + 10)/$("#line").height();
    }
    $("audio").get(0).volume = volume;
    if(volume <= 0.01)
    {
        $("#speakerPic").attr("src", "/static/mainapp/images/speaker0.png");
        $("audio").get(0).volume = 0.0;
    }
    else if(volume <= 0.33)
        $("#speakerPic").attr("src", "/static/mainapp/images/speaker33.png");
    else if(volume <= 0.66)
        $("#speakerPic").attr("src", "/static/mainapp/images/speaker66.png");
    else if(volume <= 1.0)
        $("#speakerPic").attr("src", "/static/mainapp/images/speaker100.png");
};

trackID = {
        current: null,
        next: null
    };

nextTrack();
isFirst = true;

var csrftoken = getCookie('csrftoken');

function nextTrack(){
    $("#like").css("visibility", "hidden");
	var varData = {
		current_track: trackID.current,
		next_track: trackID.next
	};
	var jsonData = JSON.stringify(varData);
	sendJSON('next/', jsonData, nextTrackSuccessFunc);
};

var isPlayedTimeColorChanged = false;
var	isTrackLengthColorChanged = false;

function nextTrackSuccessFunc(data) {         //функция успеха после получения следующего трека
    timeColorChanger();
	$("#trackname").text(data.track_name);
	$("#performername").text(data.performer_name);
	$("#audio").attr("src", data.file_link);
	if(!isFirst)
	    startPlaying();
	else
	    isFirst = false;
	trackID.current = data.current_id;
	trackID.next = data.next_id;
	$("#progressBarLine").animate({width: 0 + "%"}, 50);
	isPlayedTimeColorChanged = false;
	isTrackLengthColorChanged = false;
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
}

function sendJSON(Url, jsonData, successFunc, isFirst)
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

function successfulLikeFunc(data)
{
    if(data.result == "added")
    {
        is_liked = true;
        $("#like").css('visibility', 'visible');
	        //$("#mainlogo").animate({width: '-=10px', height: '-=10px'}, 100);
	        //$("#mainlogo").css('box-shadow', '0px 4px 28px black');
	}
	else if(data.result == "removed")
	{
        is_liked = false;
        $("#like").css('visibility', 'hidden');
	}
	    //$("#mainlogo").animate({width: '-=4px', height: '-=4px', right: '+=2px', top: '+=2px'}, 100);

}

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
    timeColorChanger();
    mins = Math.floor(currTime / 60);
    secs = (currTime % 60).toFixed();
    $("#playedTime").text(mins + ":" + ((secs < 10) ? '0' + secs : secs));
}

function timeColorChanger(progress = null)
{
    if(!isFull)
    {
        if(progress == null)
        {
            var audio = $("audio").get(0);
            var currTime = audio.currentTime;
            progress = currTime / audio.duration * 100;
        }
        if(trackLenPer != null)
        {
            if(progress >= 0.5 && isPlayedTimeColorChanged == false)
            {
                $("#playedTime").css("color", "white");
                isPlayedTimeColorChanged = true;
            }
            else if(progress < 0.5)
            {
                $("#playedTime").css("color", "black");
                isPlayedTimeColorChanged = false;
            }

            if(progress >= trackLenPer && isTrackLengthColorChanged == false)
            {
                $("#trackLength").css("color", "white");
                isTrackLengthColorChanged = true;
            }
            else if(progress < trackLenPer)
            {
                $("#trackLength").css("color", "black");
                isTrackLengthColorChanged = false;
            }
        }
    }
}

var timerId = null;

function startPlaying(){
    clearInterval(timerId);
    timerId = setInterval(progressBar, 500);
	$("#audio").trigger('play');
	$("#playButton").attr("src", "/static/mainapp/images/pauseButton.png");
}

function setCurrentTime(seconds) { //установка таймера на текущее время
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