import requests
from bs4 import BeautifulSoup

#Creation/ouverture du fichier csv en ecriture 
with open('Book_informations.csv', 'w') as book_informations:
    book_informations.write('product_page_url'+ ',' +'universal_product_code'+ ',' + 'title'+ ',' +'price_including_tax'+ ',' +'price_excluding_tax'+ ',' +'number_available'+ ',' +'product_desciption'+
     ',' +'category'+ ',' +'review_rating'+ ',' +'image_url'+ '\n')

    #Requete sur l'url et test reponse
    product_page_url = 'http://books.toscrape.com/catalogue/william-shakespeares-star-wars-verily-a-new-hope-william-shakespeares-star-wars-4_871/index.html'
    reponse = requests.get(product_page_url)
    if reponse.ok:
        print(reponse)

        #Recuperation code source url
        soup_book = BeautifulSoup(reponse.text, features='html.parser')
        #Recuperation des donnees dans le code source
        title = soup_book.find('div', {'class' : 'col-sm-6 product_main'}).find('h1').text
        universal_product_code = soup_book.find('table', {'class': 'table table-striped'}).findAll('td')[0].text
        price_including_tax = soup_book.find('table', {'class': 'table table-striped'}).findAll('td')[3].text
        price_excluding_tax = soup_book.find('table', {'class': 'table table-striped'}).findAll('td')[2].text
        number_available = soup_book.find('table', {'class': 'table table-striped'}).findAll('td')[5].text.replace('In stock (','').replace('available)','')
        product_description = soup_book.findAll('p')[3].text
        category = soup_book.find('ul', {'class': 'breadcrumb'}).findAll('li')[2].find('a').text

        #Convertion str en note sur 5
        review_rating_str = soup_book.find('div', {'class': 'col-sm-6 product_main'}).findAll('p')[2]
        review_rating_str = str(review_rating_str['class'])
        review_rating_str = review_rating_str.replace("['star-rating', '", '').replace("']", '')
        review_rating = '0'
        if review_rating_str == 'Five':
            review_rating = '5/5'
        elif review_rating_str == 'Four':
            review_rating = '4/5'
        elif review_rating_str == 'Three':
            review_rating ='3/4'
        elif review_rating_str == 'Two':
            review_rating = '2/5'
        elif review_rating_str == 'One':
            review_rating = '1/5'

        image_url = soup_book.find('div', {'class': 'item active'}).find('img')
        image_url = str(image_url['src'])
        image_url = image_url.replace('../../', 'http://books.toscrape.com/')

        #Ecriture des donees dans le fichier csv
        book_informations.write(product_page_url + ',' + universal_product_code + ',' + title + ',' + price_including_tax + ',' + price_excluding_tax + ',' +
            number_available + ',' + product_description + ',' + category + ',' + review_rating + ',' + image_url + '\n')
    else:
        print('Page introuvale.')