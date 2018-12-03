from fullWikiBuilder import nameMetrics, nmToWikiTitle, buildTable
import os
import pdb

file = "/Users/danielknight/Downloads/inputs.txt"
titleKey = None
with open(file, "r+") as f:
	print('hi')
	titleKey = f.read()
	titleKey = titleKey.lower()
	titleKey = titleKey.replace('%','-')

print(titleKey)
tableToGrab = 3
key = titleKey.split('-')[0]
print(key)
if key == 'books':
	tableToGrab = 0
if key == 'dog breeds':
	tableToGrab = 0

title = nmToWikiTitle[titleKey]

#buildTable with the appropiate args
buildTable(title,tableToGrab,"<table class=",'</table>','<tr>','</tr>','<td','</td>','demoPecent.csv',[0,1])

#remove the file so we can do it again
os.remove(file)
print(file + "Removed!")