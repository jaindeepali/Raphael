from bs4 import BeautifulSoup as BS
import requests

base_url = 'http://www.wikiart.org'

def get( endpoint ):
	response = requests.get( base_url + endpoint )
	soup = BS( response.text )
	return soup

def scrape():
	century_list_page = get( '/en/artists-by-century' )
	for century_element in century_list_page.select( 'h6.artist-grouped a' ):
		century = century_element.text[0:2]
		century_page = get( century_element['href'] )

		pager = century_page.select( 'div.pager-row.mb5' )
		if len(pager) == 0:
			artist_list = century_page.select()
		if len(pager) > 0:
			print century

if __name__ == '__main__':
	scrape()
