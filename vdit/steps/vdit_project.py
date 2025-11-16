
import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from pytest_bdd import when, then, parsers

from vdit.utils import wait_for_element, AppiumExpect as AE


@when(parsers.parse('프로젝트명 {project_name} 클릭'))
@allure.step('프로젝트명 {project_name} 클릭')
def click_project_name(app_session_driver: WebDriver,project_name:str):
    project = wait_for_element(app_session_driver, 'ACCESSIBILITY_ID',project_name)
    project.click()

@when('캔버스 버튼 클릭')
@allure.step('캔버스 버튼 클릭')
def click_canvas_btn(app_session_driver: WebDriver):
    canvas_btn = wait_for_element(app_session_driver, 'ACCESSIBILITY_ID',"icMainCanvas")
    canvas_btn.click()

@when('1:1 비율 버튼 클릭')
@allure.step('1:1 비율 버튼 클릭')
def click_11ratio_btn(app_session_driver: WebDriver):
    one_one_ratio_btn = wait_for_element(app_session_driver, 'ACCESSIBILITY_ID',"icCanvas11Instagram")
    one_one_ratio_btn.click()

@then('화면 비율이 1:1로 변경된다')
@allure.step('화면 비율이 1:1로 변경된다')
def aspect_video_11ratio(app_session_driver: WebDriver):
    video_frame = wait_for_element(app_session_driver, 'XPATH','//XCUIElementTypeApplication[@name="VDIT"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther')
    video_frame_x = video_frame.location["x"]
    video_frame_y = video_frame.location["y"]

    assert video_frame_x == 7 and video_frame_y == 59

@when(parsers.parse('텍스트 "{text}" 클릭'))
@allure.step('텍스트 "{text}" 클릭')
def click_text_obj(app_session_driver: WebDriver,text:str):
    text_obj = wait_for_element(app_session_driver, 'ACCESSIBILITY_ID',text)
    text_obj.click()

@when('서브메뉴 삭제 버튼 클릭')
@allure.step('서브메뉴 삭제 버튼 클릭')
def click_sub_menu_delete_btn(app_session_driver: WebDriver):
    sub_menu_delete_btn = wait_for_element(app_session_driver, 'ACCESSIBILITY_ID','icSubDeleteInverse')
    sub_menu_delete_btn.click()

@then(parsers.parse('텍스트 "{text}" 미 노출'))
@allure.step('텍스트 "{text}" 미 노출')
def disappear_text_obj(app_session_driver: WebDriver,text:str):
    text_obj = wait_for_element(app_session_driver, 'ACCESSIBILITY_ID',text)
    AE(app_session_driver,text_obj).not_to_be_visible()
