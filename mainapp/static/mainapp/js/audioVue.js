var track = {
    filesDir: "/static/mainapp/",
    trackID: {
        current: null,
        next: null
    },
    isLiked: false
};

var playButton = new Vue({
    el: '#playButton',
    name: 'playButton',
    data: {
    picSource: track.filesDir + "images/playButton.png"
    },
    methods: {
        click: function () {
            if(document.getElementById("audio").paused)
            {
                $("#audio").trigger('play');
                this.picSource = track.filesDir + "images/pauseButton.png";
            }
            else
            {
                $("#audio").trigger('pause');
                this.picSource = track.filesDir + "images/playButton.png";
            }
        }
    }
});

var nextButton = new Vue({
    el: '#nextButton',
    name: 'nextButton',
    methods: {
        click: nextTrack
    }
});

var mainLogo = new Vue({
    el: '#mainLogo',
    name: 'mainLogo',
    data: {
        showLike: false,
        logoSource: ''
    },
    methods: {
        mouseenter: function () {
            if (!track.isLiked)
                this.showLike = true;
        },
        mouseleave: function () {
            if (!track.isLiked)
                this.showLike = false;
        },
        click: function() {
            var varData = {
                option: "",
		    	current_track: track.trackID.current
		    };
            varData.option = (track.isLiked) ? "remove" : "add";
            sendJSON('like/', JSON.stringify(varData), successfulLikeFunc);
        }
    }
});

var trackPerformerName = new Vue({
    el: '#trackPerformerName',
    name: 'trackPerformerName',
    data: {
        trackName: '',
        performerName: ''
    },
    template: '<div id="trackPerformerName"><p id="trackname">{{ trackName }}</p><p id="performername">{{ performerName }}</p></div>'
});


var elemOpen = '<p class="menuElements">';
var elemClose = '</p>';

function makeDropElem(text)
{
    return elemOpen + text + elemClose;
}

var menu = new Vue({
    el: '#menu',
    name: 'menu',
    data: {
        showDropdown: false,
        menuElements: [makeDropElem('На страницу исполнителя'), makeDropElem('Добавить в избранное'), makeDropElem('Пожаловаться')]
    },
    methods: {
        click: function() {
            this.showDropdown = !this.showDropdown;
        }
    }
});

var speaker = new Vue({
    el: '#speaker',
    name: 'speaker',
    methods: {
        mouseenter: function() {
            volume.$data.show = !volume.$data.show;
        }
    }
});

var volume = new Vue({
    el: '#volume',
    name: 'volume',
    data: {
        show: false
    },
    methods: {
        mouseleave: function() {
            this.show = false;
        }
    }
});

function successfulLikeFunc(data)
{
    if(data.result === "added")
    {
        track.isLiked = true;
        mainLogo.$data.showLike = true;
	}
	else if(data.result === "removed")
	{
        track.isLiked = false;
        mainLogo.$data.showLike = false;
	}
}

nextTrack();

function nextTrack(){
    mainLogo.$data.showLike = false;
	var varData = {
		current_track: track.trackID.current,
		next_track: track.trackID.next
	};
	var jsonData = JSON.stringify(varData);
	sendJSON('next/', jsonData, nextTrackSuccessFunc);
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
}

function nextTrackSuccessFunc(data) {         //функция успеха после получения следующего трека
    //timeColorChanger();
    trackPerformerName.$data.trackName = data.track_name;
    trackPerformerName.$data.performerName = data.performer_name;

	$("#audio").attr("src", data.file_link);
	track.trackID.current = data.current_id;
	track.trackID.next = data.next_id;
	$("#progressBarLine").animate({width: 0 + "%"}, 50);
	$("title").text(data.track_name);

	logo = mainLogo.$data.logoSource;
	mainLogo.$data.logoSource = data.logo_link;

	$("#prevlogo").attr("src", logo);
	$("#nextlogo").attr("src", data.nextlogo_link);

	track.isLiked = !!(data.is_liked);
	mainLogo.$data.showLike = track.isLiked;
}

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

