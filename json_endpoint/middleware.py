from views import dump_result

from django.http import HttpResponseServerError

class ErrorHandlingMiddleware(object):
	def process_exception(self, request, exception):
		response = HttpResponseServerError(mimetype="application/json")
		error = {'entrezajax' : {'error' : True, 'error_message' : str(exception)}}
		dump_result(request, response, [], error)
		return response
		
		
		