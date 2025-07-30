from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 將下述變成函數
def dow():

    # 設定 Selenium 參數
    options = Options()
    options.add_argument("--headless")  # 無頭模式（不開啟視窗）
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    # 自動下載並啟動 ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # 目標網址
    url = "https://www.pilio.idv.tw/lto/list3.asp"
    driver.get(url)

    # **等待頁面完全加載**
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # **嘗試獲取開獎數據**
    try:
        date_elements = driver.find_elements(By.CSS_SELECTOR, "td[style*='font-size: 4vmin;']")
        number_elements = driver.find_elements(By.CSS_SELECTOR, "td[style*='font-size: 7vmin;']")

        # 檢查是否有抓到數據
        # print(f"日期數量: {len(date_elements)}, 號碼數量: {len(number_elements)}")

        # 確保數據有抓到
        if len(date_elements) == 0 or len(number_elements) == 0:
            print("⚠️ 未抓取到開獎數據，請檢查 XPath 或 CSS Selector")
            driver.quit()
            exit()

        # 抓取數據 (僅保留最近 20 期)
        dates = [date.text.strip().split("\n")[0] for date in date_elements[:20]]  # 去掉換行符與星期
        numbers = [num.text.strip().split(" ..")[0] for num in number_elements[:20]]  # 只取三位數

        # 分割開獎號碼
        split_numbers = [list(num.replace(" ", "")) for num in numbers]  # 去空格並拆分成數字

        # 組合整理後的數據
        results = [(dates[i], split_numbers[i][0], split_numbers[i][1], split_numbers[i][2]) for i in range(len(dates))]

    except Exception as e:
        print(f"❌ 錯誤發生：{e}")
        results = []

    # 關閉瀏覽器
    driver.quit()

    # **檢查 results 是否有數據**
    if not results:
        print("❌ 未獲取到開獎數據，請檢查爬取邏輯")
        exit()

    # **儲存數據**
    df = pd.DataFrame(results, columns=["日期", "百位", "十位", "個位"])

    # **顯示表格**
    print(df)

    # **儲存為 CSV**
    df.to_csv("Data/Three_Box.csv", index=False)

# 執行函數
if __name__ == '__main__':
    dow()