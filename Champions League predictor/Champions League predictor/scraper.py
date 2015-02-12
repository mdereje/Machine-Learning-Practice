from lxml import html
import requests
import sys
import xlrd
import xlwt
from mmap import mmap, ACCESS_READ
from xlrd import open_workbook, XL_CELL_TEXT, XL_CELL_NUMBER
'''
The data is to be imported from an excel file using the open source module
xlrd.
'''
GAMES_DATAPATH = "data/SeasonURL.xls"
gamesBook = open_workbook(GAMES_DATAPATH)
gamesSheet = gamesBook.sheet_by_index(0)

'''
dump out all scores from the website to this excel sheet
'''
SCORES_DATAPATH = "data/ScrapedData.xls"
scoresBook = xlwt.Workbook()
scoresSheet = scoresBook.add_sheet('scores')

'''
getURL takes in the season and returns the URL for scraping
The data table is stored in an excel file
'''
def getURL(season):
	
	regSesURL = [[0 for x in range(3)] for x in range(gamesSheet.nrows - 1)]
	allUrl = []
	for row in range(gamesSheet.nrows - 1):
		rnd = gamesSheet.cell_value(row + 1, 0)
		season = gamesSheet.cell_value(row + 1, 1)
		url = gamesSheet.cell_value(row + 1, 2)

		regSesURL[row][0] = rnd
		regSesURL[row][1] = season
		regSesURL[row][2] = url

		if  season == regSesURL[row][1]:
			allUrl.append(url)

	return allUrl

def store(urlTree):

	column  = 0;
	row = 0;
	for td in urlTree.iter('td'):
		
		if column == 5:
			column  = 0
			row += 1
		if td.text == None:			
			scoresSheet.write(row, column, td.find('strong').text)
		else:
			scoresSheet.write(row, column, td.text)
		column += 1
	scoresBook.save(SCORES_DATAPATH)

''' 
current scraping format only allows for regular season.
'''
def scrape():
	season = getURL(1992)
	for item in season:
		page = requests.get(item)
		tree = html.fromstring(page.text)
		store(tree)
	'page = requests.get(getURL(1992))'
	'tree = html.fromstring(page.text)'
	
scrape()

'''
printRaw function made to accomidate the utf8 printing method
for printing on screen
http://stackoverflow.com/questions/3597480/how-to-make-python-3-print-utf8
function only needed for python 3 utf8 encoding
'''

'''
def printRAW(Text):  
    RAWOut = open(1, 'w', encoding='utf8', closefd=False)  
    print(Text, file=RAWOut)  
    RAWOut.flush()  
    RAWOut.close()   
'''
'''
 iterates recursivly over the subtrees labeled 'td' table data in the
 UEFA webiste td.attrib returns returns attribute elements
'''


