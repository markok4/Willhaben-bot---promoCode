from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify
import time
from selenium.common.exceptions import NoSuchElementException
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


all_vehicles = []
seen_vehicles = set()


chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')


driver = webdriver.Chrome(options=chrome_options)


driver.get("https://sso.willhaben.at/auth/realms/willhaben/protocol/openid-connect/auth?response_type=code&client_id=bbx-bff&scope=openid&state=BJhZUzFPwyPvWLHMJPWu6IFGMoZ7PtaBu-2eTwexi4w%3D&redirect_uri=https://www.willhaben.at/webapi/oauth2/code/sso&nonce=AUXRz4jtYZ1IiMnzham6C0VGobb2rrFISzYuIuhMSQA")
time.sleep(5)  



email_field = driver.find_element(By.ID, "email")
email_field.send_keys("markokrstic001@gmail.com")


password_field = driver.find_element(By.ID, "password")
password_field.send_keys("marko990993MK1!")


input("Ručno rešite reCAPTCHA, a zatim pritisnite Enter za nastavak...")


login_button = driver.find_element(By.CLASS_NAME, "submit-button-text")
login_button.click()
time.sleep(5)

def accept_cookies():
    try:
        cookie_button = driver.find_element(By.ID, "didomi-notice-agree-button")
        cookie_button.click()
        print("Kliknuto na dugme za prihvatanje kolačića.")
    except NoSuchElementException:
        print("Dugme za kolačiće nije pronađeno.")
    finally:
        
        driver.get("https://www.willhaben.at/iad/gebrauchtwagen")


accept_cookies()

def click_search_button():
    try:
        search_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="search-submit-button"]')
        search_button.click()
        print("Kliknuto na dugme za pretragu vozila.")
    except NoSuchElementException:
        print("Dugme za pretragu vozila nije pronađeno.")


click_search_button()
time.sleep(5)


def load_vehicles_from_page():
    vehicle_names = driver.find_elements(By.CLASS_NAME, 'Text-sc-10o2fdq-0.kpTdIs')
    new_vehicles = []
    
    for vehicle in vehicle_names:
        vehicle_text = vehicle.text
        if vehicle_text not in seen_vehicles:
            new_vehicles.append(vehicle_text)
            seen_vehicles.add(vehicle_text)
    
    return new_vehicles


def go_to_next_page():
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Weiter zur nächsten Seite']")
        next_button.click()
        print("Kliknuto na sledeću stranicu.")
        return True
    except Exception as e:
        print("Nema sledeće stranice. Kraj.")
        return False


page_counter = 0

while True:
    new_vehicles = load_vehicles_from_page()
    
    if new_vehicles:
        all_vehicles.extend(new_vehicles)
    else:
        print("Nema novih vozila na ovoj stranici.")
    
    if page_counter >= 5: 
        print("Dostignut je 5. stranica. Završiću učitavanje vozila.")
        break
    
    if not go_to_next_page():
        break  
    
    page_counter += 1

    time.sleep(5)

driver.get("https://www.willhaben.at/iad/gebrauchtwagen")
time.sleep(30)

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    return jsonify({"vehicles": all_vehicles})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
