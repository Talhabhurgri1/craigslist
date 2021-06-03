from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from .models import Search

BASE_URL = 'https://losangeles.craigslist.org/search/?query={}'
url = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def index(request):
    return render(request,'base.html')


def search(request):

    output = request.POST.get('search')
    Search.objects.create(searches=output)
    final_url = BASE_URL.format(quote_plus(output))
    response = requests.get(final_url)
    data = response.text 
    print(data)
    soup = BeautifulSoup(data,'html.parser')
    post_listings = soup.find_all('li',{'class':'result-row'})
    final_posting = []

    for post in post_listings:
        
        post_title = post.find(class_='result-title').text 
        post_url = post.find('a').get('href')
        
        if post.find(class_='result-price')== None:
            post_price = 'N/A'
        else:
            post_price = post.find(class_='result-price').text

        if post.find(class_='result-image').get('data-ids') is not None:
           image_url= post.find(class_='result-image').get('data-ids').split(',')[0][2:]
           image_url = url.format(image_url)           
        else:
           image_url ='https://craigslist.org/images/peace.jgp'
           print(url)
        final_posting.append((post_title,post_url,post_price,image_url))
    else:
        msg = "Ooops didn't find any thing related to the searches "
    stuff_for_front_end = {'output':output,'final_posting':final_posting,'msg':msg}
    return render(request,'my_app/search.html',stuff_for_front_end)