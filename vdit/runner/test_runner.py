from pytest_bdd import scenario

from vdit.steps.vdit_settings import *
from vdit.steps.vdit_project import *


@scenario('../scenarios/vdit_language.feature', 'vdit 한국어에서 영어로 언어 변경')
def test_change_language():
    pass

@scenario('../scenarios/vdit_projects.feature', 'vdit canvas 변경')
def test_change_canvas():
    pass

@scenario('../scenarios/vdit_projects.feature', 'vdit Text 삭제')
def test_delete_text():
    pass
