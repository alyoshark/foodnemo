import requests as r
from bs4 import BeautifulSoup as bs

FORM_URL = 'https://docs.google.com/forms/d/1emh8Bx6t8jt_zlgMvKq8t91yJkIc1CbIyzCCrlubrkQ'
IMG_CLASS = 'freebirdFormviewerViewItemsImageImage'
DISH_CLASS = 'freebirdFormviewerViewItemsItemItemTitle'
DISH_TYPES = ('nml', 'hal', 'veg')

def objectify_dishes(dish_list):
    result = {}
    for dish in dish_list:
        result[dish[0]] = {
            'img': dish[1],
            'name': dish[2],
            'price': dish[3],
        }
    return result


def get_dishes():
    raw = r.get(FORM_URL)
    soup = bs(raw.text, 'html.parser')
    dish_imgs = [i['src'] for i in soup.findAll('img', {'class': IMG_CLASS})]
    dish_titles = [i.next_element for i in soup.findAll("div", {'class': DISH_CLASS}) if i.contents]
    dish_names = [i.split('(')[0].strip() for i in dish_titles]
    dish_prices = [i.split('$')[1].strip() for i in dish_titles]
    return objectify_dishes(zip(DISH_TYPES, dish_imgs, dish_names, dish_prices))


if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(get_dishes())
