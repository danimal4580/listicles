from fullWikiBuilder import nameMetrics, nmToWikiTitle, buildTable
import os
import pdb

##
file = "/Users/danielknight/Downloads/inputs.txt"

#wait to make sure the file is created
fileExistsHa = os.path.isfile(file)
while not fileExistsHa:
	fileExistsHa = os.path.isfile(file)
	# if fileExistsHa:
		# print(file + " Located!")
		# #get the key from file
		# titleKey = None
		# with open(file, "r+") as f:
		# 	print(f.read())
		# 	titleKey = f.read()
		# 	titleKey.lower()
		# 	titleKey.replace('%','-')
		# print(titleKey)

		# title = nmToWikiTitle[titleKey]

		# #buildTable with the appropiate args
		# buildTable(title,22,"<table class=",'</table>','<tr>','</tr>','<td','</td>','demoPecent.csv',[0,1])

		# #remove the file so we can do it again
		# os.remove(file)
		# print(file + "Removed!")

# titleKey = None
# with open(file, "r+") as f:
# 	print('hi')
# 	titleKey = f.read()
# 	titleKey = titleKey.lower()
# 	titleKey = titleKey.replace('%','-')

# print(titleKey)

# title = nmToWikiTitle[titleKey]

# #buildTable with the appropiate args
# buildTable(title,22,"<table class=",'</table>','<tr>','</tr>','<td','</td>','demoPecent.csv',[0,1])

# #remove the file so we can do it again
# os.remove(file)
# print(file + "Removed!")


