import spacy
import random
import spacy.cli
import json


class SpacyNERTrainer:
    def __init__(self, config_file):
        self.config_file = config_file
        self.configs = {}
        self.ner_labels = set()
        self.init_config()

    def init_config(self):
        with open(self.config_file) as inf:
            for line in inf:
                line = line.strip()
                key_value = line.split("=")
                self.configs[key_value[0]] = key_value[1]

    def get_input_sentences_json(self):
        file_content = ""
        inp_file_name = self.configs["TRAINING_DATA_JSON_FILE"]
        with open(inp_file_name) as inf:
            for line in inf:
                line = line.strip()
                if line != "":
                    file_content += line
        return json.loads(file_content)

    def train(self):
        # Load Training data as JSON from input file
        input_json = self.get_input_sentences_json()

        # Convert JSON to Spacy input format
        training_data = self.convert_json_to_spacy(input_json)


#SPECIFY THE NER TRAINING DATA
TRAIN_DATA = [("How many kilograms Almonds can be bought for $50.5?",{"entities":[(0,8,"action"),(9,18,"unit"),(19,26,"item"),(45,50,"price")]}),
("How many kg Mangoes can be bought for $500?",{"entities":[(0,8,"action"),(9,11,"unit"),(12,19,"item"),(38,42,"price")]}),
("Cost of Almonds per kg?",{"entities":[(0,4,"action"),(8,15,"item"),(20,22,"unit")]}),
("How much for a packet of milk?",{"entities":[(0,8,"action"),(15,21,"unit"),(25,29,"item")]}),
("show me items which cost between $500 and $1000.",{"entities":[(8,13,"item"),(0,4,"action"),(25,32,"comparison"),(33,37,"price"),(42,47,"price")]}),
("show me items under $500.",{"entities":[(20,24,"price"),(8,13,"item"),(14,19,"comparison"),(0,4,"action")]}),
("list all the items.",{"entities":[(13,18,"item"),(0,4,"action")]}),
("show me all items you have.",{"entities":[(0,7,"action"),(12,17,"item")]})]

nlp = spacy.blank('en')
ner = nlp.create_pipe("ner")

nlp.add_pipe(ner, last=True)

#ADD THE CUSTOM NAMED ENTITIES HERE
nlp.entity.add_label('action')
nlp.entity.add_label('amount')
nlp.entity.add_label('price')
nlp.entity.add_label('comparison')
nlp.entity.add_label('unit')
nlp.entity.add_label('item')


nlp.vocab.vectors.name = 'spacy_pretrained_vectors'
optimizer = nlp.begin_training()
for i in range(20):
    random.shuffle(TRAIN_DATA)
    for text, annotations in TRAIN_DATA:
        nlp.update([text], [annotations], sgd=optimizer)
#SAVE THE CUSTOM NER MODEL TO GOOGLE DRIVE
nlp.to_disk("/home/syed/Documents/nlp/model")
print("Model saved to Model folder")