import base64

import allure
from allure_commons.types import AttachmentType
from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.common.exceptions import WebDriverException
import pytest


@pytest.fixture(scope='session')
def app_session_driver():
    caps = {
        "platformName": "iOS",
        "appium:automationName": "XCUITest",
        "appium:udid": "Your_udid",
        "appium:deviceName": "Your_device_name",
        "appium:platformVersion": "26.0.1",
        "appium:xcodeOrgId": "Your_ORG_ID",
        "appium:xcodeSigningId": "Apple Development",
        "appium:updatedWDABundleId": "Your_WebDriverAgentRunner",
        "appium:usePrebuiltWDA": False,
        "appium:showXcodeLog": True,
    }

    options = XCUITestOptions().load_capabilities(caps)
    driver = webdriver.Remote("http://localhost:4723", options=options)

    yield driver
    driver.quit()


@pytest.fixture(autouse=True, scope='function')
def app_function_driver(request, app_session_driver):
    app_session_driver.start_recording_screen()
    try:
        yield app_session_driver
    finally:
        try:
            raw = app_session_driver.stop_recording_screen()
        except WebDriverException:
            return

        video_data = base64.b64decode(raw)
        allure.attach(
            video_data,
            name=request.node.name,
            attachment_type=AttachmentType.MP4,
        )
