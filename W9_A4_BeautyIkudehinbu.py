from bs4 import BeautifulSoup
import requests
import sys
import time
from csv import writer

#Connect to the website
amazon_url="https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_1?_encoding=UTF8&pg=1"

print("Data loading...")
#limit the runtime for the data fetching to 1 second
time.sleep(1)


#make soup function
def make_soup(amazon_url):
    #Raise exception in case of any problem regarding to network or the website
    try:
        #Give access to information on the website, this header was gotten from beautiful soup documentations
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.76 '
                          'Safari/537.36',
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }
        request_page = requests.get(amazon_url, headers=headers, params={"wait": 2})
        #lxml parser to get the lxml/html file of the webpage
        soup = BeautifulSoup(request_page.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print("Something went wrong", e)


#functions that takes all the books in the url page
def amazon_books(books):
    #Handle the situation whereby the data could not be gotten from the webpage and print out an info to the user then exit the program
    if not len(books.select(".zg-item-immersion")):
        print("Oops! Unable to get data. Check your internet connection and try again")
        sys.exit()
    else:
        #select required information from the webpage
        return (books.select(".zg-item-immersion"))


#function that selects the 10 most reviewed books. it takes only the reviews it takes the attribute books that will be used later on in the code
def most_reviewed(books):
    #create an empty list where the most reviewed books will be appended
    book_reviews = []
    for items in amazon_books(books):
        #Retrive only the reviews in each book. The "" in the beginning of the code takes the space at the beginning of the data away
        reviews = "".join([p.text for p in items.find_all('a', class_='a-size-small a-link-normal')])
        #Append the reviews gotten to the book_reviews list
        book_reviews.append(reviews)
    #sort the reviews so that it will be easier to get the highest number of reviews using the anonymous function
    sort_reviews = sorted(book_reviews, key=lambda x: (len(x), x))
    #sort the top the reviews
    sort_reviews = sort_reviews[-10:]
    return sort_reviews

#function that get the most expensive books and their price from the sort_reviews list
def my_expensive_list(books):
    # create an empty list where the most expensive books will be appended
    my_books = []
    #create an empty list where the price of the most expensive books will be appended
    price = []
    for items in amazon_books(books):
        for val in most_reviewed(books):
            #cast the value of the review to string
            if val in str(items):
                #Get the names of the books and append it to my_expensive_list
                my_books.append(items.find(name="div", class_="p13n-sc-truncate").text.strip())
                #get the prices of the books and append it to price list
                for cost in items.find(name="span", class_="p13n-sc-price"):
                    price.append(cost)
    print("\nTop 10 most reviewed books: Their title and price in an ascending order.\n")
    #Print the result data each in a new line and add/concartenate the price with it
    for i in range(0, len(my_books)):
        list = {my_books[i]: price[i]}
        print(list)

#Passing the data into a csv file for easy reading
    with open('Top 10 most reviewed books(Expensive).csv', 'w', newline='') as j:
        thewriter = writer(j)
        header = ['Title', 'Price']
        thewriter.writerow(header)
        info = [my_books, price]
        thewriter.writerow(info)
        
soup = make_soup(amazon_url)
amazon_books(soup)
most_reviewed(soup)
my_expensive_list(soup)
