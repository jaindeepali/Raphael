from bs4 import BeautifulSoup as BS
import requests
import urllib
import re
import urlparse
import numpy as np
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

def collect( link, style, count ):
	if count - 3 < 100:
		print 'skipping', style, 'due to low count'
		return

	print 'initiate process for', style

	paintings = []
	for i in range(1, 101):
		style_page = get( link + '/' + str( i ) )
		paintings_in_page = style_page.select( 'a.rimage img' )
		if len( paintings_in_page ) == 0:
			break

		paintings = paintings + paintings_in_page

	print 'list of paintings collected for', style

	if len( paintings ) - 3 < 50:
		print 'skipping', style, 'due to scraper problems'
		return

	training_path = os.path.join( '..', 'data', 'training', style )
	if not os.path.exists( training_path ):
		os.mkdir( training_path )

	testing_path = os.path.join( '..', 'data', 'testing', style )
	if not os.path.exists( testing_path ):
		os.mkdir( testing_path )

	if len( paintings ) - 3 < 150:
		print 'downloading paintings for', style, 'with count < 153'
		j, k = 1, 1
		random_access = np.random.random_integers( 0, len( paintings ) - 1, 3 )

		for i, painting in enumerate( paintings ):
			url = painting['src']
			if i in random_access:
				urllib.urlretrieve( iriToUri( _unicode( url ) ), os.path.join( testing_path, str( j ) + '.jpg' ) )
				print 'testing image', j, url
				j = j + 1
				continue

			urllib.urlretrieve( iriToUri( _unicode( url ) ), os.path.join( training_path, str( k ) + '.jpg' ) )
			print 'training image', k, url
			k = k + 1

	else:
		print 'downloading paintings for', style, 'with count > 153'
		random_access = np.random.random_integers( 0, len( paintings ) - 1, 153 )
		for i, idx in enumerate( random_access ):
			j = i + 1
			url = paintings[idx]['src']
			if j > 150:
				urllib.urlretrieve( iriToUri( _unicode( url ) ), os.path.join( testing_path, str( j - 150 ) + '.jpg' ) )
				print 'testing image', j - 150, url
			else:
				urllib.urlretrieve( iriToUri( _unicode( url ) ), os.path.join( training_path, str( j ) + '.jpg' ) )
				print 'training image', j, url

def scrape():
	training_path = os.path.join( '..', 'data', 'training' )
	if not os.path.exists( training_path ):
		os.mkdir( training_path )

	testing_path = os.path.join( '..', 'data', 'testing' )
	if not os.path.exists( testing_path ):
		os.mkdir( testing_path )

	style_list_page = get( '/en/paintings-by-style' )
	print 'list of styles collected'
	for style_element in style_list_page.select( 'div.search-item.fLeft' ):
		link = style_element.select( 'a.an.rimage.big' )[0]['href']
		style = style_element.select( '.r2c span.category' )[0].text.lower()
		count = int(style_element.select( '.l2c span.category' )[0].text)

		collect( link, style, count )

if __name__ == '__main__':
	scrape()
