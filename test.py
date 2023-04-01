from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Launch the browser and navigate to the page
driver = webdriver.Chrome()
driver.get("https://www.flightradar24.com/data/airports/tlv/arrivals")

# Find the table element containing the data
try:
    time.sleep(2)  # Wait for page to fully load before finding the table
    table = driver.find_element(By.CSS_SELECTOR, "table.table-condensed.table-hover.data-table.m-n-t-15")
except:
    print('Error: Table element not found on page.')
    driver.quit()
    exit()

# Extract the data from the table
data = []
for row in table.find_elements(By.TAG_NAME, "tr"):
    cols = [col.text.strip() for col in row.find_elements(By.TAG_NAME, "td")]
    if len(cols) == 7:  # Make sure there are exactly 7 columns of data
        data.append(cols)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data, columns=['Time', 'From', 'Airline', 'Flight', 'Gate', 'Status', 'Details'])

# Print the DataFrame
print(df)

# Close the browser
driver.quit()
