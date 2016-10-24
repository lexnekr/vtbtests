from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

class test(object):
    
    def __init__(self, url, titleText, h1Text = False):
        self.driver = webdriver.Chrome(r'chromedriver.exe')
        self.url = url
        self.titleText = titleText
        self.h1Text = h1Text
        self.responseCode = requests.head(url).status_code
        
        try:
            self.driver.get(url)
        except:
            print ('\x1b[31mFAIL\x1b[0m - Страница (' + url + ') не доступна!')
            

    #def __del__(self):
    #    self.driver.close()

    def close(self):
        self.driver.close()
        
    def test_200(self):
        if self.responseCode == 200:
            print ('\x1b[32mSUCCESS\x1b[0m - Успешный тест страницы ' + self.url + ', код ' + str(self.responseCode))
        else:
            print ('\x1b[31mFAIL\x1b[0m - Не открывается страница ' + self.url + ', код ' + str(self.responseCode))
            
    def test_404(self):
        if self.responseCode == 404:
            print ('\x1b[32mSUCCESS\x1b[0m - Успешный тест страницы ошибки ' + self.url + ', код ' + str(self.responseCode))
        else:
            print ('\x1b[31mFAIL\x1b[0m - Код ошибка не соответсвует (' + self.url + '), код ' + str(self.responseCode))
        
    def test_title(self, r = False):
        try:
            assert self.titleText in self.driver.title
            print ('\x1b[32mSUCCESS\x1b[0m - Успешный тест страницы ' + self.url + ' на title')
            if r == True: return True
        except:
            print ('\x1b[31mFAIL\x1b[0m - Title не соответсвует заданному (' + self.url + ')')
            if r == True: return False
            
    def test_h1_count(self, r = False):
        try:
            elem = self.driver.find_elements_by_css_selector('h1')
            if len(elem)>1:
                print ('\x1b[31mFAIL\x1b[0m - На странице более 1 тега h1 (' + self.url + ')')
                if r == True: return False
            else:
                print ('\x1b[32mSUCCESS\x1b[0m - Успешный тест страницы ' + self.url + ' на количество h1')
                if r == True: return True
        except:
            print ('\x1b[31mFAIL\x1b[0m - Теги h1 на странице не найдены (' + self.url + ')')
            if r == True: return False
            
    def test_h1_text(self, r = False):
        try:
            elem = self.driver.find_element_by_css_selector('h1.page-title')
            if elem.text == self.h1Text:
                print ('\x1b[32mSUCCESS\x1b[0m - Успешный тест страницы ' + self.url + ' на текст h1')
                if r == True: return True
            else:
                print ('\x1b[31mFAIL\x1b[0m - Текст h1 не соответсвует заданному (' + self.url + ')')
                if r == True: return False
        except:
            print ('\x1b[31mFAIL\x1b[0m - Страница не содержит <h1 class = "page-title"> (' + self.url + ')')
            if r == True: return False

    def test_CB3194(self, key, r = False):
        # key = True/False
        # True --> Main Page
        # False --> Inner Pages
        try:
            elem = self.driver.find_element_by_css_selector('li.new-string.jOpenInfoBottom')
            self.driver.find_element_by_css_selector('li.new-string.jOpenInfoBottom').click()
            if key == False:
                print ('\x1b[31mFAIL\x1b[0m - Найден пункт меню "Информация в соответствии с Указанием ЦБ РФ № 3194-У" (' + self.url + ')')
                if r == True: return False
            try:
                elem = self.driver.find_element_by_css_selector('div.pico-content')
                try:
                    self.driver.find_element_by_css_selector('body > div.pico-content > div.pico-close').click()
                    print ('''\x1b[32mSUCCESS\x1b[0m - Пункт меню "Информация в соответствии с Указанием ЦБ РФ № 3194-У" найден.
        Клик вызывает блок "Информация о максимальных процентных ставках", который можно закрыть. ''' + self.url )
                    if r == True: return True
                except:
                    print ('''\x1b[31mFAIL\x1b[0m - Всплывающий блок "Информация о максимальных процентных ставках" не закрывается. 
        Блок вызывается пунктом меню "Информация в соответствии с Указанием ЦБ РФ № 3194-У" (''' + self.url + ')')
                    if r == True: return False
            except:
                print ('''\x1b[31mFAIL\x1b[0m - Всплывающий блок "Информация о максимальных процентных ставках" не найден. 
        Блок вызывается пунктом меню "Информация в соответствии с Указанием ЦБ РФ № 3194-У" (''' + self.url + ')')
                if r == True: return False
        except:
            if key == True:
                print ('\x1b[31mFAIL\x1b[0m - Пункт меню "Информация в соответствии с Указанием ЦБ РФ № 3194-У" не найден (' + self.url + ')')
                if r == True: return False
            else:
                print ('\x1b[32mSUCCESS\x1b[0m - Пункт меню "Информация в соответствии с Указанием ЦБ РФ № 3194-У" не найден (' + self.url + ')')
                if r == True: return True
            
    def test_CiteChange(self, r = False):
        try:
            elem = self.driver.find_element_by_css_selector('div.e-cur-item')
            elem.click()
            try:   
                elem = self.driver.find_element_by_css_selector('div.overlay')
                is_active = "display: block;" in elem.get_attribute("style")
                if not(is_active):
                    print ('\x1b[31mFAIL\x1b[0m - всплывающее окно со списком городов/стран не активно (' + self.url + ')')
                    if r == True: return False
                try:
                    try:
                        self.driver.find_element_by_css_selector('div.e-header > i').click()
                    except:
                        self.driver.find_element_by_css_selector('body > div.overlay > div.b-popup.b-popup-switcher.jSW > div.e-header > i').click()

                    print ('\x1b[32mSUCCESS\x1b[0m - всплывающее окно со списком городов/стран вызывается переключателем города (' + self.url + ')')
                    if r == True: return True
                except:
                    print ('\x1b[31mFAIL\x1b[0m - всплывающее окно со списком городов/стран не закрывается (' + self.url + ')')
                    if r == True: return False
            except:
                print ('\x1b[31mFAIL\x1b[0m - всплывающее окно со списком городов/стран не открывается (' + self.url + ')')
                if r == True: return False
        except:
            print ('\x1b[31mFAIL\x1b[0m - Переключатель города не найден (' + self.url + ')')
            if r == True: return False
            
            
            

 
            

class test_MainVTBru(test):
    
    def FirstMenuPoint(self, r = False):
        try:
            elem = self.driver.find_element_by_css_selector('td.item.i1._active')
            print ('\x1b[32mSUCCESS\x1b[0m - 1-я вкладка верхнего меню выделена (' + self.url + ')')
            if r == True: return True
        except:
            print ('\x1b[31mFAIL\x1b[0m - 1-я вкладка верхнего меню не выделена (' + self.url + ')')
            if r == True: return False
            try:
                elem = self.driver.find_element_by_css_selector('td.item.i1')
            except:
                print ('\x1b[31mFAIL\x1b[0m - Элемент меню с классом "item i1" не найден (' + self.url + ')')
                if r == True: return False