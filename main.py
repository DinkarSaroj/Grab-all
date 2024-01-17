from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

chrome_driver_path = "C:/development/chromedriver.exe"  # Adjust path as necessary
chrome_options = Options()
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

def get_element_text(parent_element, selector):
    try:
        return parent_element.find_element(By.CSS_SELECTOR, selector).text
    except:
        return 'NA'

def get_element_attribute(parent_element, selector, attribute):
    try:
        return parent_element.find_element(By.CSS_SELECTOR, selector).get_attribute(attribute)
    except:
        return 'NA'

restaurants_data = []
page = 1
while page <= 20:
    url = f"https://www.grubhub.com/delivery/ny-nyc?pageNum={page}"
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(5)


    # try:
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="see-more-restaurants"]')))
        # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
    btn.click()
        # WebDriverWait(driver, 10).until(EC.staleness_of(btn))
    # except Exception as e:
    #     print(f"Error while clicking button: {e}")



    try:
        restaurants = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="restaurant-card"]')
        for restaurant in restaurants:
            name = get_element_text(restaurant, 'a[data-testid="restaurant-name"] h5')
            restaurant_link = get_element_attribute(restaurant, 'a[data-testid="restaurant-name"]', 'href')
            cuisine = get_element_text(restaurant, 'span[data-testid="cuisines"]')
            ratings = get_element_text(restaurant, 'span[data-testid="star-rating-text"]')

            restaurants_data.append({
                "Restaurant_Link": restaurant_link,
                "Name": name,
                "Ratings": ratings,
                "Cuisine": cuisine
            })
    except Exception as e:
        print(f"Error while scraping data: {e}")

    page +=1

driver.quit()

df = pd.DataFrame(restaurants_data)
df.to_csv("Restaurant_grubhub_data.csv", index=False, encoding='utf-8')
print(f"Data successfully written to Restaurant_grubhub_data.csv. Total records: {len(df)}")


