#!/usr/bin/env python
# coding: utf-8

# In[4]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime

def scraping_top(url):
    # Launch the browser and navigate to the page
    driver = webdriver.Chrome()
    driver.get(url)
    # Wait for 10 seconds
    time.sleep(10)
    
    #Click on the cookies button
    try:
        cookies_accept = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookies_accept.click()
        time.sleep(2)
    except:
        print("Cookies already accepted or not found")
        
    #get the airport name
    element = driver.find_element(By.CSS_SELECTOR,'.airport-name')
    airport_name_list = element.text.split()
    if airport_name_list [0].startswith('Tel'):
        airport_name = airport_name_list [0] + "_" + airport_name_list [1]
    else:
        airport_name = airport_name_list [0]
    
    #load to the earlier flight
    while True:
        try:
            load_earlier_button = driver.find_element(By.CSS_SELECTOR, "button.btn-flights-load")
            load_earlier_button.click()
            time.sleep(2)  # Wait for the new data to load
        except:
            break 

    # Find the table element containing the data 
    try:
        table = driver.find_element(By.CSS_SELECTOR, "table.table-condensed.table-hover.data-table.m-n-t-15")
    except:
        print('Error: Table element not found on page.')
        driver.quit()
        exit()
    # Extract the data from the table
    data = []
    date = []
    To = []
    
    # Get all date separators
    date_separators = table.find_elements(By.XPATH, "//tr[contains(@class, 'row-date-separator')]")
    date_index = 0

    for row in table.find_elements(By.TAG_NAME, "tr"):
        day = datetime.now().strftime("%A")
        if "row-date-separator hidden-xs hidden-sm " in row.get_attribute("class") and day in row.text:
            break
        if row in date_separators:
            date_text = row.text.strip()
            date_index += 1

        # Skip the first row that only contains headers
        if "TIME" in row.text:
            continue

        cols = [col.text.strip() for col in row.find_elements(By.TAG_NAME, "td")]
        if len(cols) == 7:  # Make sure there are exactly 7 columns of data
            data.append(cols)
            To.append(airport_name)
            date.append(date_text)
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data, columns=['TIME', 'FLIGHT', 'FROM', 'AIRLINE', 'AIRCRAFT', '','STATUS'])
    df['DATE'] = date 
    df['TO'] = To
    
    new_order = ['DATE','TIME','FLIGHT', 'FROM','TO', 'AIRLINE','AIRCRAFT','STATUS','']
    df = df.reindex(columns=new_order)
    
    driver.quit()
    return df


# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def Top_search():
    # Launch the browser and naviglllate to the page
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
    airport_codes = [] 
    for route in top_routes.find_elements(By.TAG_NAME, "li"):
        link = route.find_element(By.TAG_NAME, "a")
        name = link.get_attribute("title")
        code = link.text.strip()
        flights_per_week = route.find_element(By.CSS_SELECTOR, "span.pull-right").text.strip()
        routes.append((name, code, flights_per_week))
        airport_codes.append(code)


    driver.quit()
    # Print the DataFrame

    return airport_codes

    # Close the browser


# In[ ]:


airport_codes = Top_search()
print(airport_codes)


# In[ ]:


df = scraping_top("https://www.flightradar24.com/data/airports/tlv/arrivals")
df.to_csv('arrivals2.csv', index=False)
i = 0
for code in airport_codes:
    print(i)
    url = "https://www.flightradar24.com/data/airports/" + code + "/arrivals"
    df = scraping_top(url)
    df.to_csv('arrivals2.csv', mode='a', header=False, index=False)
    i += 1
    time.sleep(15+i);


# In[ ]:


def wait1():
    time.sleep(200)


# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time

def delays(code,date,flight_time,des):
    # Create a new Chrome web driver
    driver = webdriver.Chrome()
    # Navigate to the web page containing the table
    driver.get("https://www.flightradar24.com/data/flights/" + code)
    #Click on the cookies button
    try:
        cookies_accept = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookies_accept.click()
        time.sleep(2)
    except:
        print('Error: cookies element not found on page.')

    scheduled_departures = None
    actual_departures = None
    scheduled_arrival = None
    actual_arrival = None
    list1 = [scheduled_departures,actual_departures,scheduled_arrival,actual_arrival]
    # Find all the rows in the table
    try:
        table = driver.find_element(By.ID, "tbl-datatable")
    except:
        print('Error: Table element not found on page.')
        return list1
        #driver.quit()
        #exit()
    # Loop through each row and check if it matches the search criteria
    
    try:
        for row in table.find_elements(By.TAG_NAME, "tr"):
            # Find the cells in the current row
            cells = row.find_elements(By.TAG_NAME, "td")
            # Debugging: print the length of the cells lis
            if len(cells) >= 2:
                temp = row.text.split(" ")
                row_date = temp[2]+ " " + temp[3] + " "+ temp[4]
                scheduled_departures= temp[-10]
                actual_departures= temp[-9]
                row_time = temp[-8][:5]
                actual_arrival= temp[-7]
                if len(row_time) == 4:
                    row_time = "0" + row_time
            # Check if the date and flight time cells match the search criteria
                if date == row_date:
                    if len(flight_time) == 4:
                        flight_time = "0" + flight_time
                    if flight_time == row_time:
                        list1[0] = scheduled_departures
                        list1[1] = actual_departures
                        list1[2] = row_time
                        list1[3] = actual_arrival
                        break
    except:
        return list1  
        
               
 # Close the web driver
    driver.quit()
    return list1


# In[ ]:


import pandas as pd
from datetime import datetime
import time
import random
import csv
x = 40
requests_per_minute=500
sleep_time = 10
df = pd.read_csv('arrivals2.csv')
i = 0
for index, row in df.iloc[i:].iterrows():
    if(i == 0):
        scheduled_departures =[]
        actual_departures = []
        scheduled_arrival = []
        actual_arrival = []
    try:
        if(i % 300 == 0 and i > 0):
            wait1()
        code_value = str(row['FLIGHT'])
        print(str(row['FLIGHT']))
        if code_value == 'nan':
            scheduled_departures.append(None)
            actual_departures.append(None)
            scheduled_arrival.append(None)
            actual_arrival.append(None)
            i+=1
            continue
        date_value = str(row['DATE'])
        dt = datetime.strptime(date_value, '%A, %b %d')
        # convert back to string in desired format using strftime()
        dt = dt.replace(year=datetime.now().year)
        date_value = dt.strftime('%d %b %Y')
        flight_time_value = str(row['TIME'])
        list1 = delays(code_value,date_value,flight_time_value,str(row['TO']))
        scheduled_departures.append(list1[0])
        actual_departures.append(list1[1])
        scheduled_arrival.append(list1[2])
        actual_arrival.append(list1[3])
        i+=1
        print(i)
        time.sleep(60 / requests_per_minute)
    except:
        wait1()
        i+=1
        scheduled_departures.append(None)
        actual_departures.append(None)
        scheduled_arrival.append(None)
        actual_arrival.append(None)
    if(i % 100 == 0):
        data ={}
        df2 = pd.DataFrame(data)
        df2['scheduled_departures'] = scheduled_departures
        df2['actual_departures'] = actual_departures
        df2['scheduled_arrival'] = scheduled_arrival
        df2['actual_arrival'] = actual_arrival
        df2.to_csv('arrivals3.csv')
df['scheduled_departures'] = scheduled_departures
df['actual_departures'] = actual_departures
df['scheduled_arrival'] = scheduled_arrival
df['actual_arrival'] = actual_arrival

# Create two sample dataframes
df1=pd.read_csv('arrivals5.csv')

df2=pd.read_csv('arrivals6.csv')

# Merge the two dataframes on a common column
frames = [df1, df2]

result = pd.concat(frames)

result.to_csv('arrivals10.csv')


# In[55]:


#data cleaning
import pandas as pd
df = pd.read_csv('arrivals10.csv')
df = df.dropna(subset=['FLIGHT'])
df = df.dropna(subset=['scheduled_departures'])
df = df[df['actual_departures'] != '—']
df.to_csv('arrivals10.csv', index=False)


# In[66]:


#returning all the time data to format - HH:MM
# read in the CSV file
df = pd.read_csv('arrivals10.csv')

# add leading zeros to flight numbers with length 4
df['scheduled_departures'] = df['scheduled_departures'].apply(lambda x: str(x).zfill(5) if len(str(x)) == 4 else x)
df['actual_departures'] = df['actual_departures'].apply(lambda x: str(x).zfill(5) if len(str(x)) == 4 else x)
df['scheduled_arrival'] = df['scheduled_arrival'].apply(lambda x: str(x).zfill(5) if len(str(x)) == 4 else x)
df['actual_arrival'] = df['actual_arrival'].apply(lambda x: str(x).zfill(5) if len(str(x)) == 4 else x)
# write out the modified DataFrame to a new CSV file
df.to_csv('arrivals10.csv', index=False)


# In[15]:



from datetime import datetime, timedelta
import math

delay_departure_list = []
delay_arrival_list = []
direction_departure =[]
direction_arrival =[]


end_day = datetime.strptime('23:59', '%H:%M')
start_day = datetime.strptime('00:00', '%H:%M')

for index, row in df.iterrows():
    # convert the actual_departures and scheduled_departures columns to datetime objects
    
    # format the datetime objects to strings with hours and minutes only
    actual_departures = datetime.strptime(row['actual_departures'], '%H:%M')
    scheduled_departures = datetime.strptime(row['scheduled_departures'], '%H:%M')
    
    actual_arrival = datetime.strptime(row['actual_arrival'], '%H:%M')
    scheduled_arrival = datetime.strptime(row['scheduled_arrival'], '%H:%M')
    
    actual_departures_hour_int = int(actual_departures.hour)
    scheduled_departures_hour_int = int(scheduled_departures.hour)
    
    temp_departures = actual_departures - scheduled_departures 
    
    if (temp_departures).days < 0:
        if( 20 <= scheduled_departures_hour_int and actual_departures_hour_int <=10):
            actual_departures+= timedelta(minutes=1)
            temp_departures = (end_day - scheduled_departures) + (actual_departures - start_day) 
        else:
            temp_departures = scheduled_departures - actual_departures
            temp_departures = '-' + str(temp_departures)
    elif(20 <= actual_departures_hour_int and scheduled_departures_hour_int <=10):
        scheduled_departures+= timedelta(minutes=1)
        temp_departures = '-' + str((end_day - actual_departures) + (scheduled_departures - start_day))
        
    actual_arrival_hour_int = int(actual_arrival.hour)
    scheduled_arrival_hour_int = int(scheduled_arrival.hour)
    
    temp_arrival = actual_arrival - scheduled_arrival 
    
    if (temp_arrival).days < 0:
        if( 20 <= scheduled_arrival_hour_int and actual_arrival_hour_int <=10):
            actual_arrival+= timedelta(minutes=1)
            temp_arrival = (end_day - scheduled_arrival) + (actual_arrival - start_day) 
        else:
            temp_arrival = '-' + str(scheduled_arrival - actual_arrival)
    elif (20 <= actual_arrival_hour_int and scheduled_arrival_hour_int <=10):
        scheduled_arrival+= timedelta(minutes=1)
        temp_arrival = '-' + str((end_day - actual_arrival) + (scheduled_arrival - start_day))
        
    temp_departures = str(temp_departures)
    temp_arrival = str(temp_arrival)
    
    delay_departure_list.append(temp_departures)
    delay_arrival_list.append(temp_arrival)
    
    # Add a column to indicate whether the difference is positive or negative
    if(temp_departures[0] == '-'):
        direction_departure.append('early')
    else:
        direction_departure.append('late')
    
    if(temp_arrival[0] == '-'):
        direction_arrival.append('early')
    else:
        direction_arrival.append('late')
    

df['delay_departure'] = delay_departure_list
df['direction_departure'] = direction_departure
df['delay_arrival'] = delay_arrival_list
df['direction_arrival'] = direction_arrival
df


# In[17]:


df.to_csv('arrivals10.csv')


# In[18]:





# In[ ]:




