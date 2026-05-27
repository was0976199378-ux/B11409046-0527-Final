# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11409046
**系級：** 資管系大一  
**姓名：** 鄧羽芯

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| Q1 l1 (in load_proc) | 是一個暫時的變數，用來儲存從檔案 lib_data.txt 中讀取的所有行每一行代表一筆圖書資料，這些資料會被進一步解析並存入全域變|file_lines|
| Q2 d2 (in main) |是一個全域的清單，用來儲存所有圖書的資料,在程式啟動時，load_proc() 函式會從檔案 lib_data.txt 中讀取資料，並將每筆圖書資料解析後存入 d2。 |library_data|
| Q3 c_res (in check) |是一個函式，用來檢查某個 ISBN 是否已經存在於 d2 中。如果找到相符的 ISBN，回傳 True；否則回傳 False。他可以在新增圖書（add 指令）時，避免重複的 ISBN 被加入。 |is_isbn_exist|

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：** 全域變數 d2 的使用:d2 是一個全域變數，負責儲存所有圖書資料，但它的使用範圍不受限制，任何函式都可以直接修改它.會導致程式的可維護性降低，因為它可能在任何地方被意外修改，難以追蹤問題來源。全域變數破壞了函式的封裝性，函式的行為依賴於外部狀態，增加了除錯難度。
- **Q2：** 資料儲存格式不直觀:檔案中的資料格式（@@ 和 ## 分隔符）不直觀且容易出錯。使用者無法直接理解檔案內容，且解析邏輯複雜，容易導致錯誤。
- **Q3：**缺乏錯誤處理:程式中幾乎沒有任何錯誤處理邏輯，例如檔案不存在、資料格式錯誤或輸入無效等情況。如果檔案不存在或內容格式不正確，程式會直接崩潰，導致不良的使用者體驗
- **Q4：**缺乏資料驗證:程式對輸入資料的驗證不足，例如 add 指令中，未檢查書名、ISBN 或狀態是否符合預期格式。使用者可能輸入無效或惡意的資料，導致程式行為異常或資料不一致。
- **Q5：**檔案操作未使用 with 語法:檔案操作（例如 open 和 close）是手動完成的，缺乏自動資源管理。如果程式在檔案操作期間發生例外，檔案可能無法正確關閉，導致資源洩漏。


---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A： 請問在這個檔案中l1, d2, c_res 這三個變數涵義並且加以解釋

Prompt B： 請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好

Prompt C：請幫我重構這段程式碼，提升它的可讀性和維護性。
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？
在說明問題時我發現他的敘述的錯誤跟原程式碼不符。

2. 發現的問題： (範例：AI 漏掉了 exit 時要印出分類統計的功能)
他的分析寫著： 「程式的邏輯全部集中在 main() 函式中，導致函式過於龐大……」
事實上（看原程式碼）： 原程式碼其實已經把一部分邏輯抽離出去了！例如讀取檔案的 load_proc() 和檢查 ISBN 的 c_res(v) 都是獨立在 main() 之外的函式。
3. 修正的對話： (範例：我告訴它「請在結束前迴圈遍歷 JSON 資料並計算分類總額」)
第 5 點的描述不對，原本的程式碼其實已經有 load_proc() 和 c_res() 兩個獨立函式了，並非『全部集中在 main()』。請重新修改第 5 點的問題描述與為什麼不好，改成強調『核心商務邏輯（如 add, show, borrow）仍雜揉在 main 函式的條件分支中』。
---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
PS C:\Users\pclab\Desktop\NTUST-0527-Final-master> python modern_library.py
=== 圖書管理系統 v1.0 (Modern) ===
> add 深入淺出Python/978001/available
成功新增書籍！
> add 資料結構理論/978002/available
成功新增書籍！
> add 演算法實作/978003/available
成功新增書籍！
> add 重複測試書/978001/available
ISBN 已存在，無法新增。
> borrow 978002
成功借出書籍！
> show
書名: 深入淺出Python, ISBN: 978001, 狀態: available
書名: 資料結構理論, ISBN: 978002, 狀態: borrowed
書名: 演算法實作, ISBN: 978003, 狀態: available
> exit
系統資料已儲存，程式結束。
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
  {
        "title": "深入淺出Python",
        "isbn": "978001",
        "status": "available"
    },
    {
        "title": "資料結構理論",
        "isbn": "978002",
        "status": "borrowed"
    },
    {
        "title": "演算法實作",
        "isbn": "978003",
        "status": "available"
    }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
 echo "# NTUST-0527-Final-master" >> README.md
>> git init
>> git add README.md
>> git commit -m "first commit"
>> git branch -M main
>> git remote add origin https://github.com/was0976199378-ux/NTUST-0527-Final-master.git
>> git push -u origin main
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
https://github.com/was0976199378-ux/B11409046-0527-Final
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
