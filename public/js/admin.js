$(document).ready(function () {
	var golden = 1.61;

	$('#width').keyup(function () {
		var answer = parseInt($(this).val()) / golden;
		$('#height-answer').text(isNaN(answer) ? '-' : app.round(answer,0));
	});
	$('#height').keyup(function () {
		var answer = parseInt($(this).val()) * golden;
		$('#width-answer').text(isNaN(answer) ? '-' : app.round(answer,0));
	});
});
