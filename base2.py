from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Launch the browser and navigate to the page
driver = webdriver.Chrome()
driver.get("https://www.flightradar24.com/airport/tlv/arrivals")

# Find the container element containing the rows
try:
    time.sleep(15)  # Wait for page to fully load before finding the container
    container = driver.find_element(By.CLASS_NAME, "sub-content-area.live-status")
except:
    print('Error: Container element not found on page.')
    driver.quit()
    exit()

# Extract the rows from the container
rows = container.find_elements(By.CLASS_NAME, "row")
data = []
for row in rows:
    time_elem = row.find_element(By.CLASS_NAME, "flight-time")
    time = time_elem.find_element(By.CLASS_NAME, "item").text.strip()
    
    from_elem = row.find_element(By.CLASS_NAME, "arrival-from")
    from_location = from_elem.find_element(By.CLASS_NAME, "item").text.strip()
    
    airline_elem = row.find_element(By.CLASS_NAME, "col-airline")
    airline = airline_elem.find_element(By.CLASS_NAME, "item").text.strip()
    
    flight_elem = row.find_element(By.CLASS_NAME, "col-flight-number")
    flight_number = flight_elem.find_element(By.CLASS_NAME, "item").text.strip()
    
    gate_elem = row.find_element(By.CLASS_NAME, "col-gate")
    gate = gate_elem.find_element(By.CLASS_NAME, "item").text.strip()
    
    status_elem = row.find_element(By.CLASS_NAME, "text-wrapper.big")
    status = status_elem.text.strip()
    
    details_elem = row.find_element(By.CLASS_NAME, "col-extra")
    details = details_elem.find_element(By.CLASS_NAME, "item").text.strip()
    
    data.append([time, from_location, airline, flight_number, gate, status, details])

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data, columns=['Time', 'From', 'Airline', 'Flight', 'Gate', 'Status', 'Details'])

# Print the DataFrame
print(df)

# Close the browser
driver.quit()
