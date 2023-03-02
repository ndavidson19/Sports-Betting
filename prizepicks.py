from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3


import pandas as pd
from env import PRIZEPICKS_USER, PRIZEPICKS_PASSWORD

# Initialize the webdriver
driver = webdriver.Chrome()

# Navigate to the login page
driver.get("https://app.prizepicks.com/login")

# Find the username and password input fields
username_input = driver.find_element('id', "email-input")
password_input = driver.find_element('css selector', "input[type='password']")

# Enter your login credentials
username_input.send_keys(PRIZEPICKS_USER)
password_input.send_keys(PRIZEPICKS_PASSWORD)

# Submit the login form
password_input.send_keys(Keys.RETURN)

# Wait for the page to load after login
driver.implicitly_wait(10)


name = []
points = []
for projection in driver.find_elements('class name', "projection"):

    driver.execute_script("arguments[0].scrollIntoView();", projection)
    name.append(projection.find_element('class name', "name").text)
    points.append(projection.find_element('class name', "score").text)

print(name, points)
print(len(name), len(points))

points[0] = '21.5'

df = pd.DataFrame({'player_name': name, 'points': points})

# save df to sqlite database as a new table
conn = sqlite3.connect('player_props.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS prizepicks
                (player_name text, points text)''')

df.to_sql('prizepicks', conn, if_exists='replace', index=False)

conn.commit()

conn.close()






# Close the webdriver
driver.quit()
