from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Launch the browser and navigate to the page
driver = webdriver.Chrome()
driver.get("https://www.flightradar24.com/data/airports/tlv")

# Find the top routes element containing the data
try:
    top_routes = driver.find_element(By.CSS_SELECTOR, "ul.top-routes")
except:
    print('Error: Top routes element not found on page.')
    driver.quit()
    exit()

# Extract the data from the top routes
routes = []
for route in top_routes.find_elements(By.TAG_NAME, "li"):
    link = route.find_element(By.TAG_NAME, "a")
    name = link.get_attribute("title")
    code = link.text.strip()
    flights_per_week = route.find_element(By.CSS_SELECTOR, "span.pull-right").text.strip()
    routes.append((name, code, flights_per_week))

# Convert the data to a pandas DataFrame
df = pd.DataFrame(routes, columns=['AirportName', 'AirportCode', 'FlightsPerWeek'])

# Save the DataFrame to a CSV file
df.to_csv('top_routes.csv', index=False)

# Print the DataFrame
print(df)

# Close the browser
driver.quit()
