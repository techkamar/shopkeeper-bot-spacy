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
			# exit(0)

		try:
			str(sys.argv[2])
		except:
			print("ERROR!!! Input JSON File not specified")
			# exit(0)

		try:
			str(sys.argv[3])
		except:
			print("ERROR!!! Output File not specified")
			# exit(0)

		# Read the input file
		# self.input_patterns_list = self.get_content_of_file(sys.argv[1])
		self.input_patterns_list = ["list all the <items> of <man> of my <items>"]

		# Get the config to generate the sentences for labels
		# self.label_config_json = json.loads(self.get_content_of_file(sys.argv[2]))
		self.label_config_json = {"items": "COWWWW", "man": "PHEWWWWW"}

		# Add main json for final output storage
		self.final_json = []

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
					end = start + len(sub_str)

				main_str = main_str[end + 1:]
				index_list.append({'start': start, 'end': end+1, 'label': sub_str})

			except:
				break
		return index_list

	def replace_labels_with_values(self, sentence, index_list):
		if len(index_list) == 0:
			return None

		for index in range(0, len(index_list)):
			item_at_index = index_list[index]
			label = item_at_index["label"]
			label = label[1:len(label)-1]
			replaced_word = self.label_config_json[label]
			item_at_index['replaced_word'] = replaced_word
			existing_word_length = item_at_index['end']-item_at_index['start']
			additional_char_length = len(replaced_word)-existing_word_length+1
			item_at_index['additional_char_length'] = additional_char_length

			if index > 0:
				item_at_index['start'] = item_at_index['start'] + index_list[index-1]['additional_char_length']
			item_at_index['end'] = item_at_index['start'] + len(replaced_word) +1

			index_list[index] = item_at_index

		for element in index_list:
			sentence = sentence[:element['start']] + element['replaced_word'] + sentence[element['end']+1:]
		return None

	def get_sorted_index_list(self, index_list):
		new_index_list = []
		start_index_map = {}
		for item in index_list:
			start_index_map[item['start']] = item

		start_index_list = list(start_index_map.keys())
		start_index_list.sort()
		for start_index in start_index_list:
			new_index_list.append(start_index_map[start_index])

		return new_index_list

	def make_training_json(self, sentence):
		index_list = []
		for label in self.label_config_json.keys():
			tmp_index_list = self.get_all_indices_of_label_in_sentence(sentence, "<" + label + ">")
			for index in tmp_index_list:
				index_list.append(index)

		index_list = self.get_sorted_index_list(index_list)

		single_entry_json = self.replace_labels_with_values(sentence,index_list)
		if single_entry_json is not None:
			self.final_json.append(single_entry_json)

	def generate(self):
		for sentence in self.input_patterns_list:
			self.make_training_json(sentence)


# MAIN METHOD or ENTRY point
def main():
	generator = SentenceGenerator()
	generator.generate()


if __name__ == "__main__":
	main()
