# from wikiHelper import getTablesHTML, parseTable, getRowsHTML, getColumnHTML, stripTags, htmlDecomposer
import pdb
import wikipedia
import csv
from google_images_download import google_images_download 
import re
import sys
import json


def titleToHTML(inputTitle):
	return wikipedia.page(inputTitle).html().encode('ascii','ignore')

def htmlDecomposerWithAdjustment(inputHTML,startTag,endTag,startAdjuster,endAdjuster):
	tagStarts = []

	currFindIndex = inputHTML.find(startTag,0)
	while (currFindIndex != -1):
		tagStarts.append(currFindIndex)
		currFindIndex = inputHTML.find(startTag,currFindIndex+1)

	tagEnds = []
	for start in tagStarts:
		tagEnds.append(inputHTML.find(endTag,start))

	decomposedHTML = []
	for i in range(len(tagStarts)):

		start = tagStarts[i]
		end = tagEnds[i]

		start += startAdjuster
		end += endAdjuster

		decomposedHTML.append(inputHTML[start:end])

	return decomposedHTML

def htmlDecomposer(inputHTML,startTag,endTag):
	return htmlDecomposerWithAdjustment(inputHTML,startTag,endTag,0,0)

def stripTags(colHTML):

	openingTagOpeningIndex = colHTML.find('<')
	openingTagClosingIndex = colHTML.find('>')

	#create opening tag
	openingTag = []
	for i in range(openingTagOpeningIndex+1,openingTagClosingIndex+1):
		openingTag.append(colHTML[i])
	openingTag = ''.join(openingTag)
	if ' ' in openingTag:
		openingTag = openingTag.split(' ')[0] + '>'

	#check to see if there are any opening tags
	if colHTML.find('<') == -1:
		return colHTML

	#find closing tag indices
	closingTagIndices = []
	currIndex = colHTML.find('</' + openingTag,0)
	while currIndex != -1:
		closingTagIndices.append(currIndex)
		currIndex = colHTML.find('</',currIndex+1)

	#check to see if the first full tag is a stand alone
	firstClosingTag = closingTagIndices[0]
	firstTagAndContents = []
	for i in range(openingTagClosingIndex+1,firstClosingTag):
		firstTagAndContents.append(colHTML[i])
	firstTagAndContents = ''.join(firstTagAndContents)
	if firstTagAndContents.find('<') == -1:
		return firstTagAndContents

	#else recurse
	newColHTML = colHTML[openingTagClosingIndex+1:closingTagIndices[-1]]
	return stripTags(newColHTML)

def buildTable(title,tableIndex,tableOpen,tableClose,rowOpen,rowClose,colOpen,colClose,outputName,keywordIndices):

	response = google_images_download.googleimagesdownload()
	pageHTML = titleToHTML(title)
	tableHTML = htmlDecomposer(pageHTML,tableOpen,tableClose)[tableIndex]
	
	table = []

	rowCounter = 0
	for rowHTML in htmlDecomposer(tableHTML,rowOpen,rowClose):

		if rowCounter == 10:
			break

		row = []
		keywords = []

		keywords.append('Iconic')
		for i,colHTML in enumerate(htmlDecomposerWithAdjustment(rowHTML,colOpen,colClose,0,len(colClose))):
			# print(colHTML)
			col = ''
			try:
				col = stripTags(colHTML)
				col = col.strip()
			except:
				print(colHTML)
				print('error')
				# pdb.set_trace()


			row.append(col)
			if i in keywordIndices:
				keywords.append(' ')
				keywords.append(col)

		keywords = ''.join(keywords)

		arguments = {
			"keywords":keywords,
			"limit": 1
		}
		paths = response.download(arguments) 
		row.append(paths.values()[0])
		table.append(row)

		rowCounter += 1

	with open(outputName, "wb") as f:
		writer = csv.writer(f,delimiter='%')
		writer.writerows(table)

	for row in table:
		print(row)

	print('Success, ' +outputName+ ' created.')

	return table

################
def createWikiTitle(newKey):
	name = newKey[:newKey.index('-'):]

	if name == 'baby name':
		return 'List of most popular given names'
	elif name == 'cities':
		return 'List of most populous cities'
	elif name == 'colleges':
		return 'Rankings of universities'
	elif name == 'movies': #not great but ok
		return 'Academy Award for Best Picture'
	elif name == 'books':
		return 'Le Monde\'s 100 Books of the Century'
	elif name == 'albums':
		return 'List of best albums'
	elif name == 'songs':
		return 'List of best songs'
	elif name == 'tv shows':
		return 'Highest rated television shows and programs'
	elif name == 'countries':
		return 'List of countries with the highest population'
	elif name == 'dog breeds':
		return 'List of dog breeds'
	else:
		return "List of most populous cities in the United States by decade"

##dictionary to map names to possible metrics
nameMetrics = {}
nameMetrics["baby names"] = ["overall popularity","boy popularity","girl popularity","5 year popularity boy","5 year popularity girl"]
nameMetrics["cities"] = ["population","area","cost of living","GDP","sports championships","oldest"]
nameMetrics["colleges"] = ["student population","student satisfaction","ranking","S2Tratio","athletic championships","endowment"]
nameMetrics["books"] = ["best selling", "nobel laureates"]
nameMetrics["movies"] = ["box office sales","opening day earnings","oscars won","critic reviews","fan reviews"]
nameMetrics["albums"] = ["gross sales","grammys won", "gross sales: rock","gross sales: pop","gross sales: rap"]
nameMetrics["songs"] = ["gross sales","grammys won", "gross sales: rock","gross sales: pop","gross sales: rap"]
nameMetrics["tv shows"] = ["total airtime","ratings","emmys won"]
nameMetrics["countries"] = ["population","area","cost of living","GDP","world cups","olympic medals","education","public transportation","defense spending","freedom index","incarceration rate","mass shootings"]
nameMetrics["dog breeds"] = ["overall popularity","most expensive"]



nmToWikiTitle = {}
for nmKey,metrics in nameMetrics.items():
	for metric in metrics:
		newKey = str(nmKey)+'-'+str(metric)
		value = createWikiTitle(newKey)
		nmToWikiTitle[newKey] = value











































# for key in nameMetrics.keys():

# 	newKey = key+'-'+nameMetrics[key][0]
# 	title = nmToWikiTitle[newKey]

# 	tableToGrab = 3
# 	if key == 'books':
# 		tableToGrab = 0
# 	if key == 'dog breeds':
# 		tableToGrab = 0


# 	print(title)
# 	print(tableToGrab)
# 	pdb.set_trace()

# 	buildTable(title,tableToGrab,"<table class=",'</table>','<tr>','</tr>','<td','</td>',key + '.csv',[0,1])

# args = sys.argv
# name = args[1]
# metric = args[2]
# key = name + '-' + metric

# https://en.wikipedia.org/wiki/List_of_best-selling_books
# https://en.wikipedia.org/wiki/Goodreads
# https://en.wikipedia.org/wiki/List_of_Nobel_laureates_in_Literature

#buildTable("List of most populous cities in the United States by decade",22,"<table class=",'</table>','<tr>','</tr>','<td','</td>','demoPecent.csv',[0,1])
#buildTable('Rankings of universities in the United States',10,"<table class=",'</table>','<tr>','</tr>','<td','</td>','demo1.csv',[0,1])
#buildTable('List of most popular given names',3,"<table class=",'</table>','<tr>','</tr>','<td','</td>','demo1.csv',[0,1])
# buildTable('Tourist attractions in the United States',0,"<table class=",'</table>','<tr>','</tr>','<td','</td>','demo1.csv',[0,1])



# import os
# os.remove("ChangedFile.csv")
# print("File Removed!")









#give choice of table -> 

# find pages , tables -> then download the sort 

# slide show be really ambitious -> first paragraph

# slide show there would be be the first wiki pedia page that mentions the metric -> 

# big of social media query twitter

#rotating the image




# #works for fully wrapped <></
# def stripTags(colHTML):


# 	# firstTagAndSome= colHTML[:openingTagIndex:]
# 	# firstTag = None
# 	# try:
# 	# 	fTandGarbage = firstTagAndSome.split(' ')
# 	# 	if len(fTandGarbage) > 1:
# 	# 		firstTag = fTandGarbage[0] + '>'
# 	# 	else:
# 	# 		firstTag = fTandGarbage[0] 
# 	# except:
# 	# 	pass

# 	# print(colHTML)
# 	# print(firstTagAndSome)
# 	# print(firstTag)

# 	# td a  a sup a a sup td
# 	# if firstTag ==  'a href="/wiki/Aruba" title="Aruba">Aruba':
# 	# 	print(colHTML[openingTagIndex::])
# 	# 	print('HIIIIT')
# 		# print(firstTag)
# 	# print('firstTagAbove')
# 	# if openingTagIndex == -1:
# 	# 	endOfOpeningTag = colHTML.find('>',0)
# 	# 	return colHTML[endOfOpeningTag+1:]



# 	# whatTheFuckIsThis
# 	# elif firstTag == -1:
# 	# 	print('hi')
# 	# 	pdb.set_trace
# 	# 	return None
# 			# currIndex = colHTML.find('</' ,0)

# 	openingTagOpeningIndex = colHTML.find('<')
# 	openingTagClosingIndex = colHTML[openingTagOpeningIndex:].find('>') 	#could be a bug

# 	firstTag = []
# 	for i in range(openingTagOpeningIndex+1,openingTagClosingIndex+1):
# 		char = colHTML[i]
# 		if char == ' ':
# 			firstTag.append('>')
# 			break
# 		firstTag.append(char)
# 	firstTag = ''.join(firstTag)


# 	# tests to see if we have no more opening tags
# 	if colHTML.find('<') == -1:
# 		return colHTML[openingTagClosingIndex+1::]
# 	else:

# 		#builds up matching tags
# 		closingTagIndices = []
# 		currIndex = colHTML.find('</'+firstTag,0)
# 		while currIndex != -1:
# 			closingTagIndices.append(currIndex)
# 			currIndex = colHTML.find('</'+firstTag,currIndex+1)

# 		#checks to see if the first match is an internall contained thing
# 		locString = colHTML[openingTagClosingIndex+1:closingTagIndices[0]]
# 		if locString.find('<'):
# 			print('here')
# 			retValue = locString[locString.find('>',0)+1::]
# 			return retValue

# 		#else strips on both sides the outermost
# 		newColHTML = colHTML[openingTagOpeningIndex+1:closingTagIndices[-1]]
# 		return stripTags(newColHTML)




