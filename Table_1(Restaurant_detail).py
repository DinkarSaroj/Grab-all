import json
import pymongo
import requests
import json
from urllib.parse import quote

url = "https://api-gtm.grubhub.com/restaurants/search/search_listing"

bearer_token = "e1781edc-f8a6-49c3-8eb6-216cc2318164"
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
# accept_language = "en-US,en;q=0.9"

headers = {
    "Authorization": f'Bearer {bearer_token}'
}
params = {
    "orderMethod":"delivery_or_pickup",
    "locationMode": "DELIVERY_OR_PICKUP",
    "facetSet":"seoBrowseV1",
    "pageSize": 36,
    "hideHateos":"true",
    "searchMetrics":"true",
    "sorts":"seo_default",
    "facet": "delivery_metros%3Abe391ec0-5cb7-4480-bba7-d5e55efa8e1b",
    # "facet" : "collapse_brand_id%3Atrue",
    "sortSetId" : "seoBrowse",
    "pageNum": 1,
    "countOmittingTimes":"true",
    "searchId": "3d18e074-b80d-11ee-a364-77cd85e534bb"
}
# Connect to MongoDB (adjust connection string as necessary)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Debug-Daksh-100"]
collection = db["Table_1"]

# Function to format restaurant name for URL
def format_restaurant_name(name):
    return quote(name.replace(' ', '-').lower())

# Loop through pages
for page in range(15):
    params['pageNum'] = page
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print(response.text)
        data = response.json()

        for restaurant in data['results']:
            ratings = restaurant.get('ratings', {})
            rating_count = ratings.get('rating_count', 0)
            rating_value = ratings.get('rating_value', '0')
            formatted_name = format_restaurant_name(restaurant.get('name', ''))
            restaurant_link = f"https://www.grubhub.com/restaurant/{formatted_name}/{restaurant.get('restaurant_id', '')}"
            restaurant_data = {
                'restaurant_id': restaurant.get('restaurant_id', ''),
                'restaurant_link': restaurant_link,
                'name': restaurant.get('name', ''),
                'rating_count': rating_count,
                'rating_value': rating_value,
                'address': restaurant.get('address', {}),
                'cuisines': restaurant.get('cuisines', []),
            }

            # Insert the restaurant data into Database
            collection.insert_one(restaurant_data)

        print("Data inserted into MongoDB")
    else:
        print(response.text)
        print(response.status_code)
        print("Error")


