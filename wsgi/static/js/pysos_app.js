$(document).ready(function() {

	// variable for new row
	var editRow = "<tr class=\"danger\"><td>Test for edit row</td></tr>";

	// insert hidden row after each visible row
	$("tbody").children().filter("tr").each(function() {
		$(this).after(editRow);
		console.log("Added new hidden row")
	});

	// hide all new rows
	$(".danger").each(function() {
		$(this).hide();
		console.log("Hiding edit row");
	});

	$(".editRow").click(function() {
		console.log("User clicked on cog");
		
		// should store the row this came from for reference
		var curRow = $(this).parents().filter("tr");
		console.log("Set curRow");		

		// find edit row for curRow
		var nextRow = curRow.next(".danger");
		console.log("Found edit row");

		// slide down edit row
		nextRow.slideDown();
		
	});
});
