$(document).ready(function() {
	args = {'apikey'  : '191d24f81e61c107bca103f7d6a9ca10',
	        'dbfrom'  : 'pubmed', 
	        'id'      : '11812492,11774222',
	        'db'      : 'pubmed',
	        'mindate' : '1995',
	        'datetype': 'pdat',
	        'max'     : '5'}
	        
	$.getJSON('http://{{ host }}/elink+esummary?callback=?', args, function(data) {
		$('#result').html('');
		$.each(data.result, function(i, item) {
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