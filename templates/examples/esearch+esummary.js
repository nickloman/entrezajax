var search_term = "{{ term|escapejs }}";

$(document).ready(function() {
	args = {'apikey' : '191d24f81e61c107bca103f7d6a9ca10',
	        'db' : 'pubmed',
	        'term' : search_term};
	$.getJSON('/esearch+esummary?callback=?', args,	function(data) {
		$('#result').html('');
		$.each(data, function(i, item) {
			var author_list = '';
			for(var i = 0; i < item.AuthorList.length; i ++) {
				if(i != 0) {
					author_list += ', ';
				}
				author_list += item.AuthorList[i];
			}
			var html = '<p><a href=\'http://www.ncbi.nlm.nih.gov/pubmed/' + item.ArticleIds.pubmed + '\'>' + item.Title + '</a><br/>' + author_list + '<br/>' + item.FullJournalName + ' ' + item.PubDate + '</p>';
			$("<div/>").html(html).appendTo('#result');
		});
	});
});
