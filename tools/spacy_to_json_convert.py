import sys
import json

"""
    Usage : python spacy_to_json_convert.py data.list data.json
"""

def get_content_from_file(inp_file):
    content = ""
    with open(inp_file) as inf:
        for line in inf:
            line = line.strip()
            content += line
    return content


def get_entities_json(entity):
    entity_json = {}
    entity_tokens = entity.split(",\"")
    tag = entity_tokens[1]

    # Remove " at the end
    tag = tag[:len(tag)-1]

    indices_list = entity_tokens[0].split(",")
    entity_json["start"] = int(indices_list[0])
    entity_json["end"] = int(indices_list[1])
    entity_json["label"] = tag
    return entity_json


def get_entities_json_list(entities):
    entities_list = []
    entities_tokens = entities.split(")")
    for token in entities_tokens:
        if token != "":
            # Check for comman in begining
            if token[0] == ",":
                token = token[2:]
            else:
                token = token[1:]
            entities_list.append(get_entities_json(token))
    return entities_list


def get_each_sentence_json(sentence):
    sentence = sentence[2:]
    if sentence == "":
        return None
    sentence_split = sentence.split(",{\"entities\":[")
    text = sentence_split[0]
    entities = sentence_split[1]

    required_json = {'text': text[1:len(text) - 1], 'entities': get_entities_json_list(entities)}

    return required_json


def main():
    try:
        str(sys.argv[1])
    except:
        print("ERROR!!! Input File not specified")
        exit(0)

    try:
        str(sys.argv[2])
    except:
        print("ERROR!!! Output File not specified")
        exit(0)

    inp_file = str(sys.argv[1])
    oup_file = str(sys.argv[2])
    content = get_content_from_file(inp_file)
    sentence_list = content.split("]})")
    final_json = []
    for sentence in sentence_list:
        sentence_json = get_each_sentence_json(sentence)
        if sentence_json is not None:
            final_json.append(sentence_json)

    oup = open(oup_file, "w")
    oup.write(json.dumps(final_json))
    oup.close()


if __name__ == "__main__":
    main()
