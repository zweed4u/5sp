#!/usr/bin/python3
import time
import argparse
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options





poll = 60

print(f"[*] {datetime.datetime.now()} :: Reading config")


print(f"[*] {datetime.datetime.now()} :: Setting up webdriver options")
options = Options()
options.headless = True
# start-maximized flag doesnt work in headless - makes sense; instead explicitly set
# options.add_argument("--start-maximized")
options.add_argument("--window-size=1440x900")

print(f"[*] {datetime.datetime.now()} :: Initializing webdriver")
driver = webdriver.Chrome(options=options)
driver.delete_all_cookies()

ps5_url = (
    "https://direct.playstation.com/en-us/consoles/console/playstation5-console.3005816"
)
# cam_test_url = "https://direct.playstation.com/en-us/accessories/accessory/hd-camera.3005726"
running = True
while running:
    try:
        print(f"[*] {datetime.datetime.now()} :: Visiting...")
        driver.get(ps5_url)
        if "queue" in driver.current_url or driver.current_url != ps5_url:
            print(
                f"[!] {datetime.datetime.now()} :: 'queue' in url or url has redirected!"
            )
        try:
            add_btn = driver.find_element_by_class_name(
                "btn.transparent-orange-button.js-analyitics-tag.add-to-cart"
            )
            if add_btn.is_displayed() is False:
                print(
                    f"[*] {datetime.datetime.now()} :: Add to cart button on page on page but not visible - OOS :("
                )
            else:
                print(
                    f"[!] {datetime.datetime.now()} :: ADD TO CART BUTTON IS VISIBLE AND NO REDIRECT - GOGOGO!"
                )
        except Exception as exc:
            print(f"[*/!] {datetime.datetime.now()} :: Unable to find add button?")
        time.sleep(poll)
    except (Exception, KeyboardInterrupt) as exc:
        print(f"[*] {datetime.datetime.now()} :: SIGINT caught - closing browser")
        running = False
        continue
# driver.close() #raises an exception for some reason? (Failed to establish a new connection)
