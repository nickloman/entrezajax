from django import forms
from models import DeveloperRegistration
from datetime import datetime
import logging
import md5

class DeveloperRegistrationForm(forms.Form):
	contact_name = forms.CharField(initial='Your name')
	website_url = forms.URLField(label='Your website')
	email = forms.EmailField(max_length=255)
	tool_id = forms.CharField(max_length=40)
	
	def clean_tool_id(self):
		tool_id = self.cleaned_data['tool_id']
		q = DeveloperRegistration.all().filter("tool_id =", tool_id)
		if q.get():
			raise forms.ValidationError("A tool with this name has already been registered!")
		return tool_id

	def save(self):
		tool_id = self.cleaned_data['tool_id']
		reg = DeveloperRegistration(
				key_name = md5.new(str(tool_id)).hexdigest(),
				contact_name = self.cleaned_data['contact_name'],
				website_url = self.cleaned_data['website_url'],
				email = self.cleaned_data['email'],
				tool_id = tool_id,
				created_on = datetime.now()
		)
		reg.put()
		
		return reg
		
		
		
		
	

    