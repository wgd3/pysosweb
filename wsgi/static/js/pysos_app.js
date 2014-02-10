$(document).ready(function() {

	// hide all edit rows
	$(".editRow").each(function() {
		$(this).hide();
		console.log("Hiding edit rows");
	});

	$(".glyphicon-pencil").click(function() {
		console.log("User clicked on glyph");
		
		// should store the row this came from for reference
		var curRow = $(this).parents().filter("tr");
		console.log("Set curRow");		

		// first hide any rows that currently have 'editing' class. row should only have this if open
		$(".editing").toggle();
		console.log("Should be hiding any open rows");

		// remove 'editing' class from all rows since they should all be closed at this point
		$(".editing").removeClass(".editing");
		console.log("removing editing class from whatever rows have it");

		// find edit row for curRow
		var nextRow = curRow.next(".editRow");
		console.log("Found edit row");

		// slide down edit row
		nextRow.toggle();
		console.log("showing edit row");

		// add 'editing' class since this row will now be visible
		curRow.addClass("editing");
		console.log("added editing class to current open edit row");

	});
});
