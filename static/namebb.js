var babyNameWordCount = 0;
var babyGender = "both";
var babyXing = "";

var myNewChart;

function getNextName() {
	$.mobile.loading('show', {
		text: "",
		textVisible: false,
		theme: 'z',
		html: ""
	});

	$.getJSON("/name/random", {
		"xing": babyXing,
		"word_count": babyNameWordCount,
		"gender": babyGender
	}, function (json) {

		$("#babyName").empty();


		for (i = 0; i < json.n.length; i++) {
			$("<div>").attr({
				'id' : "babyNameContainer" + i,
				'style' : "float : left;margin: 5px;"

			}).appendTo("#babyName");

			$("<div>").attr({
				'id' : "babyName" + i
			}).appendTo("#babyNameContainer"+i);

			$("<div>").attr({
				'id' : "babyNamePinYin" + i
			}).appendTo("#babyNameContainer"+i);

			$("#babyName" + i).html(json.n[i]);
			$("#babyNamePinYin" + i).html(json.r[i]);
		}

		//score["poem"] = get_poem_score(name)
		//score["wuge"] = get_wu_ge_score(xing, name)
		//score["stroke_count"] = get_stroke_count_score(name)

		//var newData = [json.score.poem,json.score.wuge, json.score.stroke_count];


		$("<div>").attr({
			'style' : "float : right"

		}).appendTo("#babyName");

		myNewChart.datasets[0].points[0].value = json.score.poem;
		myNewChart.datasets[0].points[1].value = json.score.wuge;
		myNewChart.datasets[0].points[2].value = json.score.stroke_count;
		myNewChart.update();

		$.mobile.loading('hide');
	});
}

$(document).ready(function () {

	Chart.defaults.global.animationSteps = 30;

	if(typeof(Storage) !== "undefined") {
		var localBabyXing = localStorage.getItem("xing");
		if(localBabyXing !== null){
			babyXing = localBabyXing;
		}

		var localGender = localStorage.getItem("gender");
		if(localGender != null) {
			babyGender = localGender;
		}
		var localWordCount = localStorage.getItem("wordCount");
		if(localWordCount != null) {
			babyNameWordCount = localWordCount;
		}
	}

	if(babyXing == "") {

		$.mobile.changePage('#settingPage', 'pop', true, true);
	} else {
		$.mobile.changePage('#mainPage', 'pop', true, true);
		getNextName();
	}


	$("#babyXingText").bind('input', function () {
		babyXing = $("#babyXingText").val();
		$("#settingOk").prop("disabled", babyXing == "" ? true : false);
	});
	$("#gender").change(function () {
		babyGender = $("input:radio[name='gender']:checked").val();
	});

	$("#wordCount").change(function () {
		babyNameWordCount = $("input:radio[name='wordCount']:checked").val();
	});

	$("#settingOk").click(function () {
//                $( "#settingPage" ).dialog( "close" );
		if(typeof(Storage) !== "undefined") {
			localStorage.setItem("xing", babyXing);
			localStorage.setItem("gender", babyGender);
			localStorage.setItem("wordCount", babyNameWordCount);
		}

		$.mobile.changePage('#mainPage', 'pop', true, true);
		getNextName();
//                window.location = "#main";
	});

	$("#nextName").click(function () {
		getNextName();
	});
//
//            $("#rank_name_button").click(function () {
//                $.getJSON("/rank", {
//                    name:$("#rank_content").html
//                }, function(json){
//                    $("#rank_score").html(json.score);
//
//                });
//            });

	var ctx = document.getElementById("myChart").getContext("2d");

	var data = {
		labels: ["文化", "笔划", "五格"],
		datasets: [
			{
				label: "My First dataset",
				fillColor: "rgba(220,220,220,0.2)",
				strokeColor: "rgba(220,220,220,1)",
				pointColor: "rgba(220,220,220,1)",
				pointStrokeColor: "#fff",
				pointHighlightFill: "#fff",
				pointHighlightStroke: "rgba(220,220,220,1)",
				data: [0, 0, 0]
			}
//                    {
//                        label: "My Second dataset",
//                        fillColor: "rgba(151,187,205,0.2)",
//                        strokeColor: "rgba(151,187,205,1)",
//                        pointColor: "rgba(151,187,205,1)",
//                        pointStrokeColor: "#fff",
//                        pointHighlightFill: "#fff",
//                        pointHighlightStroke: "rgba(151,187,205,1)",
//                        data: [28, 48, 40, 19, 96, 27, 100]
//                    }
		]
	};
	myNewChart = new Chart(ctx).Radar(data);
});

$(document).bind('mobileinit', function () {
//            $.mobile.loader.prototype.options.text = "";
//            $.mobile.loader.prototype.options.textVisible = false;
//            $.mobile.loader.prototype.options.theme = "";
//            $.mobile.loader.prototype.options.html = "";
});