$(document).ready(function() {
	$('input[name=title]').focus();

	$year = $('input[name=created]').val();

	if ($year === '') {
		$('input[name=created]').val(new Date().getFullYear());
	}

	$('.delete_picture').click(function() {
		$.ajax({
			'type': 'DELETE',
			'url': '/photo/' + event.target.id
			})
		$(event.target).parent().remove();
		event.preventDefault();
	});

	$('#add_file').click(function () {
		$file = $('#add_file');
		$('<input type="file" name="file"><br/>').insertBefore('#add_file');
		event.preventDefault();
	});
});

