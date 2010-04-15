
from django.shortcuts import render_to_response
from django.http import HttpResponse
from google.appengine.api.memcache import Client

def frontpage(request):
	return render_to_response('index.html')
	
def memcache(request):
	return HttpResponse(str(Client().get_stats()))