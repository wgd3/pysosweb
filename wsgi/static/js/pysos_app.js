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
			window.location.href = '/delete/'+packageName
		} else {
			console.log("User has chosen not to confirm deletion")
			// leave edit row open for more edits
		}
	});

	// add listener to all checkmark glyphs
	$(".glyphicon-ok").click(function() {
		console.log("User clicked on OK glyph");

		// get current row
		var curRow = $(".editing");
		
		// get the row that has the new data in it
		// row with input fields always has the 'warning' class used by bootstrap for background coloring
		var newRow = $(this).parents().filter(".warning");

		// get all input boxes, see if they have data
		var newData = new Array();
		var newData = newRow.find("input").each(function() {
			console.log("Looking for text input: " + $(this).val());
			var tempText = $(this).val();
			newData.push(tempText);
			for (i=0;i<newData.length;i++) {
				console.log(newData[i])
			}	
		});

		// find the package name on the original row
		// necessary because even if we're updating the name, we need to look up the record by it's current name
		var origName = curRow.children().eq(1).text();
		console.log("Found original package name to be: " + origName);		

	
		console.log("newData has the following length: " + newData.length);

		// cycle through input boxes looking for new text
		var updatedData = false;
		var newName = false;
		var newVersion = false;
		var newWarning = false;

		for (i=0;i<newData.length;i++)
			{
			console.log("Entering loop with index: " + i);
			var newText = newData[i];
			console.log("Evaluating new text: " + newText.value);
			if (newText.value != '')
				{
				updatedData = true;
				switch(i)
					{
					case 0:
						console.log("Found new package name: " + newText.value);
						newName = true;
						break;
					case 1:
						console.log("Found new package version: " + newText.value);		
						newVersion = true;
						break;
					case 2:
						console.log("Found new package warning: " + newText.value);
						newWarning = true;
					}
			}
			}


		// if there's new data, do something with it
		if (updatedData) {
			console.log("Hey, there's updated data here. Do something with it!")
			// maybe use a /update page?
			var url_string = '/update/'+origName+'/'
			if (newName) {
				url_string = url_string + newData[0].value+'/'
				console.log("updating update url: "+url_string)
			} else {
				url_string = url_string + 'null/'
			}
			if (newVersion) {
				url_string = url_string + newData[1].value+'/'
				console.log("updating update url: "+url_string)
			} else {
				url_string = url_string + 'null/'
			}
			if (newWarning) {
				url_string = url_string + newData[2].value
				console.log("updating update url: "+url_string)
			} else {
				url_string = url_string + 'null'
			}
			window.location.href = url_string
		} else {
			console.log("User clicked check mark glyph with no new data in boxes, closing edit row");
			// close the editing row - same action as if pencil glyph is clicked
			newRow.toggle();
			curRow.removeClass("editing")
		}

	});
});
