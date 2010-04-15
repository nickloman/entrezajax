
from django.shortcuts import render_to_response
from forms import DeveloperRegistrationForm

def register(request):
	if request.POST:
		form = DeveloperRegistrationForm(request.POST)
		if form.is_valid():
			reg = form.save()
			return render_to_response('registration-successful.html', {'reg' : reg.key().name()})
	else:
		form = DeveloperRegistrationForm()	
	return render_to_response('register.html', {'form': form})
	
	