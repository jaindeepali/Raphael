from bs4 import BeautifulSoup as BS
import requests
import urllib
import re
import urlparse
import os

base_url = 'http://www.wikiart.org'

def get( endpoint ):
	response = requests.get( base_url + endpoint )
	soup = BS( response.text )
	return soup

def _unicode( string ):
	if isinstance( string, unicode ):
		result = string
	else:
		try:
			result = unicode( string, encoding='utf-8' )
		except UnicodeDecodeError:
			result = string.decode( 'latin1' ).encode( 'utf-8', 'replace' )

	return result

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )

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
				urllib.urlretrieve( iriToUri( _unicode( painting_url ) ), path )
				print painting_url + ' retrieved'
				i = i + 1

if __name__ == '__main__':
	scrape()
