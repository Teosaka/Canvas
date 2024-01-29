import subprocess

def install_requirements():
    print("Installing required libraries...")
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print("Libraries installed successfully.")
    except Exception as e:
        print(f"Error installing libraries: {e}")
        print("Please make sure you have pip installed and try installing the libraries manually.")
        exit(1)

try:
    import tkinter as tk
    from tkinter import simpledialog
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    try:
      install_requirements()
      import tkinter as tk
      from tkinter import simpledialog
      from selenium.webdriver.chrome.options import Options
      from selenium import webdriver
      from selenium.webdriver.common.keys import Keys
      from selenium.webdriver.common.by import By
      from selenium.webdriver.support.ui import WebDriverWait
      from selenium.webdriver.support import expected_conditions as EC
      from selenium.webdriver.chrome.service import Service as ChromeService
      from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
       print("Error in importing required libraries")
       exit(1)

def get_Classes(driver, user, pw):
  base = "https://canvas.uw.edu"
  driver.get(base)
  WebDriverWait(driver, 100).until(
     EC.presence_of_element_located((By.ID, 'weblogin_netid'))
  )
  driver.find_element(By.ID, 'weblogin_netid').send_keys(user)
  driver.find_element(By.ID, 'weblogin_password').send_keys(pw)
  driver.find_element(By.ID, 'submit_button').click()
  WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.ID, 'global_nav_courses_link'))
  )
  driver.find_element(By.ID, 'global_nav_courses_link').click()
  WebDriverWait(driver, 100).until(
     EC.presence_of_element_located((By.CLASS_NAME, 'css-1dsl5sr-view'))
  )
  class_container = driver.find_elements(By.CLASS_NAME, 'css-1t5l7tc-view--block-list')[1]
  classes = class_container.find_elements(By.TAG_NAME, 'a')
  links = {each_class.get_attribute('href') : each_class.text[:each_class.text.find(" ", each_class.text.find(" ") + 1)] for each_class in classes}
  return links

def get_assignments(driver, links):
  for link in links:
    driver.get(link + '/assignments')
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, 'assignment_group_upcoming_assignments'))
    )
    upcoming = driver.find_element(By.ID, 'assignment_group_upcoming_assignments')
    assignments = upcoming.find_elements(By.CSS_SELECTOR, 'li.assignment.sort-disabled.search_show')
    for item in assignments:
      # dateContainer = item.find_element(By.CLASS_NAME, 'ig-details__item assignment-date-due')
      # pointContainer = item.find_element(By.CLASS_NAME, 'ig-details__item js-score')
      # date = item.find_element(By.CSS_SELECTOR, 'div.ig-details__item.assignment-date-due').text
      # date = date[date.find('e') + 2: date.find("|") - 1]
      # points = item.find_element(By.CSS_SELECTOR, 'span.score-display').text
      # points = points[points.find('/') + 1:points.find(' ')]
      # print(date)
      # print(points)
      # text.write(date + " " + points)

        name = item.find_element(By.CSS_SELECTOR, 'a.ig-title').text
        partNum = 0
        assType = ''
        dueDate = ''
        parts = item.find_elements(By.CLASS_NAME, 'screenreader-only')
        for part in parts:
            if partNum == 0:
              assType = part.text
            elif partNum == 1:
                if 'at' in part.text:
                    dueDate = part.text[:part.text.find('at')-1]
                else:
                    dueDate = part.text
            else:
                points = part.text[part.text.find('.') + 2: part.text.find('p') - 1]
            partNum += 1
        text.write(name + '\n')
        text.write(assType + '\n')
        text.write(course + '\n')
        text.write(dueDate + '\n')

def main():
  user = simpledialog.askstring(title="Canvas", prompt="What's your Username?:")
  pw = simpledialog.askstring(title="number", prompt="What's your password")
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
  class_links = get_Classes(driver, user, pw)

if __name__ == '__main__':
   main()