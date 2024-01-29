import json
import csv

# Function to calculate metrics for each restaurant
def calculate_metrics(restaurant_data):
    number_of_categories = len(restaurant_data['categories'])
    number_of_dishes = sum(len(category) for category in restaurant_data['categories'].values())

    total_price = 0
    price_count = 0
    for category in restaurant_data['categories'].values():
        for item in category:
            for price in item.values():
                if price > 0:  # Exclude prices that are 0 / not available
                    total_price += price
                    price_count += 1

    average_price = round(total_price / price_count, 2) if price_count else 0
    return number_of_categories, number_of_dishes, average_price

# Load JSON data
with open('Debug-Daksh-100.Table_2.json', 'r', encoding='utf-8') as file:
    restaurants = json.load(file)

# Prepare data for CSV
csv_data = []
for restaurant in restaurants:
    restaurant_id = restaurant['restaurant_id']
    number_of_categories, number_of_dishes, average_price = calculate_metrics(restaurant)
    csv_data.append([restaurant_id, number_of_categories, number_of_dishes, average_price])

# Write data to CSV
with open('formated_table2.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['restaurant_id', 'number_of_categories', 'number_of_dishes', 'average_price'])
    writer.writerows(csv_data)

