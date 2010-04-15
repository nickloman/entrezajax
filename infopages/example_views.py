
from django.shortcuts import render_to_response

def example_with_term(request, template, default):
	return render_to_response(template, {'term' : request.GET.get('term', default)})
	