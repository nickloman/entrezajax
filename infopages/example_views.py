
from django.shortcuts import render_to_response

def example(request, template):
	return render_to_response(template, {'host' : request.META.get('HTTP_HOST', '')})
		

def example_with_term(request, template, default):
	return render_to_response(template, {
	             'host' : request.META.get('HTTP_HOST', ''),
	             'term' : request.GET.get('term', default)
	             })
	