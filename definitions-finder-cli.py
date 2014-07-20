from wordnik import *
import thread

def read_words(list):
	list_replace = list.replace("\n", "")
	list_split = list_replace.split(",")
	return list_split

files = open("test.txt", "r")
words = files.read()

api_url = 'http://api.wordnik.com/v4'
api_key = "b44d5b197c73203bf30040df7ec02ee0c179bbf699b5ca39d"
client = swagger.ApiClient(api_key, api_url)
wordApi = WordApi.WordApi(client)
	
def loading_bar(at, total):
	print str(at) + " out of " + str(total) + " definitions found"	
def get_definitions(list):
	all_the_definitions = ""
	total_words = len(list)
	for word in list:
		thread.start_new_thread(loading_bar, ((list.index(word)+1), total_words))
		definitions = wordApi.getDefinitions(word)
		all_the_definitions += word + " - \n"
		i = 1
		for definition in definitions:
			all_the_definitions += (str(i) + ". " + definition.text + "\n")
			i+=1
	return all_the_definitions
	
def get_definitions_new(lists):
	for word in lists:
		definitions = wordApi.getDefinitions(word)
		print word
		for definition in definitions:
			print definition.text

lists = read_words(words)
print get_definitions(lists)
