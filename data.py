import pandas as pd

def data():

    # 設定 CSV 檔案路徑
    file_path = "Data/three_box.csv"  # 請替換為你的 CSV 檔案路徑

    # 讀取 CSV 文件
    df = pd.read_csv(file_path)

    # 轉換日期欄位為 datetime 格式
    df['日期'] = pd.to_datetime(df['日期'], format='mixed')

    # 找出最舊和最新的日期
    oldest_date = df['日期'].min().strftime("%Y-%m-%d")
    latest_date = df['日期'].max().strftime("%Y-%m-%d")

    # 計算每個號碼在所有列中出現的次數並轉換為字典格式
    number_counts_dict = df[['百位', '十位', '個位']].stack().value_counts().to_dict()

    # 取最新三期數據
    latest_three = df.head(3)

    # 取得各期的數字
    num_1 = latest_three.iloc[0][['百位', '十位', '個位']].tolist()
    num_2 = latest_three.iloc[1][['百位', '十位', '個位']].tolist()
    num_3 = latest_three.iloc[2][['百位', '十位', '個位']].tolist()

    check = {
        "個位_1": num_1[2] in [num_2[0], num_2[1], num_2[2], num_3[0], num_3[1], num_3[2]],
        "十位_1": num_1[1] in [num_2[0], num_2[1], num_2[2], num_3[0], num_3[1], num_3[2]],
        "百位_1": num_1[0] in [num_2[0], num_2[1], num_2[2], num_3[0], num_3[1], num_3[2]],
        "個位_2": num_2[2] in [num_3[0], num_3[1], num_3[2]],
        "十位_2": num_2[1] in [num_3[0], num_3[1], num_3[2]],
        "百位_2": num_2[0] in [num_3[0], num_3[1], num_3[2]]
    }

    # 檢查是否有 TRUE 存在
    result = any(check.values())
    # print(result)

    return oldest_date, latest_date, number_counts_dict, result

# 執行函數
if __name__ == "__main__":
    data()