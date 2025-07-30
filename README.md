
# **Three Box Lottery Data Pipeline**

## 📂 **專案結構**
```
├── data.py        # 資料處理與分析模組
├── download.py    # 爬取最新資料並儲存為 CSV
├── final.py       # 主程式，串接所有流程
├── up_data.py     # 上傳分析結果至 Notion
```

---

## **1. download.py**
**功能：**  
使用 Selenium 爬取 **最新 20 期**的「三星彩」開獎數據，並存成 `Data/Three_Box.csv`。

**流程：**
- 使用 `webdriver_manager` 自動安裝 ChromeDriver。
- 目標網站：[https://www.pilio.idv.tw/lto/list3.asp](https://www.pilio.idv.tw/lto/list3.asp)。
- 擷取資料：
  - **日期**：`td[style*='font-size: 4vmin;']`
  - **號碼**：`td[style*='font-size: 7vmin;']`
- 清理並組合資料 → 轉為 **Pandas DataFrame**。
- 儲存至 `Data/Three_Box.csv`。

**輸出欄位：**
- `日期`
- `百位`
- `十位`
- `個位`

---

## **2. data.py**
**功能：**  
對 CSV 進行分析，回傳以下資訊：
- **最舊日期**與**最新日期**。
- 每個號碼出現次數（字典）。
- 最新三期號碼之間是否有重複數字（布林值）。

**回傳值：**
```python
(oldest_date, latest_date, number_counts_dict, result)
```

**檢查邏輯：**
- 取出最新三期號碼。
- 檢查是否有數字在不同期數間重複。
- `result = True` 表示有重複。

---

## **3. up_data.py**
**功能：**  
將 `data.py` 的結果上傳至 **Notion Database**。

**步驟：**
- 讀取 `.env` 中的：
  - `NOTION_TOKEN`
  - `NOTION_DATABASE_ID`
- 呼叫 **Notion API** 建立 Page。
- 上傳內容：
  - `最舊日期`
  - `最新日期`
  - `{號碼: 出現次數}`
  - `是否有組`（True/False）

**API：**
```
POST https://api.notion.com/v1/pages
```

---

## **4. final.py**
**功能：**  
整合流程，一鍵完成：
1. 爬取資料 → `download.py`
2. 分析數據 → `data.py`
3. 上傳結果 → `up_data.py`

**執行：**
```bash
python final.py
```

---

## ✅ **執行流程圖**
```
download.py  →  data.py  →  up_data.py
      ↓            ↓             ↓
   下載資料      數據分析       上傳Notion
```

---

## **需求套件**
- **核心套件**：
  ```bash
  pip install pandas selenium webdriver-manager python-dotenv requests
  ```

---

## **注意事項**
- 請先建立 `.env` 檔案並設定：
  ```
  NOTION_TOKEN=your_notion_token
  NOTION_DATABASE_ID=your_database_id
  ```
- 確保 `Data` 資料夾存在。
- Windows / MacOS 皆適用。
