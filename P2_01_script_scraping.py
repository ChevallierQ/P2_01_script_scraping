import requests
from urllib import request
from bs4 import BeautifulSoup
import os

count = 0
#Initiale URL
url = 'http://books.toscrape.com/index.html'
reponse_url = requests.get(url)

#Source code recovery  
if reponse_url.ok:
    soup_url = BeautifulSoup(reponse_url.text, features='html.parser')
    url_category_name = []
    url_category_nb = soup_url.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('a')
    url_category = []
    i = 0
 
    while i < len(url_category_nb):
        url_category_name.append(soup_url.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('a')[i].text.strip())
        #Creation of all CSV files and writing column names
        with open(url_category_name[i] + '.csv', 'w', encoding='utf-8') as book_informations:
            book_informations.write('product_page_url'+ ' , ' +'universal_product_code'+ ' , ' + 'title'+ ' , ' +'price_including_tax'+ ' , ' +'price_excluding_tax'+ ' , ' 
            + 'number_available'+ ' , ' + 'product_desciption'+ ' , ' + 'category'+ ' , ' + 'review_rating'+ ' , ' +'image_url'+ '\n')
        #Retrieving the url of all categories
        x = url_category_nb[i]['href']
        url_category.append('http://books.toscrape.com/' + x )
        i += 1

for link in url_category:
    reponse_category = requests.get(link)

    if reponse_category.ok: 
        #Retrieving the source code and searching for the URL of the books in each category
        soup_category = BeautifulSoup(reponse_category.text, features='html.parser')
        nb_book = soup_category.findAll('strong')[1].text
        product_page_url = []

        #Test number of pages
        if int(nb_book) <= 20:
            h3s = soup_category.findAll('h3')

            for h3 in h3s:
                a = h3.find('a')
                a = a['href'].replace('../../..', 'http://books.toscrape.com/catalogue')
                product_page_url.append(a)

        else:
            nb_page = soup_category.find('li', {'class': 'current'}).text.replace('Page 1 of ', '').strip()
            i = 1

            while i <= int(nb_page):
                i_str = 'page-' + str(i)
                i += 1
                url_category_page_x = link.replace('index', i_str)
                reponse_category = requests.get(url_category_page_x)

                if reponse_category.ok:
                    soup_category = BeautifulSoup(reponse_category.text, features='html.parser')
                    h3s = soup_category.findAll('h3')

                    for h3 in h3s:
                        a = h3.find('a')
                        a = a['href'].replace('../../..', 'http://books.toscrape.com/catalogue')
                        product_page_url.append(a)
        i = 0

        while i < len(product_page_url):
            reponse_book = requests.get(product_page_url[i])

            #Retrieving the source code of each book
            if reponse_book.ok:
                soup_book = BeautifulSoup(reponse_book.text, features='html.parser')
                #Retrieving books data
                title = soup_book.find('div', {'class' : 'col-sm-6 product_main'}).find('h1').text
                universal_product_code = soup_book.find('table', {'class': 'table table-striped'}).findAll('td')[0].text
                price_including_tax = soup_book.find('table', {'class': 'table table-striped'}).findAll('td')[3].text
                price_excluding_tax = soup_book.find('table', {'class': 'table table-striped'}).findAll('td')[2].text
                number_available = soup_book.find('table', {'class': 'table table-striped'}).findAll('td')[5].text.replace('In stock (','').replace('available)','')
                product_description = soup_book.findAll('p')[3].text.strip()
                category = soup_book.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text
                #Conversion str to note per 5
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
                count += 1
                #Download image from book in a folder
                path = os.getcwd() + '\\Image\\'
                os.makedirs(path, exist_ok=True)
                final_title = path + str(count) + ' ' + title.replace(':', '').replace('/', ' ').replace('\\', '').replace('"',"'").replace('*', '').replace('?','').replace('|', '').replace('<','').replace('>','') + '.jpg'
                if len(final_title) >= 256:
                    final_title = final_title[:250]  + '.jpg'
                request.urlretrieve(image_url, final_title)

                #Writing data in the right CSV files 
                with open(category + '.csv', 'a', encoding='utf-8') as book_informations:
                    book_informations.write(product_page_url[i] + ' , ' + universal_product_code + ' , ' + title + ' , ' + price_including_tax + ' , ' + price_excluding_tax + ' , ' +
                        number_available + ' , ' + product_description + ' , ' + category + ' , ' + review_rating + ' , ' + image_url + '\n')
                    i += 1