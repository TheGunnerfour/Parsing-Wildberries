import time
from selenium import webdriver
import csv

def get_feedback(id: int):
    browser = webdriver.Firefox()
    browser.get(f'https://www.wildberries.ru/catalog/{id}/feedbacks')
    time.sleep(3)
    str = ''
    for word in browser.find_element('class name', 'product-line__param').text.split(' '):
        if word.isnumeric():
            str += word

    count_element = int(str)
    count_current_element = 0
    i = 1
    while i < 500 and count_element != count_current_element and count_current_element != 1000:
        time.sleep(0.4)
        browser.execute_script(f"window.scrollTo(0, {i * 1000})")
        count_current_element = len(browser.find_elements('class name', "feedback__text"))
        print(f'{i} итерация, {count_current_element}/{count_element}')
        i += 1
    with open('C:/Users/akhma/Desktop/Python Dataset/feedbacks.csv', 'a') as csvfile:
        text_feedback_elements = browser.find_elements('class name', "feedback__text")
        text_feedback_rate = browser.find_elements('class name', "feedback__rating")

        fieldnames = ['rating', 'feedback']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for j in range(len(text_feedback_elements)):
            if len(text_feedback_rate) <= j:
                browser.quit()
                print('что-то не то')
                return
            if len(text_feedback_rate[j].get_attribute('class')) != 0:
                rate = text_feedback_rate[j].get_attribute('class')[-1]
                print(rate, text_feedback_elements[j].text)
                writer.writerow({'rating': rate, 'feedback': text_feedback_elements[j].text})



    browser.quit()


get_feedback(60721902)


