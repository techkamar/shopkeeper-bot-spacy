import string 
import random 

sentence_list=["how much for <item>?"
,"what is the price of <item>?"
,"how much do <item> cost?"
,"price of <item>?"
,"give me 5 kg of <item>."
,"I need 1 packet of <item>."
,"give 5 kilograms of <item>"
,"I need 7.5 kilograms of <item>"
,"give me kg 5 of <item>."
,"I need packet 2 of <item>."
,"give kilograms 6.25 of <item>"
,"I need kilograms 7.5 of <item>"]

def get_random_string():
	N = random.randint(5,12)  
	res = ''.join(random.choices(string.ascii_uppercase +
                             	string.ascii_lowercase, k = N))
	return res

def main():
	for sentence in sentence_list:
		for i in range(0,10):
			new_sent = sentence.replace("<item>",get_random_string())
			print(new_sent)

if __name__=="__main__":
	main()