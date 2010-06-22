from views import dump_result

from django.http import HttpResponse

class ErrorHandlingMiddleware(object):
	def process_exception(self, request, exception):
		response = HttpResponse(mimetype="application/json")
		error = {'error' : True, 'error_message' : str(exception)}
		dump_result(request, response, [], error)
		return response
		
		
		