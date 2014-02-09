$(document).ready(function() {

// set mouseover function for each element in the list.html table
	$(".row-config").parent().mouseover(function() {
		
		$(this).children().first().html("<span class="glyphicon glyphicon-cog"></span>");
	});
});
