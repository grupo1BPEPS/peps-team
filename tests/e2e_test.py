from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

URL = "http://10.227.87.81:6101"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:

    driver.get(URL)

    # --- REGISTER ---
    driver.find_element(By.XPATH, "//button[contains(text(),'Crear cuenta')]").click()

    driver.find_element(By.ID, "username_register").send_keys("testuser")
    driver.find_element(By.ID, "password_register").send_keys("testpass")

    driver.find_element(By.XPATH, "//button[contains(text(),'Registrarse')]").click()

    time.sleep(1)

    # --- LOGIN ---
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("testpass")

    driver.find_element(By.XPATH, "//button[contains(text(),'Entrar')]").click()

    time.sleep(2)

    # --- BUSCAR RUTINA ---
    driver.find_element(By.ID, "dias").send_keys("3")

    driver.find_element(By.XPATH, "//button[contains(text(),'Buscar rutinas')]").click()

    time.sleep(2)

    print("E2E TEST PASSED")

finally:
    driver.quit()
