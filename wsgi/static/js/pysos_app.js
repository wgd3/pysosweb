$(document).ready(function() {

	// variable for new row
	var editRow = "<tr class=\"danger\"><td>Test for edit row</td></tr>";

	// insert hidden row after each visible row
	$("tbody").children().filter("tr").each(function() {
		$(this).after(editRow)
	});

	// hide all new rows
	$(".danger").each(function() {
		$(this).hide()
	});

	$(".row-config").each().children().click(function() {
		// should store the row this came from for reference
		var curRow = $(this).parent();
		
		// slide down editRow
		curRow.slideDown()
	});
});
