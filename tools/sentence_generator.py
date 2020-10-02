import string 
import random
import sys
import json


class SentenceGenerator:
	def __init__(self):
		try:
			str(sys.argv[1])
		except:
			print("ERROR!!! Input Text File not specified")
			exit(0)

		try:
			str(sys.argv[2])
		except:
			print("ERROR!!! Input JSON File not specified")
			exit(0)

		try:
			str(sys.argv[3])
		except:
			print("ERROR!!! Output File not specified")
			exit(0)

		# Read the input file
		self.input_patterns_list = self.get_content_of_file(sys.argv[1])

		# Get the config to generate the sentences for labels
		self.label_config_json = json.loads(self.get_content_of_file(sys.argv[2]))

	def get_content_of_file(self,file_name):
		content = ""
		with open(file_name) as inp:
			for line in inp:
				line = line.strip()
				content += line
		return content

	def get_random_string(self, min_length, max_length):
		length = random.randint(min_length, max_length)
		res = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k = length))
		return res


	def generate(self):
		pass


# MAIN METHOD or ENTRY point
def main():
	generator = SentenceGenerator()
	generator.generate()


if __name__=="__main__":
	main()