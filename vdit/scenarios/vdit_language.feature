Feature: vdit_언어 설정

  Scenario: vdit 한국어에서 영어로 언어 변경
    When 설정 버튼 클릭
    Then "설정" 타이틀 노출
    When 설정페이지 [언어] 항목 클릭
    When 변경할 언어 "English" 클릭
    Then "Settings" 타이틀 노출
