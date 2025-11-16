
import allure
from appium.webdriver.webdriver import WebDriver
from pytest_bdd import when, then, parsers

from vdit.utils import wait_for_element, AppiumExpect as AE


@when('설정 버튼 클릭')
@allure.step('설정 버튼 클릭')
def click_config_btn(app_session_driver: WebDriver):
    config_btn = wait_for_element(app_session_driver, 'ACCESSIBILITY_ID','btnHomeSettings')
    config_btn.click()

@when(parsers.parse('설정페이지 {language_btn_name} 항목 클릭'))
@allure.step('설정페이지 {language_btn_name} 항목 클릭')
def click_language_btn(app_session_driver: WebDriver,language_btn_name:str):
    config_btn = wait_for_element(app_session_driver, 'ACCESSIBILITY_ID','setting-language-cell')
    config_btn.click()

@when(parsers.parse('변경할 언어 "{language_name}" 클릭'))
@allure.step('변경할 언어 "{language_name}" 클릭')
def click_language_btn(app_session_driver: WebDriver,language_name:str):
    config_btn = wait_for_element(app_session_driver, 'ACCESSIBILITY_ID',language_name)
    config_btn.click()

@then(parsers.parse('"{title}" 타이틀 노출'))
@allure.step('"{title}" 타이틀 노출')
def visible_config_title(app_session_driver: WebDriver,title:str):
    config_title = wait_for_element(app_session_driver, 'XPATH','//XCUIElementTypeNavigationBar[@name="'+title+'"]')
    AE(app_session_driver, element=config_title).to_be_visible()