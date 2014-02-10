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

		// check to see if open row was clicked to close
		if (curRow.hasClass("editing"))
			{
			curRow.next(".editRow").toggle();
			curRow.removeClass("editing");
			console.log("Detected that we are closing the currently open row");
			}
		else // current row isn't the row being currently edited
			{
			$(".editing").next(".editRow").toggle();
	
			$(".editing").removeClass("editing");

			var nextRow = curRow.next(".editRow");

			curRow.addClass("editing");

			nextRow.toggle()
			}

	});
});
