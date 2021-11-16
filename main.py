import pyautogui
import time
import math
import random
import os
import sys
import requests
import wmi
import imaplib
import email
from email.header import decode_header
import webbrowser
import threading
from os.path import expanduser
import concurrent.futures
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
import concurrent.futures
from datetime import datetime
import time,string,zipfile,os
#import selenium

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
    
def press_key(key, driver):
    actions = ActionChains(driver)
    actions.send_keys(key)
    actions.perform()

def randpresskeys(keys,driver):
    chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','[',']','/','?',',','.']

    for key in keys:
        actions = ActionChains(driver)
        actions.send_keys(key)
        actions.perform()
        time.sleep(random.uniform(0.05, 0.25))
        #myrand = random.randint(0,25)
        #if myrand >= 22 and str(key) not in "1234567890":
            #press_key(chars[random.randint(0,int(len(chars)-1))],driver)
            #time.sleep(random.uniform(0.1,0.8))
            #press_key(Keys.BACKSPACE,driver)
            #time.sleep(random.uniform(0.3,0.7))

def randkeys(element, keys, driver):
    chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','[',']','/','?',',','.']
    for myi in keys:
        element.send_keys(myi)
        time.sleep(random.uniform(0.05, 0.25))
        #myrand = random.randint(0,25)
        #if myrand >= 22 and str(key) not in "1234567890":
            #element.send_keys(chars[random.randint(0,int(len(chars)-1))])
            #time.sleep(random.uniform(0.1,0.5))
            #press_key(Keys.BACKSPACE,driver)
            


def create_proxyauth_extension(proxy_host, proxy_port,proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """Proxy Auth Extension
    args:
        proxy_host (str): domain or ip address, ie proxy.domain.com
        proxy_port (int): port
        proxy_username (str): auth username
        proxy_password (str): auth password
    kwargs:
        scheme (str): proxy scheme, default http
        plugin_path (str): absolute path of the extension

    return str -> plugin_path
    """
    if plugin_path is None:
        file='./chrome_proxy_helper'
        if not os.path.exists(file):
            os.mkdir(file)
        plugin_path = file+'/%s_%s@%s_%s.zip'%(proxy_username,proxy_password,proxy_host,proxy_port)

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = string.Template(
    """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "${scheme}",
                host: "${host}",
                port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "${username}",
                password: "${password}"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


        
def initdriver(proxy,threadnum):
    print(proxy)
    chrome_options = webdriver.ChromeOptions()

    mobilerand = random.randint(0,10)
    useragents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  ,'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  ,'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  ,'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
                  ,'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1'
                  ,'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1'
                  ,'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'
                  ,'Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36']
    devicemetricslist1 = [640,
                          480,
                          768]
    
    devicemetricslist2 = [1136,
                          800,
                          1024]

    if mobilerand >= 3:
        metric = random.randint(0,int(len(devicemetricslist1)-1))
        mobile_emulation = {
            "deviceMetrics": { "width": devicemetricslist1[metric], "height": devicemetricslist2[metric], "pixelRatio": 3.0 },
        
        "userAgent": useragents[random.randint(0,int(len(useragents)-1))]}
        #chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    prefs = {"profile.managed_default_content_settings.images": 2,"download.default_directory": str(str(os.getcwd())+'\\downloads\\audio'+str(threadnum)+'\\')}
    chrome_options.add_experimental_option("prefs",prefs)

    # chrome_options.add_argument('--user-data-dir=C:\\Users\\exoti\\AppData\\Local\\Google\\Chrome\\User Data\\')
    #chrome_options.add_extension('buster.zip')
    #chrome_options.add_argument(str('--profile-directory=Default'))
    #chrome_options.add_argument("--start-maximized")
    #chrome_options.add_argument(str('--proxy-server='+str(proxy)))
    #chrome_options.add_argument("--headless")
    #countries = ['IE','US','UK','CA']
    proxyauth_plugin_path = create_proxyauth_extension(
    proxy_host=str(str(proxy.split(":")[0]).strip().replace("\n","").replace("\r","")),
    proxy_port=str(str(proxy.split(":")[1]).strip().replace("\n","").replace("\r","")),#80,
    proxy_username='',#+str(countries[therand])),#str(str(proxy.split(":")[2]).strip().replace("\n","").replace("\r","")),#"country-ca",
    proxy_password='',#str(str(proxy.split(":")[3]).strip().replace("\n","").replace("\r","")),
    scheme='http'
    )
    chrome_options.add_extension(proxyauth_plugin_path)
    
    driver = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)
    driver.set_page_load_timeout(90)
    driver.delete_all_cookies()
    #driver.set_window_position(-10000,0)
    return driver




def setreferer(request):
    del request.headers['Referer']
    #sources = ['https://google.com','https://instagram.com','https://facebook.com','https://yahoo.ca','https://bing.com','duckduckgo.com'] 
    
    request.headers['Referer'] = "https://google.com"


def sendcaptcha(fileopen):
    try:
        assemblyaivar = "putyourauthkeyhere"
        headers = {'authorization':assemblyaivar}
        response = requests.post('https://api.assemblyai.com/v2/upload',headers=headers,data=open(fileopen, 'rb'))
        print(response.json())

        time.sleep(5)
        endpoint = "https://api.assemblyai.com/v2/transcript"

        json = {
          "audio_url": str(response.json()['upload_url'])
        }

        headers = {
            "authorization": assemblyaivar,
            "content-type": "application/json"
        }

        response = requests.post(endpoint, json=json, headers=headers)

       

        status = ""

        while "completed" not in status:
            time.sleep(5)
            print("ID: "+str(response.json()['id']))
            endpoint = "https://api.assemblyai.com/v2/transcript/"+str(response.json()['id'])

            headers = {
                "authorization":assemblyaivar,
            }
            
            response = requests.get(endpoint, headers=headers)
            
        
            status = response.json()['status']
            finalresponse = response.json()
            print("Status: "+str(status))


        stringtotype = ""
        for words in finalresponse['words']:
            stringtotype = stringtotype+" "+str(words['text'])
            
        return stringtotype.strip().replace(".","").replace("-","").replace(",","")
    except Exception as ee:
        print("Error with sendcaptcha: "+str(ee))
        time.sleep(10)


def funcaptcha(driver,threadnum):
    #FUNCAPTCHA
    continuenow = False
    for _ in range(1):
        try:
            driver.switch_to.frame(driver.find_element_by_id('fc-iframe-wrap'))
            continuenow = True
            break
        except Exception as EEe:
            print("Error: "+str(EEe))
            time.sleep(2)
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'That Captcha did not work. Please try again.')]]").text
                for _ in range(40):
                    try:
                        driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[3]/button').click()
                        break
                    except Exception as EEe:
                        print("ER: "+str(EEe))
                        time.sleep(1)

                break
            except Exception as EEe:
                print("No error message")
    if continuenow == True:
        time.sleep(30)

        for _ in range(60):
            try:
                driver.find_element_by_xpath('/html/body/div[5]/div[2]/a[2]').click()
                break
            except Exception as EEe:
                print("Error: "+str(EEe))
                time.sleep(1)


        try:
            os.remove(str('downloads/audio'+str(threadnum)+'/'+str(os.listdir(str("downloads/audio"+str(threadnum)+"/"))[0])))
        except:
            print("No files there")

        for _ in range(10):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Download')]]").click()
                break
            except Exception as EEe:
                try:
                    driver.find_element_by_xpath('/html/body/div[5]/div[2]/a[2]').click()
                    break
                except Exception as EEe:
                    print("Error: "+str(EEe))
                    time.sleep(1)
                time.sleep(5)

        time.sleep(20)
        if len(os.listdir(str("downloads/audio"+str(threadnum)+"/"))) >= 1:
            print("File found")
            result = sendcaptcha(str("downloads/audio"+str(threadnum)+"/"+str(os.listdir(str("downloads/audio"+str(threadnum)+"/"))[0])))

        print(result)

        time.sleep(0.5)

        press_key(Keys.TAB, driver)

        time.sleep(0.5)

        randpresskeys(result,driver)

        time.sleep(0.5)

        press_key(Keys.TAB, driver)

        time.sleep(0.5)

        press_key(Keys.SPACE, driver)

            
        time.sleep(15)
        return True
   


def register(driver,threadnum):
    try:
        file = open("usernames.txt","r")
        userspossible = file.readlines()
        file.close()
        pref1 = str(userspossible[random.randint(0,int(len(userspossible)-1))]).strip().replace("\n","").replace("\r","")
        pref2 = str(userspossible[random.randint(0,int(len(userspossible)-1))]).strip().replace("\n","").replace("\r","")
        username = str(pref1+pref2+str(random.randint(99,9999))).strip().replace("\n","").replace("\r","")
   
        domains = ["@gmail.com","@yahoo.com","@outlook.com"]
        email = str(username+str(domains[random.randint(0,int(len(domains)-1))]))
        user = str(email.split("@")[0].strip().replace("\n","").replace("\r","")).replace(" ","").replace("-","")
        if len(user) >= 23:
            user = str(user.split(user[23])[0])
        chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0','$','!','#','%','&']
        password = str(chars[random.randint(0,int(len(chars)-1))]+chars[random.randint(0,int(len(chars)-1))]+chars[random.randint(0,int(len(chars)-1))]+chars[random.randint(0,int(len(chars)-1))]+chars[random.randint(0,int(len(chars)-1))]+chars[random.randint(0,int(len(chars)-1))]+chars[random.randint(0,int(len(chars)-1))]+chars[random.randint(0,int(len(chars)-1))]+chars[random.randint(0,int(len(chars)-1))]+chars[random.randint(0,int(len(chars)-1))]+"$$#$##"+str(random.randint(9999,9999999)))

        for _ in range(4):
            try:
                driver.get(urltovisit)
                break
            except Exception as EEEr:
                print("Error: "+str(EEEr))
        
        for myi in range(60):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Sign Up')]]").click()
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)
                if myi >= 20:
                    driver.refresh()
                    time.sleep(20)

        for myi in range(60):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Join Twitch today')]]").text
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)


        time.sleep(5)
        
        randpresskeys(user, driver)

        time.sleep(random.uniform(0.2,1.0))
        
        press_key(Keys.TAB, driver)

        time.sleep(random.uniform(0.2,1.0))

        randpresskeys(password, driver)

        time.sleep(1)
        time.sleep(random.uniform(0.2,1.0))
        
        press_key(Keys.TAB, driver)

        time.sleep(random.uniform(0.2,1.0))

        randpresskeys(password, driver)

        time.sleep(random.uniform(0.2,1.0))
        


        press_key(Keys.TAB, driver)

        time.sleep(random.uniform(0.2,1.0))

        press_key(Keys.ENTER, driver)

        time.sleep(random.uniform(0.2,1.0))

        months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','nov','dec']
        randpresskeys(months[random.randint(0,int(len(months)-1))], driver)

        press_key(Keys.ENTER, driver)

        time.sleep(random.uniform(0.2,1.0))


        press_key(Keys.TAB, driver)

        time.sleep(random.uniform(0.2,1.0))

        randpresskeys(str(random.randint(1,25)), driver)

        
        press_key(Keys.TAB, driver)

        time.sleep(random.uniform(0.2,1.0))

        randpresskeys(str(random.randint(1960,2001)), driver)

        for _ in range(10):
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'Use email instead')]]").click()
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)

        
        for _ in range(10):
            try:
                driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[4]/div/div[1]/div[2]/input").click()
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)
        

        randpresskeys(email, driver)

        time.sleep(random.uniform(0.2,1.0))

        time.sleep(1)

        press_key(Keys.TAB, driver)

        time.sleep(random.uniform(0.2,1.0))

        press_key(Keys.TAB, driver)

        time.sleep(random.uniform(0.2,1.0))

        press_key(Keys.TAB, driver)

        time.sleep(random.uniform(0.2,1.0))

        press_key(Keys.TAB, driver)
        
        time.sleep(random.uniform(0.2,1.0))

        press_key(Keys.SPACE, driver)

        time.sleep(random.uniform(0.2,1.0))
        
        successaccount1 = False
        breakl = True

        
        for _ in range(40):
            try:
                funcaptcha(driver,threadnum)
                driver.find_element_by_xpath("//*[text()[contains(.,'Remind me later')]]").click()
                breakl = False
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(2)

        
                
        if breakl == False:
            
            for _ in range(4):
                try:
                    driver.get(urltovisit)
                    break
                except Exception as EEe:
                    print("Error: "+str(EEe))
                    time.sleep(1)


            for _ in range(4):
                try:
                    driver.get(urltovisit)
                    break
                except Exception as EEe:
                    print("Error: "+str(EEe))
                    time.sleep(1)
           
            time.sleep(1)
            successaccount1 = True
        
        if successaccount1 == True:    
            #verifyemail(driver,email)
            file = open("myaccounts.txt","a")
            file.write(str(user.strip().replace("\r","").replace("\n","")+":"+password.strip().replace("\r","").replace("\n","")+"\n"))
            file.close()
        
    except Exception as EEE:
        print("MASTER LOOP: Exception: "+str(EEE))
        return

def login(driver,threadnum,user,passw):
    while True:
        try:
            for _ in range(4):
                try:
                    driver.get(urltovisit)
                    break
                except Exception as EEee:
                    print("Error: "+str(EEee))
                    time.sleep(1)

            for myi in range(60):
                try:
                    driver.find_element_by_xpath("//*[text()[contains(.,'Log In')]]").click()
                    break
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)

            for myi in range(60):
                try:
                    driver.find_element_by_xpath("//*[text()[contains(.,'Log in to Twitch')]]").text
                    break
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)


            time.sleep(1)

            randpresskeys(user, driver)

            time.sleep(random.uniform(0.2,1.0))

            time.sleep(1)

            press_key(Keys.TAB, driver)

            time.sleep(random.uniform(0.2,1.0))

            randpresskeys(passw, driver)

            time.sleep(random.uniform(4.0,6.0))

            for _ in range(40):
                try:
                    driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[3]/button').click()
                    break
                except Exception as EEe:
                    print("ER: "+str(EEe))
                    time.sleep(1)

            breakl = False
            stopcaptchas = False
            for _ in range(40):
                try:
                    if stopcaptchas == False:
                        if funcaptcha(driver,threadnum) == True:
                            stopcaptchas = True
                    driver.find_element_by_xpath("//*[text()[contains(.,'Remind me later')]]").click()
                    breakl = True
                    break
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(2)


            if breakl == True:
                time.sleep(15)
                return
        except Exception as EEe:
            print("Error: "+str(EEe))


def spamforums(driver,secondurl,threadnum,user):
    try:
        user = user.strip().replace("\n","").replace("\r","")
        login(driver,threadnum,user.split(":")[0],user.split(":")[1])

        for _ in range(2):
            try:
                driver.get(urltovisit)
            except Exception as EEee:
                print("Er: "+str(EEee))


        for _ in range(4):
            try:
                driver.get(secondurl)
                break
            except Exception as EEee:
                print("Error: "+str(EEee))
        time.sleep(30)
        chatelem = None
        breakl = False
        for _ in range(60):
            try:
                elements = driver.find_elements_by_tag_name('textarea')
                for element in elements:
                    if "Send a message" in str(element.get_attribute('placeholder')):
                        chatelem = element
                        try:
                            chatelem.click()
                        except:
                            print("No click")
                        time.sleep(2)
                        breakl = True
                        break
                if breakl == True:
                    break
            except Exception as EEee:
                print("Error: "+str(EEee))
                time.sleep(1)


        for myi in range(10):
            try:
                elements = driver.find_elements_by_tag_name('button')
                for element in elements:
                    try:
                        if "chat-rules-ok-button" in str(element.get_attribute('data-test-selector')):
                            element.click()
                            print("CLICKED ELEMENT")
                            break
                    except Exception as EEeee:
                        print("Err: "+str(EEeee))
                break
            except Exception as EEEe:
                print("Error: "+str(EEEe))
                time.sleep(1)


        file = open("script2.txt","r")
        script = file.read()
        file.close()
            
        while True:
            try:
                driver.find_element_by_xpath("//*[text()[contains(.,'You are banned from Chat')]]").text
                print("Banned from chat")
                break
            except Exception as EEee:
                print("Er: "+str(EEee))
            try:
                chatelem.send_keys(script.replace("#random",str(random.randint(9,99999))).replace("\n","").replace("\r",""))
                time.sleep(1)
                press_key(Keys.ENTER,driver)
                time.sleep(10)
            except Exception as EEee:
                print("Error: "+str(EEee))

        
    except Exception as EEe:
        print("Error: "+str(EEe))

def sendmessage(driver,chatelem,msg):
    while True:
        try:
            driver.find_element_by_xpath("//*[text()[contains(.,'You are banned from Chat')]]").text
            print("Banned from chat")
            break
        except Exception as EEee:
            print("Er: "+str(EEee))
        try:
            chatelem.send_keys(msg.replace("#random",str(random.randint(9,99999))))
            time.sleep(9)
            press_key(Keys.ENTER,driver)
            time.sleep(1)
            break
        except Exception as EEee:
            print("Error: "+str(EEee))

def spam(groupnumber,secondurl):
    groupnumber += 1
    global urltovisit
    try:
        #file = open("proxies.txt","r")
        #proxies = file.readlines()
        #file.close()

        #proxy = proxies[threadnum]
        file = open("myaccounts.txt","r")
        allaccounts = file.readlines()
        file.close()
        threadnum = int(int(groupnumber * 3) + 1)
        for i in range(len(allaccounts)):
            account = allaccounts[int(int(groupnumber * i) + 1)]
            driver = initdriver("megaproxy.rotating.proxyrack.net:222",threadnum)    
            driver.request_interceptor = setreferer

            #register(driver,threadnum)
            spamforums(driver,secondurl,threadnum,account)
            time.sleep(2)                   
            try:
                driver.close()
                driver.quit()
            except:
                print("Error closing driver")
            #time.sleep(random.uniform(7.000, 18.000))        
    except Exception as EEE:
        print("Error: "+str(EEE))
        try:
            driver.close()
            driver.quit()
        except:
            print("Error closing driver")


def supporter(user,messages,groupnumber,secondurl):
    try:
        groupnumber += 1
        thei = 0
        threadnum = int(int(groupnumber * 3))
        driver = initdriver("megaproxy.rotating.proxyrack.net:222",threadnum)    
        driver.request_interceptor = setreferer
        
        while True:
            thei += 1
        
            login(driver,threadnum,user.split(":")[0],user.split(":")[1])

            for _ in range(2):
                try:
                    driver.get(urltovisit)
                except Exception as EEee:
                    print("Er: "+str(EEee))


            for _ in range(4):
                try:
                    driver.get(secondurl)
                    break
                except Exception as EEee:
                    print("Error: "+str(EEee))
            time.sleep(30)
            chatelem = None
            breakl = False
            for myi in range(10):
                try:
                    elements = driver.find_elements_by_tag_name('button')
                    for element in elements:
                        try:
                            if "follow-button" in str(element.get_attribute('data-a-target')):
                                element.click()
                                break
                        except Exception as EEeee:
                            print("Err: "+str(EEeee))
                    break
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)
                    
            for _ in range(60):
                try:
                    elements = driver.find_elements_by_tag_name('textarea')
                    for element in elements:
                        if "Send a message" in str(element.get_attribute('placeholder')):
                            chatelem = element
                            try:
                                chatelem.click()
                            except:
                                print("No click")
                            time.sleep(2)
                            breakl = True
                            break
                    if breakl == True:
                        break
                except Exception as EEee:
                    print("Error: "+str(EEee))
                    time.sleep(1)


            for myi in range(10):
                try:
                    elements = driver.find_elements_by_tag_name('button')
                    for element in elements:
                        try:
                            if "chat-rules-ok-button" in str(element.get_attribute('data-test-selector')):
                                element.click()
                                break
                        except Exception as EEeee:
                            print("Err: "+str(EEeee))
                    break
                except Exception as EEEe:
                    print("Error: "+str(EEEe))
                    time.sleep(1)


            #CHECKS FOR MESSAGES FROM SPAM BOTS TO START
            file = open("script2.txt","r")
            script = str(file.readlines()[0]).strip().replace("\n","").replace("\r","")
            file.close()
            while True:
                for myi in range(2):
                    try:
                        elements = driver.find_elements_by_tag_name('button')
                        for element in elements:
                            try:
                                if "chat-rules-ok-button" in str(element.get_attribute('data-test-selector')):
                                    element.click()
                                    break
                            except Exception as EEeee:
                                print("Err: "+str(EEeee))
                        break
                    except Exception as EEEe:
                        print("Error: "+str(EEEe))
                        time.sleep(1)
                try:
                    driver.find_element_by_xpath(str("//*[text()[contains(.,'"+str(script)+"')]]")).text
                    break
                except Exception as EEee:
                    print("Error: "+str(EEee))
                time.sleep(1)
            #SUPPORT MESSAGES
            for message in messages:
                sendmessage(driver,chatelem,message.split("#")[0])
                time.sleep(int(str(message).split("#")[1].strip()))
            return
            
    except Exception as EEEE:
        print("MAIN SUPPORTER ERROR: "+str(EEEE))
#SUPPORTER AND MAIN THREAD
def main(groupnumber,secondurl):
    try:
        file = open(str("supporter1.txt"),"r")
        messages = file.readlines()
        file.close()

        file = open("supporters.txt","r")
        allaccounts = file.readlines()
        file.close()

        account = allaccounts[groupnumber]
        
        threading.Thread(target=supporter,args=[account,messages,groupnumber,secondurl]).start()
        time.sleep(135)
        
        threads = []
        #START 3 SPAM THREADS
        for i in range(3):            
            threads.append(threading.Thread(target=spam,args=[groupnumber,secondurl]))
            print("GROUP "+str(groupnumber)+" STARTED THREAD "+str(i))
        for thread in threads:
            thread.start()

                            
    except Exception as EEe:
        print("Error: "+str(EEe))
                    
def startthreads(groups):
    global secondurl
    threads = []
    for i in range(groups):
        threads.append(threading.Thread(target=main,args=[i,secondurl,]))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    



    
print("""
WELCOME TO TWITCH LIVE CHAT LEADS V.1
MESSAGE TWITCH.COM WITH LINKS AND "SUPPORTERS"
-
""")
urltovisit = "https://twitch.tv"
while True:
    try:
        threadstodo = int(input("# of Groups of bots: "))
    except:
        print("Invalid input, please try again")


while True:
    try:
        secondurl = str(input("URL of Twitch stream to message"))
    except:
        print("Invalid input, please try again")


print("Beginning LIVE CHAT LEADS V.1")
startthreads(threadstodo)

    
