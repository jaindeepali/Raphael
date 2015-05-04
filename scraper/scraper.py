from bs4 import BeautifulSoup as BS
import requests
import urllib
import os

base_url = 'http://www.wikiart.org'

def get( endpoint ):
	response = requests.get( base_url + endpoint )
	soup = BS( response.text )
	return soup

def scrape():
	art_movement_list_page = get( '/en/artists-by-art-movement' )
	for art_movement_element in art_movement_list_page.select( 'h6.artist-grouped a' ):
		art_movement = art_movement_element.text
		art_movement_page = get( art_movement_element['href'] )

		i = 1
		for artist_element in art_movement_page.select( 'p.bigtext a' ):
			artist = artist_element.text
			artist_page = get( artist_element['href'] )
			for painting_element in artist_page.select( 'a.rimage img' ):
				painting_url = painting_element['src']
				path = os.path.join( '..', 'data', 'training', art_movement )
				if not os.path.exists( path ): os.mkdir( path )
				path = os.path.join( path , str( i ) + '.jpg' )
				urllib.urlretrieve( painting_url, path )
				print painting_url + ' retrieved'
				i = i + 1

if __name__ == '__main__':
	scrape()
