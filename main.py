import time
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Credentials
LOGIN = 'YOUR_LOGIN_HERE'
PASSWORD = 'YOUR_PASSWORD_HERE'


today = date.today()

delta = 1 if today.weekday() != 0 else 3

targetDay = today - timedelta(delta)

formattedToday = today.strftime('%d/%m/%Y')
formattedTargetDay = targetDay.strftime('%d/%m/%Y')

print('Today is', formattedToday)
print('Target day is', formattedTargetDay)

driver = webdriver.Chrome()
driver.get('http://manager.b2card.com.br/gestao_2/autenticacao/')

form1 = driver.find_element(By.NAME, value='login').send_keys(LOGIN)

form2 = driver.find_element(By.NAME, value='senha')
form2.send_keys(PASSWORD)
form2.send_keys(Keys.RETURN)

try:
    waitCondition = EC.presence_of_element_located((By.CLASS_NAME, 'tab-content'))
    WebDriverWait(driver, 15).until(waitCondition)
    
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Relatório').click()

    waitCondition = EC.presence_of_element_located((By.CLASS_NAME, 'dropdown-menu'))
    WebDriverWait(driver, 15).until(waitCondition)

    driver.find_element(By.PARTIAL_LINK_TEXT, 'Relatório de lançamentos').click()

    waitCondition = EC.presence_of_element_located((By.NAME, 'pesquisa'))
    WebDriverWait(driver, 15).until(waitCondition)

    formInput1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/form/div/div/div[2]/div[1]/div/input').send_keys(formattedTargetDay)
    formInput2 = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/form/div/div/div[2]/div[2]/div/input').send_keys(formattedTargetDay)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/form/div/div/div[2]/div[3]/button[1]').click()
    
    driver.execute_script('document.getElementsByClassName("navbar")[0].style.display = "none"')

    time.sleep(10)
    
    table_rows = driver.find_elements(By.XPATH, '//table/tbody[1]/tr')
    num_rows = len (table_rows)
    print(repr(num_rows) + ' rows in table')

    for row in table_rows:
        if formattedTargetDay in row.text:
            driver.set_window_size(830, 400)
            
            location = row.location
            x, y = location['x'], location['y']
            driver.execute_script('window.scrollTo({}, {})'.format(x,y))
            
            row.screenshot('test-row.png')
            driver.save_screenshot('Manager [{}].png'.format(targetDay.strftime('%d-%m-%Y')))
except:
    print('ERROR: Row not found')
finally:
    driver.quit()