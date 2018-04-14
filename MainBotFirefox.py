import re
import time
from time import strftime, localtime

try:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import Select
except ImportError:
    print("You don't have selenium on your device")
    exit()


def main():
    while (True):
        print("1. Type 1 buying with default information")
        print("2. Type 2 change Item you want to buy")
        print("3. Type 3 change Personal Information")
        print("4. Type 4 to exit")
        choose = input()
        if int(choose) == 1:
            personalInfo = readPersonInfo()
            item = readItem()
            print("Opening the browser")
            # chromeoption = webdriver.ChromeOptions()
            # chromeoption.add_argument('--user-data-dir=C:\\Users\\IronMan\\AppData\\Local\\Google\\Chrome\\User Data')
            # chrome_option=chromeoption
            fp = webdriver.FirefoxProfile(
                'C:\\Users\\IronMan\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\f34epq0m.default-1523640923193')
            browser = webdriver.Firefox(fp)
            while strftime("%H:%M", localtime()) != item[4]:
                print(strftime("%H:%M", localtime()))
            repeatCheck = 0
            # search the item on the Supreme new page with 10 times
            while (repeatCheck < 10):
                if goingtocheck(browser, item) != False:
                    print("find the item")
                    break
                else:
                    repeatCheck += 1
            if (repeatCheck == 10):
                print("Didn't find the Item")
                exit()

            # select Size
            delay = 10
            try:
                myElem = WebDriverWait(browser, delay).until(
                    EC.presence_of_element_located((By.NAME, "s")))
            except:
                print("Size loading are too slow")
                exit()
            try:
                sizeselect = Select(browser.find_element_by_name("s"))
                sizeselect.select_by_visible_text(item[3])
            except:
                print("Size is not available now")
                exit()
            # add to cart
            try:
                browser.find_element_by_name("commit").click()
            except:
                print("Size is not available now")
                exit()
            # check out
            time.sleep(1)
            browser.find_element_by_link_text("checkout now").click()
            if fillTheInfo(browser, personalInfo) is True:
                print("Great, the only now is wait your item be shipped")

            # else:
        elif int(choose) == 2:
            changeItem()
        elif int(choose) == 3:
            changePersonal()
        else:
            exit()


def fillTheInfo(browser, personalInfo):
    delay = 10
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME, "order[billing_name]")))
        print("Successfully entering the payment page")
    except:
        print("Item not available")
        exit()
    # name
    print(personalInfo[0])
    browser.find_element_by_name("order[billing_name]").send_keys("Jiarui Jiang")
    # email
    email = browser.find_element_by_name("order[email]").send_keys(personalInfo[1])
    # tel
    browser.find_element_by_id("order_tel").send_keys(personalInfo[2])
    # address
    browser.find_element_by_id("bo").send_keys(personalInfo[3])
    # apt
    browser.find_element_by_id("oba3").send_keys(personalInfo[4])
    # zip
    browser.find_element_by_id("order_billing_zip").send_keys(personalInfo[5])
    # city
    browser.find_element_by_id("order_billing_city").send_keys(personalInfo[6])
    # State
    stateselect = Select(browser.find_element_by_id("order_billing_state"))
    stateselect.select_by_visible_text(personalInfo[7])
    # Country
    stateselect = Select(browser.find_element_by_id("order_billing_country"))
    stateselect.select_by_visible_text(personalInfo[8])
    # card number
    browser.find_element_by_id("nnaerb").send_keys(personalInfo[9])
    # Card month
    stateselect = Select(browser.find_element_by_id("credit_card_month"))
    stateselect.select_by_visible_text(personalInfo[10])
    # Card year
    stateselect = Select(browser.find_element_by_id("credit_card_year"))
    stateselect.select_by_visible_text(personalInfo[11])
    # cvv
    browser.find_element_by_id("orcer").send_keys(personalInfo[12])
    # to pass the recaptcha, you need to do it by yourself
    # #checkbox
    # browser.find_element_by_class_name("iCheck-helper").click()
    #
    # try:
    #     browser.find_element_by_name("commit").click()
    #     return True
    # except:
    #     return False
    return True


def goingtocheck(browser, item):
    # item[0] is the category
    browser.get("http://www.supremenewyork.com/shop/all/" + item[0])
    delay = 10  # seconds
    try:
        # item[1] is the list of key word
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, item[1][0])))
        print("Page is ready!")
    except TimeoutException:
        return False
    namelink = browser.find_elements_by_class_name('name-link')
    counter = 0
    while counter < len(namelink):
        # item[2] is the color
        if checkItem(namelink[counter].text, item[1]) is True and item[2] in namelink[counter + 1].text:
            namelink[counter].click()
            try:
                # item[1] is the list of key word
                myElem = WebDriverWait(browser, delay).until(
                    EC.presence_of_element_located((By.NAME, "s")))
                print("Item detail Page is ready!")
            except TimeoutException:
                return False
            return True
        counter += 2
    return False


def checkItem(nameText, keywords):
    for i in keywords:
        if i not in nameText:
            return False
    return True


def readItem():
    lines = open('Item').read().splitlines()
    a = []
    for _ in lines:
        line = re.split(' ', _)
        if line[0] is 'keyword:':
            for i in range(1, len(line)):
                b = []
                b.append(line[i])
                a.append(b)
        else:
            a.append(line[1])
    return a


def readPersonInfo():
    lines = open('PersonalFile').read().splitlines()
    a = []
    for _ in lines:
        line = re.split(': ', _)
        a.append(line[1])
    return a


def changeItem():
    lines = open('Item').readlines()
    for _ in range(len(lines)):
        print(str(_ + 1) + ". " + lines[_], end='')
    print("\npick one you want to change or enter 0 to exit")
    check = 1
    while check != 0 and 0 <= check <= len(lines):
        check = int(input())
        if check != 0:
            print("Change to?")
            changeinput = input()
            line = re.split(': ', lines[check - 1])
            lines[check - 1] = line[0] + ": " + changeinput + "\n"
            print("Change to:" + lines[check - 1])
            print("pick one you want to change or enter 0 to exit")
    f = open('Item', 'w')
    for _ in lines:
        f.write(_)
    f.close()


def changePersonal():
    lines = open('PersonalFile').readlines()
    for _ in range(len(lines)):
        print(str(_ + 1) + ". " + lines[_], end='')
    print("\npick one you want to change or enter 0 to exit")
    check = 1
    while check != 0 and 0 <= check <= len(lines):
        check = int(input())
        if check != 0:
            print("Change to?")
            changeinput = input()
            line = re.split(": ", lines[check - 1])
            lines[check - 1] = line[0] + ": " + changeinput + "\n"
            print("Change to:" + lines[check - 1])
            print("pick one you want to change or enter 0 to exit")
    f = open('PersonalFile', 'w')
    for _ in lines:
        f.write(_)
    f.close()


if __name__ == '__main__':
    main()
