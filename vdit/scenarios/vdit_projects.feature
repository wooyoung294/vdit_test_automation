Feature: vdit_프로젝트

  Scenario: vdit canvas 변경
    When 프로젝트명 데모 프로젝트 클릭
    When 캔버스 버튼 클릭
    When 1:1 비율 버튼 클릭
    Then 화면 비율이 1:1로 변경된다

  Scenario: vdit Text 삭제
    When 프로젝트명 데모 프로젝트 클릭
    When 텍스트 "Welcome to VDIT" 클릭
    When 서브메뉴 삭제 버튼 클릭
    Then 텍스트 "Welcome to VDIT" 미 노출
