from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import random
import pyautogui

#함수들 정의

#좌석선택함수
def find_and_click_random_coordinate(target_rgb, start_x, start_y, end_x, end_y):
    screenshot = pyautogui.screenshot()

    matching_coordinates = []
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            pixel_rgb = screenshot.getpixel((x, y))
            if pixel_rgb == target_rgb:
                matching_coordinates.append((x, y))

    if matching_coordinates:
        random_coordinate = random.choice(matching_coordinates)
        pyautogui.click(*random_coordinate)

        # 좌석 선택 완료 버튼을 찾습니다.
        booking_button = driver.find_element(By.CLASS_NAME, "booking")

        # 좌석 선택 완료 버튼을 클릭합니다.
        booking_button.click()
    time.sleep(0.2)


# 셀레니움 웹 드라이버를 초기화합니다.
driver = webdriver.Chrome()

# 브라우저 창을 최대화합니다.
driver.maximize_window()

# 웹 페이지로 이동합니다.
driver.get("http://ticket.yes24.com/Special/46237")

try:
    # id가 "consiceLogin"인 태그를 찾아 클릭합니다.
    consice_login_element = driver.find_element("id", "consiceLogin")
    consice_login_element.click()

    # id가 "SMemberID"인 태그를 찾아 아이디를 입력합니다.
    s_member_id_element = driver.find_element("id", "SMemberID")
    s_member_id_element.send_keys("이곳에 아이디를 적으세요")

    # id가 "SMemberPassword"인 태그를 찾아 비밀번호를 입력합니다.
    s_member_password_element = driver.find_element("id", "SMemberPassword")
    s_member_password_element.send_keys("이곳에 비밀번호를 적으세요")

    # id가 "btnLogin"인 버튼을 찾아 클릭합니다.
    btn_login_element = driver.find_element("id", "btnLogin")
    btn_login_element.click()

    # 시간을 기다립니다. 특정 시간에 실행하도록 설정해주세요.
    target_time = datetime.now().replace(hour=13, minute=40, second=0, microsecond=600)
    current_time = datetime.now()
    while current_time < target_time:
        time.sleep(0.1)
        current_time = datetime.now()

    #JavaScript 코드 실행
    script = """
    const url = 'http://ticket.yes24.com/Pages/Perf/Sale/PerfSaleProcess.aspx?IdPerf=46237';
    const form = $("<form>");
    const target = 'pop_perfsale';

    window.open(url, target, "width=1000,height=700,resizable=yes,toolbar=yes,menubar=yes,location=yes");

    form.attr({
      action: url,
      target: target,
      method: 'post'
    });

    const hiddenField = $("<input>", {
      type: "hidden",
      name: "netfunnel_key",
      value: '=39933EC3387A0E808C27A6052B281E34675B28D1901CB067D2395FFDDB4A47A664813F9747FDBBA628FBC1B2488570F0728AF4FC48B94415858ED65AE4320152F85E4183304A019577928D21AC1B5BCD0126B34E709F725ABC3F566B6A2423E038D03869938F9E7E0349B52349469DA52C312C302C30"
    });

    form.append(hiddenField);
    $("body").append(form);
    form.submit();
    """
    driver.execute_script(script)

    #새창전환
    driver.switch_to.window(driver.window_handles[-1])
    
    #날짜선택
    wait = WebDriverWait(driver, 12000)
    date_element = wait.until(EC.element_to_be_clickable((By.ID, "2023-07-16")))
    date_element.click()

    # id가 "btnSeatSelect"인 요소를 찾아 클릭합니다.
    seat_select_element = wait.until(EC.element_to_be_clickable((By.ID, "btnSeatSelect")))
    seat_select_element.click()

    # name이 "ifrmSeatFrame"인 프레임으로 전환합니다.
    frame_element = wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "ifrmSeatFrame")))

    # id가 "grade_FLOOR"인 p 태그를 찾아 클릭합니다.
    try:
        grade_element = wait.until(EC.element_to_be_clickable((By.ID, "grade_FLOOR")))
        grade_element.click()

        # class가 "seat_layer"인 ul 태그의 자식 li 태그들을 모두 찾습니다.
        seat_layer_element = driver.find_element(By.CLASS_NAME, "seat_layer")
        li_elements = seat_layer_element.find_elements(By.TAG_NAME, "li")

        # 맨 아래 li 태그를 선택하여 클릭합니다.
        last_li_element = li_elements[-2]
        last_li_element.click()

    except NoSuchElementException:
        print("p태그를 찾지 못함")
        time.sleep(1)
    time.sleep(0.2)

    # 특정 RGB 값
    target_rgb = (206, 0, 151) #NCT 지정석은 (85, 41, 221) 플로어(206, 0, 151)

    # 시작점과 끝점 좌표 설정
    start_x = 39
    start_y = 171
    end_x = 747
    end_y = 641

    alert_present = False

    #좌석선택
    find_and_click_random_coordinate(target_rgb, start_x, start_y, end_x, end_y)
    time.sleep(0.2)

    #이선좌 뜨면 다시 좌석 선택
    try:
        alert = driver.switch_to.alert
        alert_present = True
        alert.dismiss()
    except:
        pass

    indexNum = -1
    seatCheck = 1
    while True:
        if alert_present:
            while True:
                # 화면 캡처
                screenshot = pyautogui.screenshot()
                # 회색좌석
                gray_rgb = (255, 255, 255)

                # 좌표 범위 내에서 특정 RGB 값이 있는지 검사
                found_rgb = False
                while True:

                    for x in range(start_x, end_x + 1):
                        for y in range(start_y, end_y + 1):
                            pixel_rgb = screenshot.getpixel((x, y))
                            if pixel_rgb == gray_rgb:
                                found_rgb = True
                                break
                        if found_rgb:
                            break
                    if found_rgb:
                        break

                    if found_rgb == False:
                        if indexNum >= -5 | seatCheck == 0:
                            indexNum = indexNum - 1

                            # class가 "seat_layer"인 ul 태그의 자식 li 태그들을 모두 찾습니다.
                            seat_layer_element = driver.find_element(By.CLASS_NAME, "seat_layer")
                            li_elements = seat_layer_element.find_elements(By.TAG_NAME, "li")

                            # 맨 아래 li 태그를 선택하여 클릭합니다.
                            last_li_element = li_elements[indexNum]
                            last_li_element.click()

                        elif indexNum == -6 & seatCheck != 0:
                            seatCheck = 0;
                            indexNum = indexNum - 1
                            grade_element = wait.until(EC.element_to_be_clickable((By.ID, "grade_지정석")))
                            grade_element.click()

                            # class가 "seat_layer"인 ul 태그의 자식 li 태그들을 모두 찾습니다.
                            seat_layer_element = driver.find_element(By.CLASS_NAME, "seat_layer")
                            li_elements = seat_layer_element.find_elements(By.TAG_NAME, "li")

                            # 맨 아래 li 태그를 선택하여 클릭합니다.
                            last_li_element = li_elements[-1]
                            last_li_element.click()

                if found_rgb :
                    print("좌석선택화면 로딩됨")

                    #FLOOR
                    if seatCheck == 1:
                        target_rgb = (206, 0, 151)
                        find_and_click_random_coordinate(target_rgb, start_x, start_y, end_x, end_y)

                    #지정석
                    elif seatCheck == 0:
                        target_rgb = (85, 41, 221)
                        find_and_click_random_coordinate(target_rgb, start_x, start_y, end_x, end_y)

        else:
            time.sleep(6000)
            break

except NoSuchElementException as e:
    print("요소를 찾을 수 없습니다:", e)

# 사용자 입력을 받고 종료하려면 아무 키나 누르세요.
input("프로그램을 종료하려면 아무 키나 누르세요.")

# 브라우저 창을 종료합니다.
driver.quit()
