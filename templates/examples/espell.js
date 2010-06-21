var search_term = "{{ term|escapejs }}";

$(document).ready(function() {
	args = {'apikey' : '191d24f81e61c107bca103f7d6a9ca10',
	        'db' : 'pubmed',
	        'term' : search_term};
	$.getJSON('/espell?callback=?', args, function(data) {
		if(data.result.CorrectedQuery.length) {
			var result = data.result.Query + " should be spelt " + data.result.CorrectedQuery;
		} else {
			var result = data.result.Query + " is spelt correctly or no spelling suggestions could be made";
		}
		$('#result').html(result);
	});
});