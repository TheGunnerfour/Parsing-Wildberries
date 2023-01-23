import time
from selenium import webdriver
import csv

def get_feedback(id: int):
    #открываем экземпляр браузера и нужную нам страницу
    browser = webdriver.Firefox()
    browser.get(f'https://www.wildberries.ru/catalog/{id}/feedbacks')
    time.sleep(3)
    str = ''
    #определяем количество отзывов на продукт
    for word in browser.find_element('class name', 'product-line__param').text.split(' '):
        if word.isnumeric():
            str += word
    
    #создаем счетчики для цикла
    count_element = int(str)
    count_current_element = 0
    i = 1
    
    #основной цикл для занесения данных в csv файл
    while i < 500 and count_element != count_current_element and count_current_element != 1000:
        time.sleep(0.4)
        
        #выполняет JavaScript по прогрузке отзывов в окне
        browser.execute_script(f"window.scrollTo(0, {i * 1000})")
        #определяем количество прогруженных отзывов
        count_current_element = len(browser.find_elements('class name', "feedback__text"))
        print(f'{i} итерация, {count_current_element}/{count_element}')
        i += 1
        
    with open('C:/Users/akhma/Desktop/Python Dataset/feedbacks.csv', 'a') as csvfile:
        #находим и заносим в переменную текст отзыва
        text_feedback_elements = browser.find_elements('class name', "feedback__text")
        #находим и заносим в переменную оценку в отзыве
        text_feedback_rate = browser.find_elements('class name', "feedback__rating")

        fieldnames = ['rating', 'feedback']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for j in range(len(text_feedback_elements)):
            #проверка, если количество оценок меньше количества отзывов
            if len(text_feedback_rate) <= j:
                browser.quit()
                print('что-то не то')
                return
            
            #проверка, правильно ли выбран отзыв
            if len(text_feedback_rate[j].get_attribute('class')) != 0:
                #заносим в переменную rate оценку из отзыва
                rate = text_feedback_rate[j].get_attribute('class')[-1]
                #выводим оценку и текст отзыва для проверки правильности парсинга
                print(rate, text_feedback_elements[j].text)
                #записываем в csv полученную пару рейтинг-текст отзыва
                writer.writerow({'rating': rate, 'feedback': text_feedback_elements[j].text})
                

    browser.quit()


get_feedback(41675865)


