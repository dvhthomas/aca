$(document).ready(function() {
	$('.photo input[type=checkbox]').click(function() {
		var thisCheck = $(this);
		var inshow = thisCheck.is(':checked') ? true : false;

		$.ajax({
			type: 'PUT',
			url: '/photo/' + event.target.name,
			contentType: 'application/json',
			data: JSON.stringify({ in_show: inshow })
			});

		//$(event.target).parent().remove();
		//event.preventDefault();
	});

	$('#add_file').click(function () {
		$file = $('#add_file');
		$('<input type="file" name="file"><br/>').insertBefore('#add_file');
		event.preventDefault();
	});
});

