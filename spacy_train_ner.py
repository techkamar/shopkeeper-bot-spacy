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

    def convert_json_to_spacy(self,input_json_list):
        sentence_train_list = []
        for inp_json in input_json_list:
            text = inp_json["text"]
            entities_list = []
            for entity in inp_json["entities"]:
                start = entity['start']
                end = entity['end']
                label = entity['label']
                self.ner_labels.add(label)
                entities_list.append((start,end,label))
            sentence_train_list.append((text,{"entities":entities_list}))
        return sentence_train_list

    def train(self):
        # Load Training data as JSON from input file
        input_json = self.get_input_sentences_json()

        # Convert JSON to Spacy input format
        training_data = self.convert_json_to_spacy(input_json)
        print("=================== Training Data ===================")
        print(training_data)

        # As modle language. If its based on english then 'en'
        nlp = spacy.blank(self.configs["MODEL_LANGUAGE"])
        ner = nlp.create_pipe("ner")

        nlp.add_pipe(ner, last=True)

        # Add all the labels found in training file
        for label in self.ner_labels:
            nlp.entity.add_label(label)

        # Set Vocab Vector name
        nlp.vocab.vectors.name = self.configs["VECTOR_VOCAB_NAME"]
        optimizer = nlp.begin_training()
        no_of_iterations = int(self.configs["NO_OF_ITERATIONS"])

        print("\n\n=================== NER Training In Progress ===================")
        print("No of iterations : "+str(no_of_iterations))
        for i in range(no_of_iterations):
            print("Performing ("+str(i+1)+"/"+str(no_of_iterations)+") iteration...")
            random.shuffle(training_data)
            for text, annotations in training_data:
                nlp.update([text], [annotations], sgd=optimizer)

        # Save Custom model to output model path
        print("Saving model to path : "+str(self.configs["MODEL_OUTPUT_PATH"]))
        nlp.to_disk(self.configs["MODEL_OUTPUT_PATH"])


if __name__ == "__main__":
    ner = SpacyNERTrainer("app.config")
    ner.train()
