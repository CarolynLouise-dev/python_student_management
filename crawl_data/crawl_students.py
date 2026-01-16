from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--incognito")

driver = webdriver.Chrome(options=options)
driver.set_window_size(800, 1000)

driver.get("http://127.0.0.1:5500/")
time.sleep(2)

all_students = []
current_page = 1

while True:
    print(f"📄 Đang crawl trang {current_page}")

    time.sleep(1)

    rows = driver.find_elements(By.CSS_SELECTOR, "#studentTable tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        student = {
            "mssv": cols[0].text.strip() or None,
            "ho": cols[1].text.strip() or None,
            "ten": cols[2].text.strip() or None,
            "email": cols[3].text.strip() or None,
            "ngay_sinh": cols[4].text.strip() or None,
            "que_quan": cols[5].text.strip() or None,
            "diem_toan": cols[6].text.strip() or None,
            "diem_van": cols[7].text.strip() or None,
            "diem_anh": cols[8].text.strip() or None,
            "diem_tb": cols[9].text.strip() or None,
            "xep_loai": cols[10].text.strip() or None,
        }
        all_students.append(student)

    try:
        next_page = driver.find_element(
            By.XPATH,
            f"//button[text()='{current_page + 1}']"
        )
        next_page.click()
        current_page += 1
        time.sleep(1)
    except NoSuchElementException:
        print("✅ Hết trang")
        break

driver.quit()

print(f"🎉 Crawl xong {len(all_students)} sinh viên")
with open("students.txt", "w", encoding="utf-8") as f:
    for s in all_students:
        f.write("|".join([
            s["mssv"] or "",
            s["ho"] or "",
            s["ten"] or "",
            s["email"] or "",
            s["ngay_sinh"] or "",
            s["que_quan"] or "",
            s["diem_toan"] or "",
            s["diem_van"] or "",
            s["diem_anh"] or "",
            s["diem_tb"] or "",
            s["xep_loai"] or "",
        ]) + "\n")
