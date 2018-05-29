
'''
assumption: review content will not be made into prediction
The cleaned up reviews file had the following fields
1. Ratings
2. Author name or User name 3. Author Location
4. Date of Review
5. HotelID
6. Hotel Location
'''

import glob, json
import dateutil.parser
from xml.etree import ElementTree

def write_json(d, fname):
    '''write dictionary d to fname'''
    with open(fname,'w') as f:
        f.write(json.dumps(d))

def get_date(date):
    return dateutil.parser.parse(date)

def aggregate_rating(review):
    newrating = {}
    keys = review.keys()
    if len(keys)==1:
        newrating['business service'] = review['Overall']
        newrating['internet access'] = review['Overall']
        newrating['front desk'] = review['Overall']
        newrating['cleanliness'] = review['Overall']
        newrating['location'] = review['Overall']
        newrating['overall'] =review['Overall']
        newrating['rooms'] = review['Overall']
        newrating['service'] = review['Overall']
        newrating['sleep quality'] = review['Overall']
        newrating['value'] = review['Overall']
    else:
        newrating['business service'] = review.get('Business service',review['Overall'])
        newrating['internet access'] = review.get('Internet access',review['Overall'])
        newrating['front desk'] = review.get('front desk',review['Overall'])
        newrating['cleanliness'] = review.get('Cleanliness',review['Overall'])
        newrating['location'] = review.get('Location',review['Overall'])
        newrating['overall'] =review['Overall']
        newrating['rooms'] = review.get('Rooms',review['Overall'])
        newrating['service'] = review.get('Service',review['Overall'])
        newrating['sleep quality'] = review.get('Sleep Quality',review['Overall'])
        newrating['value'] = review.get('Value',review['Overall'])
    return newrating

def extract_hoteladdress(xmlstr):
    try:
        tree = ElementTree.ElementTree(ElementTree.fromstring(xmlstr))
        root = tree.getroot()
        for neighbor in root.iter('span'):
            if neighbor.get('property') == 'v:locality':
                return neighbor.text
    except:
        return ""
    
def load_file():
    files = glob.glob('./json/*.json')
    newdata = {}
    for each in files:
        with open(each) as f:
            data = json.load(f)
            for review in data['Reviews']:
                newRating = aggregate_rating(review['Ratings'])
                newdata[review['ReviewID']] = {'Ratings': newRating, 
                                               'Author': review['Author'],
                                               'Author Location': review.get("'AuthorLocation'", "").split(",")[0],
                                               'Date': str(get_date(review['Date'])), 
                                               'HotelID': data['HotelInfo']["HotelID"],
                                               'HotelLocation': extract_hoteladdress(data['HotelInfo'].get("Address", "")),
                                              }
    write_json(newdata,'./data/created/review.json')
    
if __name__ == '__main__':
    load_file()  