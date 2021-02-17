import requests
from bs4 import BeautifulSoup

#Creation/ouverture du fichier csv en ecriture 
with open('Book_informations.csv', 'w', encoding='utf-8') as book_informations:
    book_informations.write('product_page_url'+ ',' +'universal_product_code'+ ',' + 'title'+ ',' +'price_including_tax'+ ',' +'price_excluding_tax'+ ',' +'number_available'+ ',' +'product_desciption'+
     ',' +'category'+ ',' +'review_rating'+ ',' +'image_url'+ '\n')

    #Requete url categorie et test reponse
    url_category = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'
    reponse_category = requests.get(url_category)
    if reponse_category.ok: 

        #Recuperation code source url, stockage liens livres 
        soup_category = BeautifulSoup(reponse_category.text, features='html.parser')
        #Test pagination
        nb_book = soup_category.findAll('strong')[1].text
        product_page_url = []
        if int(nb_book) <= 20:
            h3s = soup_category.findAll('h3')
            for h3 in h3s:
                a = h3.find('a')
                a = a['href'].replace('../../..', 'http://books.toscrape.com/catalogue')
                product_page_url.append(a)
                print(a)
        else:
            nb_page = soup_category.find('li', {'class': 'current'}).text.replace('Page 1 of ', '').strip()
            print(nb_page)
            i = 1
            while i <= int(nb_page):
                i_str = 'page-' + str(i)
                i += 1
                print(i_str)
                url_category_page_x = url_category.replace('index', i_str)
                print(url_category_page_x, '\n')
                reponse_category = requests.get(url_category_page_x)
                if reponse_category.ok:
                    soup_category = BeautifulSoup(reponse_category.text, features='html.parser')
                    h3s = soup_category.findAll('h3')
                    for h3 in h3s:
                        a = h3.find('a')
                        a = a['href'].replace('../../..', 'http://books.toscrape.com/catalogue')
                        product_page_url.append(a)
                        print(a)

        #Total livres 
        print('\n', len(product_page_url))

        i = 0
        while i < len(product_page_url):
            #Requete url livre et test reponse
            reponse_book = requests.get(product_page_url[i])
            if reponse_book.ok:
                print(reponse_book, '\t', i+1)

                #Recuperation code source url
                soup_book = BeautifulSoup(reponse_book.text, features='html.parser')
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
                book_informations.write(product_page_url[i] + ',' + universal_product_code + ',' + title + ',' + price_including_tax + ',' + price_excluding_tax + ',' +
                    number_available + ',' + product_description + ',' + category + ',' + review_rating + ',' + image_url + '\n')
                i += 1
            else:
                print('Page introuvale.')
