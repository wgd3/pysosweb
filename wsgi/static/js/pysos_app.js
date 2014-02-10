$(document).ready(function() {

	// variable for new row
	var editRow = "<tr class=\"danger\"><td><span class=\"glyphicon glyphicon-ok col-md-6\"></span><span class=\"glyphicon glyphicon-remove col-md-6\"></span></td></tr>";

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

	$(".glyphicon-pencil").click(function() {
		console.log("User clicked on glyph");
		
		// should store the row this came from for reference
		var curRow = $(this).parents().filter("tr");
		console.log("Set curRow");		

		// set background color to indicate edit mode
		// add new class just in case we need it to identify the row later
		curRow.addClass("editing");
		curRow.css("background-color","yellow");

		// find edit row for curRow
		var nextRow = curRow.next(".danger");
		console.log("Found edit row");

		// slide down edit row
		//nextRow.slideToggle();
		
	});
});
