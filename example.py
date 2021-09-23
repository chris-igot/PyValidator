from validator import validate

checks = {
	"email":[																	#Key that will correspond to another key in a dict that needs to be checked
		{																				#First check in an array of dicts for "email" key
			'lambda': lambda x: type(x) == str,		#Lambda function to check the field. Generates an error on return False
			'error': "Field must be a string",		#Error to be generated. Passed to a function given in validate(). Defaults to print
			'category': "email_field_error",			#Category for error above. Passed to the same function. Works when func=flash when used with Flask
			'showstopper': True,									#Stops any further checks for this field. Should be first for highest priority. Use for type checks
		},
		{
			'regex': r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]+$",
			'error': "Please enter valid email address",
			'category': "email_field_error",
		},
	]
}

form_data1 = {
	'email': 1,
}

validate(form_data1,checks)

form_data2 = {
	'email': "nonemail",
}

validate(form_data2,checks)

form_data3 = {
	'email': "name@domain.com",
}

validate(form_data3,checks)