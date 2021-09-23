import re

def validate(form_data,checks,form_name="form",strict=True,func=print):
	valid = True
	for key, val in checks.items():
		if key in form_data:
			for check in val:
				if "lambda" in check:
					if not check["lambda"](form_data[key]):
						valid = False
						func(check["error"],check["category"])
						if "showstopper" in check and check["showstopper"]:
							break
				if type(form_data[key]) == str and "regex" in check:
					regex = re.compile(check["regex"])
					if not regex.match(form_data[key]):
						valid = False
						func(check["error"],check["category"])
						if "showstopper" in check and check["showstopper"]:
							break
					
		elif strict and key not in form_data:
			valid = False
			func(f"Field {key} not submitted",form_name+"_messages")
	
	return valid
