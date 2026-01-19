from playwright.sync_api import sync_playwright
from lxml import html

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://example.com", wait_until="networkidle")
    page.wait_for_selector("#studentTable tr")  # wait for JS table

    content = page.content()
    browser.close()

tree = html.fromstring(content)

rows = tree.xpath('//tbody[@id="studentTable"]/tr')
print(len(rows))

# rows =tree.xpath('//tbody[@id="studentTable"]/tr')
#
# students =[]
#
# for row in rows:
#     cols = row.xpath ('./td')
#     student= {
#         "mssv": cols[0].text_content().strip() if len(cols) > 0 else None,
#         "ho": cols[1].text_content().strip() if len(cols) > 1 else None,
#         "ten": cols[2].text_content().strip() if len(cols) > 2 else None,
#         "email": cols[3].text_content().strip() if len(cols) > 3 else None,
#         "ngay_sinh": cols[4].text_content().strip() if len(cols) > 4 else None,
#         "que_quan": cols[5].text_content().strip() if len(cols) > 5 else None,
#         "diem_toan": cols[6].text_content().strip() if len(cols) > 6 else None,
#         "diem_van": cols[7].text_content().strip() if len(cols) > 7 else None,
#         "diem_anh": cols[8].text_content().strip() if len(cols) > 8 else None,
#         "diem_tb": cols[9].text_content().strip() if len(cols) > 9 else None,
#         "xep_loai": cols[10].text_content().strip() if len(cols) > 10 else None,
#
#
#     }
#
#     students.append(student)
#
# print(f"🎉 Crawl xong {len(students)} sinh viên")
# # save in raw_data_student.txt
# with open("raw_data_student.txt", "w", encoding="utf-8") as f:
#     for s in students:
#         f.write("|".join([
#             s["mssv"] or "",
#             s["ho"] or "",
#             s["ten"] or "",
#             s["email"] or "",
#             s["ngay_sinh"] or "",
#             s["que_quan"] or "",
#             s["diem_toan"] or "",
#             s["diem_van"] or "",
#             s["diem_anh"] or "",
#             s["diem_tb"] or "",
#             s["xep_loai"] or "",
#         ]) + "\n")