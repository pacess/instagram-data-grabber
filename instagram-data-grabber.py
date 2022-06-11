##------------------------------------------------------------------------------
##  Instagram Data Grabber
##------------------------------------------------------------------------------
##  Platform: Python3 + Ubuntu 20 + Raspberry Pi 4
##  Written by Pacess HO
##  Copyrights Pacess Studio, 2022.  All rights reserved.
##------------------------------------------------------------------------------

from selenium import webdriver
import time
import json
import os

##------------------------------------------------------------------------------
##  Global variables
_username = "charmainefong"

##------------------------------------------------------------------------------
def getDataOfInstagram(username):

    screenshotPath = "./instagram_"+username+".png"

    url = "https://www.instagram.com/"+username+"/"
    print("Start loading from "+url)
    _driver.get(url)

    time.sleep(5)
    _driver.save_screenshot(screenshotPath)

    ##------------------------------------------------------------------------------
    ##  Input username
    ##  Title = Login • Instagram
    print("Current page: "+_driver.title)

    inputField = _driver.find_element_by_name("username")
    inputField.send_keys("pacess@pacess.com")

    ##  Input password
    inputField = _driver.find_element_by_name("password")
    inputField.send_keys("riUVKaJUYNJWMQnQ")

    ##  Submit login form
    _driver.find_element_by_id("loginForm").submit()

    time.sleep(5)
    _driver.save_screenshot(screenshotPath)

    ##------------------------------------------------------------------------------
    ##  Click "Save Info" if this page appeared
    ##  Title = Instagram
    print("Current page: "+_driver.title)
    if (_driver.title == "Instagram"):

        button = _driver.find_element_by_xpath('//button[normalize-space()="Save Info"]')
        button.click()

        time.sleep(5)
        _driver.save_screenshot(screenshotPath)

    ##------------------------------------------------------------------------------
    ##  Retrieve information
    ##  Title = 方皓玟 Charmaine Fong (@charmainefong) • Instagram photos and videos
    print("Current page: "+_driver.title)

    posts = _driver.find_element_by_xpath("//ul/li[1]/div/span")
    print("Posts: "+posts.text)

    followers = _driver.find_element_by_xpath("//ul/li[2]/a/div/span")
    print("Followers: "+followers.get_attribute("title"))

    following = _driver.find_element_by_xpath("//ul/li[3]/a/div/span")
    print("Following: "+following.text)

    _driver.save_screenshot(screenshotPath)

    dictionary = {
        'GraphProfileInfo': {
            'info': {
                'followers_count': int(followers.replace(",", "")),
                'following_count': int(following.replace(",", "")),
                'posts_count': int(posts.replace(",", "")),
                'username': username
            },
            'source': driver.page_source
        }
    }
    return dictionary

##------------------------------------------------------------------------------
def saveInstagramData(dictionary, username):

    savePath = "../../Dataset/Instagram/"+username+"/"
    filename = time.strftime("%Y%m%d")+"_"+username+".json"
    subfolder = time.strftime("%Y.%m")

    ##  Create subfolder
    filePath = os.path.join(savePath, subfolder)
    filePath = os.path.join(filePath, filename)
    if not os.path.exists(os.path.dirname(filePath)):
        os.makedirs(os.path.dirname(filePath))

    ##  Write file
    print("Saving data to "+filePath)
    with open(filePath, "w") as file:
        json.dump(dictionary, file)
        file.close()

##==============================================================================
##  Main program
##------------------------------------------------------------------------------

##  Create headless Chrome browser
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-setuid-sandbox")
chromeOptions.add_argument("--disable-gpu")

##  This is important, otherwise crash
chromeOptions.add_argument("--headless")

##  iPhone 12
iphone12Emulation = {
    "deviceMetrics": {
        "width": 360,
        "height": 780,
        "pixelRatio": 3.0
    },
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
}
chromeOptions.add_experimental_option("mobileEmulation", iphone12Emulation)
_driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=chromeOptions)

##------------------------------------------------------------------------------
##  Grab data
username = _username
dictionary = getDataOfInstagram(username)
saveInstagramData(dictionary, username)

username = "jumbotsang"
dictionary = getDataOfInstagram(username)
saveInstagramData(dictionary, username)

##------------------------------------------------------------------------------
##  Finally, close browser
_driver.quit()
print("End")
