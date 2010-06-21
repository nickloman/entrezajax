var search_term = "{{ term|escapejs }}";

$(document).ready(function() {
	args = {'apikey' : '191d24f81e61c107bca103f7d6a9ca10',
	        'db' : 'protein',
	        'term' : search_term};
	$.getJSON('/esearch+efetch?callback=?', args, function(data) {
		var result = '';
		records = data.result;
		for(var i = 0; i < records.length; i++) {
			result += "<p>&gt; "
			       + records[i].GBSeq_locus
			       + "<textarea cols=\"60\" rows=\"5\">"
			       + records[i].GBSeq_sequence
			       + "</textarea></p>"
	
			$('#result').html(result);
		}
	});
});