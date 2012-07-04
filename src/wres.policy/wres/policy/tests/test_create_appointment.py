import unittest2 as unittest
from plone.testing.z2 import Browser
from plone.testing import z2
from selenium import webdriver
from time import sleep

import datetime


#Constants
wait_time = 3000
today = datetime.date.today()

#URLS default
port = '8080'
instance_name = raw_input("\n-----------------------------------------------------------------------\n\
\tInstrucoes para testes com o Selenium\n\
Certifique-se que voce rodou o debug_init para que pteste e dteste estejam disponiveis\n\
Certifique-se que o link do servidor eh localhost:8080.\nEnter CommuniMed site name:")
instance_URL = "http://localhost:" + port + "/" + instance_name + "/"
my_Calendar = instance_URL + "Appointments/dteste/Agenda"
login_URL = instance_URL + "login_form"
doctor_desk = instance_URL + "Appointments/sec_desk"

def wait(browser):
    browser.implicitly_wait(wait_time)

def go_to_window_with_text(browser,text):
        handles = browser.window_handles
        for handle in handles:
            wait(browser)
            browser.switch_to_window(handle)
            wait(browser)
            if text in browser.page_source:
                return
        raise NameError("ERRO: Texto nao encontrato!")
            
def click_option_by_text(browser,field_name,text):
    field = browser.find_element_by_name(field_name)
    options = field.find_elements()
    wait(browser)
    for option in options:
        #print "Comparando " + text + " " + option.text
        if text == option.text:
            option.click()
            return
    raise NameError("Erro: Opcao " + text + " nao encontrada")


class TestSetup(unittest.TestCase):
    def get_month_name(month):
        months = ["janeiro","fevereiro",u"mar\xe7o","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
        return months[month-1]
    
      
    def login(self,browser,user,password):
        wait(browser)
        browser.get(login_URL)
        wait(browser)
        wait(browser)
        user_field = browser.find_element_by_name("__ac_name")
        user_field.send_keys(user)
        wait(browser)
        
        password_field = browser.find_element_by_name("__ac_password")
        password_field.send_keys(password)
        wait(browser)
        
        submit = browser.find_element_by_name("submit")
        submit.click()
        wait(browser)
    
    def create_appointment_as_doctor(self,browser,
                                     start_year=str(today.year),
                                     start_month=get_month_name(today.month),
                                     start_day=str(today.day),
                                     start_hour=str(14),
                                     start_min=str(30),
                                     duration_min=str(50)):
        
        if not "id=\"portaltab-calendar\"" in browser.page_source:
            raise NameError("ERRO: Voce nao esta logado como medico.")
            return
        browser.get(my_Calendar)
        wait(browser)
        slot = browser.find_element_by_class_name("fc-slot30")
        slot.find_element_by_class_name("ui-widget-content").click()
        
        #Switch to pop-up frame
        browser.switch_to_frame("SFEventEditIFRAME")
        
        #Open window to find patient
        find_button = browser.find_element_by_id("popup_search_patient")
        find_button.click()
        wait(browser)
        
        #Go to new window
        go_to_window_with_text(browser, "Digite o nome, CPF")
        wait(browser)
        
        #Select Patient
        patient_field = browser.find_element_by_name("Title")
        patient_field.click()
        wait(browser)
        patient_field.clear()
        patient_field.send_keys("pteste")
        patient_link = browser.find_element_by_class_name("contenttype-patient")
        patient_link.click()
        wait(browser)
        
        #Back to Main window
        print "Cansei de testar... dormindo (Gambirra tensa.. se voce estiver animado pode tentar arruma-la)"
        sleep(1)
        print "Acordei"
        browser.switch_to_window(browser.window_handles[0])
        wait(browser)
        #Switch to pop-up frame again
        
        #Set apointment atributes
        
        browser.switch_to_frame("SFEventEditIFRAME")
        
        #Set years
        click_option_by_text(browser,"startDate_year",start_year)
        
        #Set month
        click_option_by_text(browser,"startDate_month",start_month)
        
        #Set days
        click_option_by_text(browser,"startDate_day", start_day)
        
        #Set hour
        click_option_by_text(browser,"startDate_hour",start_hour)
        
        #Set duration
        duration_field = browser.find_element_by_name("duration")
        duration_field.clear()
        duration_field.send_keys(str(duration_min))
        
        #Set minute
        click_option_by_text(browser,"startDate_minute",start_min)
        
        #Set insurance
        click_option_by_text(browser,"insurance","Outro")
        new_insurance = browser.find_element_by_id("other_insurance")
        new_insurance.send_keys("Salvacao")
        
        #Submit
        browser.find_element_by_name("form.button.save").click()
        wait(browser)
    
    
    def test_create_appointment(self):
         #Main commands
        print "\nTeste criar consulta, SELENIUM, comecou"
        browser = webdriver.Firefox()
        self.login(browser,"dteste","senha1")
        wait(browser)
        self.create_appointment_as_doctor(browser,start_min="15")
        browser.get(doctor_desk)
        assert("Salvacao" in browser.page_source)
        wait(browser)
        browser.close()
        print "----------------------------------------------------------------"
        print "Teste criar consulta, SELENIUM, terminou e foi um sucesso!!!!!!"
        print "----------------------------------------------------------------"
        
        
   
