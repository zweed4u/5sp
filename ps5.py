#!/usr/bin/python3
import time
import argparse
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Optional


class SlackRequester:
    def __init__(self, url: Optional[str]):
        self.url = url

    def send_message(self, message: str):
        slack_response = requests.request("POST", self.url, json={"text": message})


print(f"[*] {datetime.datetime.now()} :: Parsing cli options")
parser = argparse.ArgumentParser()
parser.add_argument("--poll", type=int, default=60)
args = parser.parse_args()
poll = args.poll

print(f"[*] {datetime.datetime.now()} :: Reading config")
current_directory = os.path.dirname(os.path.realpath(__file__))
with open(f"{current_directory}/config.json") as json_file:
    config_data = json.load(json_file)
slack_webhook_url = config_data.get("webhook_url")
slack_requester = SlackRequester(slack_webhook_url)

slack_requester.send_message(
    f"<!channel> *{datetime.datetime.now()} UTC* - initializing ps5 bot"
)


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
            slack_requester.send_message(
                f"<!channel> *{datetime.datetime.now()} UTC* - 'queue' in url or hardlink redirect! - {ps5_url}"
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
                slack_requester.send_message(
                    f"<!channel> *{datetime.datetime.now()} UTC* - Add to cart button is displayed and hardlink had no redirect - {ps5_url}"
                )
        except Exception as exc:
            print(f"[*/!] {datetime.datetime.now()} :: Unable to find add button?")
            slack_requester.send_message(
                f"<!channel> *{datetime.datetime.now()} UTC* - Add to cart button element couldnt be found? - {ps5_url}"
            )
        time.sleep(poll)
    except (Exception, KeyboardInterrupt) as exc:
        print(f"[*] {datetime.datetime.now()} :: SIGINT caught - closing browser")
        slack_requester.send_message(
            f"<!channel> *{datetime.datetime.now()} UTC* - Exception was raised during runtime - ps5 bot exiting"
        )
        running = False
        continue
# driver.close() #raises an exception for some reason? (Failed to establish a new connection)
