$(document).ready(function() {

	// hide all edit rows
	$(".editRow").each(function() {
		$(this).hide();
		console.log("Hiding edit rows");
	});

	// prefill the edit fields placeholders
	$("tbody").children("tr").each(function() {
		var dataRow = $(this);
		var dataFields = dataRow.children
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

	// add listeners to all 'X' glyphs for deletion
	$(".glyphicon-remove").click(function() {
		console.log("User clicked on remove glyph, attempting deletion");

		// get current row - should coincide with the row currently labelled "editing" since that
		// is activated when the editRow appears
		var curRow = $(".editing")

		// find package name in second column (children() returns all td elements)
		var packageName = curRow.children().eq(1).text()
		console.log("User is trying to delete package " + packageName);

		// prompt user for confirmation
		if (confirm('Are you sure you want to delete the package ' + packageName)) {
			console.log("User has confirmed deletion")

			// go ahead and attempt to remove from the database
		} else {
			console.log("User has chosen not to confirm deletion")
			// do nothing
		}
	});
});
