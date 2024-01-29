import pymongo
import requests

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Debug-Daksh-100"]

# Access Collections
collection_table_1 = db["Table_1"]
collection_table_2 = db["Table_2"]

bearer_token = "1d9a867b-6702-4722-bc9e-23cf2ebae9bf"

headers = {
    "Authorization": f'Bearer {bearer_token}',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language" : "en-US,en;q=0.9",
    "Referer" : "https://www.grubhub.com/"
}


# Define the index range for fetching restaurant IDs
start_index = 481
end_index = 505

# Calculate the number of documents to skip and the limit
skip_count = start_index
limit_count = end_index - start_index


# Fetch restaurant IDs and location data from 'Table_1'
restaurant_data = collection_table_1.find({}, {"_id": 0, "restaurant_id": 1, "address.latitude": 1, "address.longitude": 1}).skip(skip_count).limit(limit_count)


# Iterate through each restaurant data entry
for restaurant in restaurant_data:
    restaurant_id = restaurant.get("restaurant_id")
    latitude = restaurant.get("address", {}).get("latitude")
    longitude = restaurant.get("address", {}).get("longitude")

    if restaurant_id and latitude and longitude:
        url = f"https://api-gtm.grubhub.com/restaurants/{restaurant_id}"
        params = {
            "hideChoiceCategories": "false",
            "version": "4",
            "variationId": "rtpFreeItems",
            "orderType": "standard",
            "hideUnavailableMenuItems": "false",
            "hideMenuItems": "false",
            # "location": f"POINT({longitude}%20{latitude})",  #this to be used if required only
            "locationMode": "delivery",
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            restaurant_data = data.get('restaurant', {})

            # Dictionary to hold category and dishes information
            categories_info = {}

            # Iterate through each category
            for category in restaurant_data.get('menu_category_list', []):
                category_name = category['name']
                dishes = []

                # Iterate through each item in the category
                for item in category.get('menu_item_list', []):
                    dish_name = item['name']
                    price_amount = item['price']['amount']
                    dishes.append({dish_name: price_amount})

                # Add the dishes list to the category
                categories_info[category_name] = dishes

            # Create a document for MongoDB insertion
            document = {
                "restaurant_id": restaurant_id,
                "categories": categories_info
            }
            collection_table_2.insert_one(document)

            print(f"Data for restaurant ID {restaurant_id} inserted into MongoDB collection 'Table_2'")
        else:
            print(f"Error fetching data for restaurant ID {restaurant_id}: {response.status_code}")
            print(response.text)
