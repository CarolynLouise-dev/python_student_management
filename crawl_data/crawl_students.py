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

    rows = driver.find_elements(By.CSS_SELECTOR, "#studentTable tbody tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 14:
            continue

        student = {
            "mssv": cols[0].text.strip(),
            "last_name": cols[1].text.strip(),
            "first_name": cols[2].text.strip(),
            "math": cols[3].text.strip(),
            "history": cols[4].text.strip(),
            "physics": cols[5].text.strip(),
            "chemistry": cols[6].text.strip(),
            "biology": cols[7].text.strip(),
            "english": cols[8].text.strip(),
            "geography": cols[9].text.strip(),
            "gpa": cols[10].text.strip(),
            "rank": cols[11].text.strip(),
        }

        all_students.append(student)

    try:
        next_page = driver.find_element(
            By.XPATH, f"//button[text()='{current_page + 1}']"
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
            s["mssv"],
            s["last_name"],
            s["first_name"],
            s["math"],
            s["history"],
            s["physics"],
            s["chemistry"],
            s["biology"],
            s["english"],
            s["geography"],
            s["gpa"],
            s["rank"],
        ]) + "\n")