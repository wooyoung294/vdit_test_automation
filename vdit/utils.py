from typing import Literal, Optional

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import base64
import io

import allure
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from PIL import Image
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


APP_LOCATORS = {
    'ID': AppiumBy.ID,
    'XPATH': AppiumBy.XPATH,
    'ACCESSIBILITY_ID': AppiumBy.ACCESSIBILITY_ID,
    'CLASS_NAME': AppiumBy.CLASS_NAME,
    'UIAUTOMATOR': AppiumBy.ANDROID_UIAUTOMATOR,
}
LocatorKey = Literal['ID', 'XPATH', 'ACCESSIBILITY_ID', 'CLASS_NAME', 'UIAUTOMATOR']


def wait_for_element(driver: WebDriver,by: LocatorKey, search_value: str, search_type:Literal['present','visible'] = 'visible', time: int = 10) \
        -> Optional[WebElement]:
    if search_type == "present":
        condition = EC.presence_of_element_located((APP_LOCATORS[by], search_value))
        poll = 1
    elif search_type == "visible":
        condition = EC.visibility_of_element_located((APP_LOCATORS[by], search_value))
        poll = 1
    else:
        raise ValueError("search_type은 'present' 나 'visible' 만 사용할 수 있습니다.")

    try:
        return WebDriverWait(
            driver,
            time,
            poll_frequency=poll,
            ignored_exceptions=(StaleElementReferenceException, NoSuchElementException),
        ).until(condition)
    except TimeoutException as e:
        print('No Such Element :',e)
        return None




def long_click(driver: WebDriver, element):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, 'touch'))
    actions.w3c_actions.pointer_action.move_to(element)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(2)  # 2초 대기
    actions.w3c_actions.pointer_action.release()
    actions.perform()


def get_emoticon_kind_count(driver: WebDriver) -> int:
    emoticons = wait_for_element(driver, 'CLASS_NAME', 'android.widget.HorizontalScrollView')

    _count = emoticons.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.ImageView')
    return len(_count)

def compare_elements_similarity(driver, path, target, threshold=0.99, attach_prefix='img_compare'):
    with Image.open(path) as im:
        buf = io.BytesIO()
        im.save(buf, format='PNG')
        ori_png = buf.getvalue()
    target_png = target.screenshot_as_png

    ori_b64 = base64.b64encode(ori_png).decode('ascii')
    target_b64 = base64.b64encode(target_png).decode('ascii')

    res = driver.get_images_similarity(ori_b64, target_b64, visualize=True)
    score = float(res.get('score', 0.0))

    # 리포트 첨부
    try:
        allure.attach(ori_png, name=f'{attach_prefix}_Expect', attachment_type=allure.attachment_type.PNG)
        allure.attach(target_png, name=f'{attach_prefix}_Actual', attachment_type=allure.attachment_type.PNG)
        diff_b64 = res.get('visualization')
        if diff_b64:
            allure.attach(
                base64.b64decode(diff_b64), name=f'{attach_prefix}_diff', attachment_type=allure.attachment_type.PNG
            )
    except Exception:
        pass

    assert score >= threshold, f'유사도 부족: score={score:.4f} < threshold={threshold}'


class AppiumExpect:
    def __init__(self, driver: WebDriver, element: WebElement = None, timeout: int = 5):
        self.driver = driver
        self.element = element
        self.timeout = timeout

    def _wait_until(self, condition, message: str = None) -> bool:
        try:
            WebDriverWait(
                self.driver,
                self.timeout,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(condition, message)
            return True
        except TimeoutException as e:
            raise AssertionError(message or f'[WAIT FAILED] Timeout after {self.timeout}s') from e

    def to_be_visible(self) -> bool:
        if not self.element:
            raise AssertionError("to_be_visible() requires 'element' to be set in AppiumExpect.")
        return self._wait_until(EC.visibility_of(self.element), '요소를 찾지 못함')

    def not_to_be_visible(self) -> bool:
        if not self.element:
            return True

        def _cond():
            try:
                return not self.element.is_displayed()
            except (NoSuchElementException, StaleElementReferenceException):
                return True

        return self._wait_until(_cond, '요소가 아직 화면에 보임')
    def not_to_be_enable(self):
        if not self.element:
            raise AssertionError("not_to_be_enable() requires 'element' to be set in AppiumExpect.")
        try:
            self._wait_until(EC.element_to_be_clickable(self.element), '요소가 활성화 상태')
            raise AssertionError('요소가 활성화 상태입니다')
        except TimeoutException:
            # 타임아웃 예외가 발생하면 요소가 비활성화된 상태이므로 정상
            return True

    def to_be_enable(self):
        if not self.element:
            raise AssertionError("to_be_enable() requires 'element' to be set in AppiumExpect.")
        assert self._wait_until(EC.element_to_be_clickable(self.element), '요소를 찾지 못했거나 비활성화 상태')

    def to_have_text(self, text: str) -> bool:
        if not text:
            raise AssertionError("not_to_have_text() requires 'text' to be set in AppiumExpect.")
        xpath = f"//*[contains(@text, '{text}')]"
        locator = (AppiumBy.XPATH, xpath)
        return self._wait_until(EC.presence_of_element_located(locator), f'텍스트를 포함하는 요소를 찾지 못함: {text}')

    def not_to_have_text(self, text: str):
        if not text:
            raise AssertionError("not_to_have_text() requires 'text' to be set in AppiumExpect.")
        xpath = f"//*[contains(@text, '{text}')]"
        locator = (AppiumBy.XPATH, xpath)

        self._wait_until(EC.invisibility_of_element_located(locator), f'[WAIT FAILED] "{text}" 가 존재합니다.')

