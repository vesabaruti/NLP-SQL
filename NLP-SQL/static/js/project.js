//alert("Working");
$(document).ready(function() {
            //option A
        $("#queryForm").submit(function(e){
		e.preventDefault(e);
		$( "#queryResult" ).empty();
		var form = $('#queryForm');
		var formData = form.serialize();
		$.ajax({
		type:"POST",
		data:formData,
    		url : "submitQuery",
	        success: function(result) {
				console.log(result);
				$(result).appendTo('#queryResult');
	        	}
	        });
            });

    $('#Database').hide();


	$("#toggleDatabase").click(function () {
		if ($('#Database').is(':visible')) {
			$('#Database').hide();
			return
		}
	   	if ($('#Database').is(':hidden')) {
	   		$('#Database').show();
			$( "#showStudentDetails" ).empty();
			$( "#showDepartmentDetails" ).empty();
			$.ajax({
				type:"POST",
				data:{},
				url : "showStudentDetails",
				success: function(result) {
					console.log(result);
					$(result).appendTo('#showStudentDetails');
				}
			});
			$.ajax({
				type:"POST",
				data:{},
				url : "showDepartmentDetails",
				success: function(result) {
					console.log(result);
					$(result).appendTo('#showDepartmentDetails');
				}
			 });
	   }
	});

	$('#toggleTree').click(function () {
		$('.tree-image').toggle();
	})
});
