import os
import time
from selenium import  webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import firebase_admin
import smtplib
from firebase_admin import credentials
from firebase_admin import  firestore



cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
import datetime

# using now() to get current time
current_time = datetime.datetime.now()
db=firestore.client()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
#driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)



def getFlipkartPrice(url):
    driver.get(url)
    search_result = driver.find_element(By.XPATH, "//span[contains(@class,'B_NuCI')]")
    product_price = driver.find_element(By.XPATH, "//div[contains(@class,'_30jeq3 _16Jk6d')]")
    #print(search_result.text)
    try:
        p_img = driver.find_element(By.XPATH, "//img[contains(@class,'_396cs4 _2amPTt _3qGmMb  _3exPp9')]")
    except NoSuchElementException:
        p_img = driver.find_element(By.XPATH, "//img[contains(@class,'_2r_T1I _396QI4')]")

    product_img = p_img.get_attribute('src')
    price = product_price.text.replace(u'\u20B9', '')
    price = price.replace(',','')
    price = (int(price))
    #print(price)
    res = {
    "name": search_result.text,
    "price": price,
    "image": product_img
    }
    #print(res)
    return res


def getAmazonPrice(url):
    driver.get(url)
    search_result = driver.find_element(By.XPATH, "//span[contains(@id,'productTitle')]")
    try:
        product_price = driver.find_element(By.XPATH, "//span[contains(@id,'priceblock_dealprice')]")
    except NoSuchElementException:
        product_price = driver.find_element(By.XPATH, "//span[contains(@id,'priceblock_ourprice')]")

    p_img = driver.find_element(By.XPATH, "//img[contains(@class,'a-dynamic-image ')]")



    product_img = p_img.get_attribute('src')

    #print(product_img)
    #print(search_result.text)
    price = product_price.text.replace(u'\u20B9', '')
    price = price.replace(',','')
    price = (float(price))
    #print(price)
    res = {
        "name" : search_result.text,
        "price": price,
        "image": product_img
    }
    #print(res)
    return res








def send_mail(url,email,price,name):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('malushreyash@gmail.com','znmjsgqardhdszjn')
    subject = "Price Fell Down! for " + name
    body = 'Your favourite product '+ name  + ' is now just at Rs '+ str(price) +  ' Check the Product link Here ' + url
    msg = f"Subject:{subject}\n\n{body}"
    server.sendmail(
        'malushreyash@gmail.com',
        email,
        msg
    )
    print("Hey Email has been sent")
    server.quit()


def algo():
    todaysDate = current_time.year*10000 + current_time.month*100 + current_time.day
    userId = []
    price = []
    result = db.collection('users').get()


    for res in result:
        userId.append(res.id)
        # print(res.id)

    for u in userId:
        userProd = []
        product = db.collection('users').document(u).collection('urlDataCollection').get()

        for p in product:
            userProd.append(p.id)
        for k in userProd:
            col = db.collection('users').document(u).collection('urlDataCollection').document(k).get()

            currentInfo = col.to_dict()
            print(currentInfo)
            priceData = {
                '0': None,
                '1': None,
                '2': None,
                '3': None,
                '4': None,
                '5': None,
                '6': None,
                '7': None
            }




            lastDate = currentInfo["lastUpdatedDate"]
            purl = currentInfo["productUrl"]
            currentpriceData = currentInfo['prices']
            currentPriceSDatabase = currentInfo['currentPrice']
            if(currentInfo['type'] == 'amazon'):
                 trackres = getAmazonPrice(purl)
                 print('Amazon!!')
            else:
                trackres = getFlipkartPrice(purl)

            newPrice = trackres["price"]
            noList = ['0','1','2','3','4','5','6','7']
            limit = todaysDate - lastDate

            i = 0

            if(limit>0):
                while(i<(8-(limit))):
                    priceData[noList[i]] = currentpriceData[noList[i+limit]]
                    i = i+1
                priceData['7'] = newPrice
                print('New Date Updation')

            elif(limit == 0):
                if(currentPriceSDatabase > newPrice):
                    priceData = currentpriceData
                    priceData['7'] = newPrice
                elif(currentPriceSDatabase < newPrice):
                    currentInfo['currentPrice'] = newPrice
                    print('Price Change')
                    db.collection('users').document(u).collection('urlDataCollection').document(k).update(currentInfo)
                    continue
                else:
                    print('No Price Change')
                    continue


            currentInfo['prices'] = priceData
            currentInfo['currentPrice'] = newPrice
            currentInfo['lastUpdatedDate'] = todaysDate
            if (currentInfo['activeStatus'] == True):
                if (currentInfo['thresholdAlertStatus'] == True):
                    if (currentInfo['currentPrice'] < currentInfo['thresholdValue']):
                        mailid = getEmail(u)
                        send_mail(purl, mailid, newPrice, currentInfo['productName'])

                else:
                    mailid = getEmail(u)
                    send_mail(purl, mailid, newPrice, currentInfo['productName'])

            db.collection('users').document(u).collection('urlDataCollection').document(k).update(currentInfo)
            send_mail(purl, 'sarnobatadi@gmail.com', newPrice, 'Test Mail For Python Script')
            col = db.collection('users').document(u).collection('urlDataCollection').document(k).get()
            print('New Result After Update')
            print(col.to_dict())


def getEmail(id):
    result = db.collection('users').get()
    for res in result:
        if(res.id == id):
            dt = res.to_dict()

    return dt['email']













