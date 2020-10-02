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

		# Add main json for final output storage
		self.final_json = {}

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

	def get_all_indices_of_label_in_sentence(self,main_str, sub_str):
		index_list = []
		while True:
			try:
				start = main_str.index(sub_str)
				end = start + len(sub_str)

				# Previously data exists
				if len(index_list) > 0:
					# Find last item
					start_end = index_list[len(index_list) - 1]

					start += start_end['end']
					end += start

				main_str = main_str[end + 1:]
				index_list.append({'start': start, 'end': end, 'label': sub_str})

			except:
				break
		return index_list

	def make_training_json(self, sentence):
		index_list = []
		for label in self.label_config_json.keys():
			tmp_index_list = self.get_all_indices_of_label_in_sentence(sentence, "<" + label + ">")
			for index in tmp_index_list:
				index_list.append(index)

		print(index_list)

	def generate(self):
		for sentence in self.input_patterns_list:
			self.make_training_json(sentence)


# MAIN METHOD or ENTRY point
def main():
	generator = SentenceGenerator()
	generator.generate()


if __name__ == "__main__":
	main()
