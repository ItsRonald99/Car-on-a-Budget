from bs4 import BeautifulSoup
import requests
import re
import math
import pandas as pd

alph = 'pleasecontact'
make = input('What make of car do you want to search for? \n')

make = make.lower()
url = f'https://www.kijiji.ca/b-cars-trucks/gta-greater-toronto-area/{make}/c174l1700272a54'


page = requests.get(url).text

doc = BeautifulSoup(page, 'html.parser')

num_search_results = doc.find('span', class_='resultsShowingCount-1707762110').text.split(' ')[-2]

num_pages = int(num_search_results)/40
num_pages = math.ceil(num_pages)

if num_pages == 0:
    num_pages+=1 

print(f'There are {num_pages} page(s) of results for this make of car.')
search_pages = input('How many pages would you like to search through?\n') 
car_dict = {}
car_table =[]
budget_cars = {}
#int(num_pages)+1
for i in range(1, int(search_pages)+1):
    url = f'https://www.kijiji.ca/b-cars-trucks/gta-greater-toronto-area/{make}/page-{i}/c174l1700272a54?ad=offering'
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')
    car_list = doc.find_all('div', class_='search-item regular-ad')
    for car in car_list:
        is_char = False
        price = car.find('div', class_='price').text.strip().replace(' ','').replace('\n','').split('M')[0]
        for char in alph:
            if char in price:
                is_char = True
        if not is_char:
            float_price = float(price.replace('$','').replace(',',''))
            if float_price > 1000.0: #posts that are less than $1000 are most likely not actual car postings.
                print(float_price)
                link = car.find('div', class_ ='title').a['href'].strip().replace('\n','')
                car_name = car.find('div', class_ ='title').a.text.strip().replace('\n','').lower()
                if 'wanted' not in car_name:
                    car_dict[car_name] = {'price': float_price, 'link': f'https://www.kijiji.ca{link}'}
                    car_table.append([car_name, float_price, link])

cheapest_cars = sorted(car_dict.items(), key = lambda x: x[1]['price'])[0:5]
most_expensive_cars = sorted(car_dict.items(), key = lambda x: x[1]['price']*-1)[0:5]

answer = input('Would you like to see a list of cars within a certain budget? (yes/no)\n')

if answer == 'yes':
    budget = input('Okay, what is your budget for buying a car?\n')

    for car_name in car_dict.keys():
        if car_dict[car_name]['price'] <= float(budget):
            budget_cars[car_name] = {'price': car_dict[car_name]['price'], 'link': car_dict[car_name]['link']}

    print(f'Great, here is a list of {make} cars that are within your budget range.\n')
    print(budget_cars)
    print()

answer = input(f'Would you like to see the cheapest {make} cars available? (yes/no)\n')

if answer == 'yes':
    print(cheapest_cars)

answer = input(f'Would you like to see the most expensive {make} cars available? (yes/no)\n')
if answer == 'yes':
    print(most_expensive_cars)

df = pd.DataFrame(car_table, columns = ['Car Name', 'Price', 'Link'])

print(df)

df.to_csv('cars_table.csv')


 
#implement a budget system where the user gives a budget and if the car's price is in that budget, it will display the car. 












