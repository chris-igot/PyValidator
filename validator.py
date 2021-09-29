from typing import Union,Callable
import re
function_type = type(lambda x:x)

class Validator:
	def __init__(self,check:dict):
		self.check:dict = check
	@classmethod
	def validate(cls,data,validation_matrix:dict,err_func=print,strict=True,strong_type=True) -> bool:
		valid:bool = True

		data_type:type
		ch: Union[str,function_type]
		err:Union[str,list[str]]

		try:
			data_type = validation_matrix["type"]
			ch = validation_matrix["validations"]
		except KeyError as e:
			err_func("type and/or check keys do not exist in validation matrix","general_error")
			raise e

		if strong_type:
			if not cls.__verify_type__(data,data_type):
				valid = False
		else:
			type_casted_data = None

			try:
				type_casted_data = cls.__verify_type__(data_type(data),data_type)
			except ValueError as e:
				err_func("Unable to type cast data","general_error")
				raise e

			if not type_casted_data:
				valid = False
			else:
				data = type_casted_data

		print("\nDATA1",data,valid,type(ch),"\n",validation_matrix)

		if not valid:
			return valid

		print("DATA2",data,valid,type(ch),"\n",validation_matrix)

		if type(ch) == list:
			print("DATA3 - list",data,valid,type(ch),"\n",validation_matrix)
			for sub_ch in ch:
				if not cls.__validate__(data,sub_ch,err_func):
					valid = False
		else:
			if not cls.__validate__(data,ch,err_func):
				valid = False
		
		if not valid:
			return valid

		print("DATA4",data,valid,type(ch),"\n",validation_matrix)

		if "content" in validation_matrix:
			content = validation_matrix["content"]
			if data_type == dict and type(content) == dict:
				sub_content_valid: bool = True
				for key, sub_validation_matrix in content.items():
					if not cls.validate(data[key],sub_validation_matrix,strict,strong_type):
						sub_content_valid = False
				if not sub_validation_matrix:
					valid = False
			# elif data_type == list and type(content) == list:
			# 	sub_content_valid: bool = True
			# 	for t in content:
			# 		if strong_type:
			# 			pass
		
		return valid
	
	@classmethod
	def __validate__(cls,data,ch:dict,err_func) -> bool:
		valid = True
		if type(ch) == str:
			regex:re
			try:
				regex = re.compile(ch)
			except re.error as e:
				err_func("Invalid regex","general_error")
				raise e

			if not regex.match(data):
				valid = False
		elif type(ch) == function_type:
			if not ch(data):
				valid = False
		return valid

	@classmethod
	def __verify_type__(cls,data,data_type,err_func):
		if type(data) == data_type:
			return data
		else:
			err_func("Data does not match type in validation", "general_error")
			return False

print(type(function_type))