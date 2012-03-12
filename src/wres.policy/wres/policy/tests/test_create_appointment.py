from selenium import webdriver
import datetime


#Constants
wait_time = 3000
today = datetime.date.today()

#URLS default
instance_URL = "http://localhost:8080/Plone1/"
my_Calendar = "http://localhost:8080/Plone1/go2mycalendar"
login_URL = "http://localhost:8080/Plone1/login_form"
doctor_desk = "http://localhost:8080/Plone1/Appointments/sec_desk"

def get_month_name(month):
    months = ["janeiro","fevereiro",u"mar\xe7o","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
    return months[month-1]
    
def wait(browser):
    browser.implicitly_wait(wait_time)

def login(browser,user,password):
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

def create_appointment_as_doctor(browser,
                                 start_year=str(today.year),
                                 start_month=get_month_name(today.month),
                                 start_day=str(today.day),
                                 start_hour=str(14),
                                 start_min=str(30),
                                 duration_min=str(50),
                                 note="Nota da consulta - criada por teste no selenium"):
    
    if not "id=\"portaltab-Calendario\"" in browser.page_source:
        raise NameError("ERRO: Voce nao esta logado como medico.")
        return
    
    browser.get(my_Calendar)
    wait(browser)
    
    
    browser.find_element_by_class_name("fc-slot0").click()
    
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
    patient_field.send_keys("pteste")
    patient_link = browser.find_element_by_class_name("contenttype-patient")
    patient_link.click()
    wait(browser)
    
    #Back to Main window
    browser.switch_to_window(browser.window_handles[0])
    wait(browser)
    #Switch to pop-up frame again
    browser.switch_to_frame("SFEventEditIFRAME")
    wait(browser)
    
    #Set apointment atributes

    year_field = browser.find_element_by_name("startDate_year")
    click_option_by_text(year_field, start_year)

    month_field = browser.find_element_by_name("startDate_month")
    click_option_by_text(month_field, start_month)
    
    day_field = browser.find_element_by_name("startDate_day")
    click_option_by_text(day_field, start_day)
    
    hour_field = browser.find_element_by_name("startDate_hour")
    click_option_by_text(hour_field, start_hour)
    
    duration_field = browser.find_element_by_name("duration")
    duration_field.clear()
    duration_field.send_keys(str(duration_min))
    
    minute_field = browser.find_element_by_name("startDate_minute")
    click_option_by_text(minute_field, start_min)
    
    note_field = browser.find_element_by_name("note")
    note_field.send_keys(note)
    
    #Submit
    browser.find_element_by_name("form.button.save").click()
    wait(browser)

def go_to_window_with_text(browser,text):
    handles = browser.window_handles
    for handle in handles:
        wait(browser)
        browser.switch_to_window(handle)
        wait(browser)
        if text in browser.page_source:
            return
    raise NameError("ERRO: Texto nao encontrato!")
        
def click_option_by_text(field,text):
    options = field.find_elements()
    for option in options:
        print "Comparando " + text + " " + option.text
        if text == option.text:
            option.click()
            return
    raise NameError("Erro: Opcao " + text + " nao encontrada")

def test_create_appointment(browser):
    create_appointment_as_doctor(browser,start_min="15")
    browser.get(doctor_desk)
    if not "02:15 pm" in browser.page_source:
        raise NameError("FALHA: Ao criar consulta")

#Main commands
print "\nTeste criar consulta, SELENIUM, comecou"
browser = webdriver.Firefox()
login(browser,"dteste","senha1")
wait(browser)
test_create_appointment(browser)
wait(browser)
browser.close()
print "Teste criar consulta, SELENIUM, comecou"
