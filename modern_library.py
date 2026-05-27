import os
import json

# filepath: c:\Users\pclab\Desktop\NTUST-0527-Final-master\modern_library.py

class Library:
    def __init__(self, file_name="library_data.json"):
        self.file_name = file_name
        self.library_data = []
        self.load_data()

    def load_data(self):
        """從 JSON 檔案載入圖書資料"""
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as f:
                    self.library_data = json.load(f)
            except json.JSONDecodeError:
                print("檔案格式錯誤，無法載入資料。")
                self.library_data = []
        else:
            print("檔案不存在，將建立新檔案。")
            self.library_data = []

    def save_data(self):
        """將圖書資料儲存到 JSON 檔案"""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(self.library_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"儲存資料時發生錯誤：{e}")

    def add_book(self, title, isbn, status="available"):
        """新增一本書到圖書館"""
        if self.is_isbn_exist(isbn):
            print("ISBN 已存在，無法新增。")
            return
        self.library_data.append({"title": title, "isbn": isbn, "status": status})
        print("成功新增書籍！")

    def is_isbn_exist(self, isbn):
        """檢查 ISBN 是否已存在"""
        return any(book["isbn"] == isbn for book in self.library_data)

    def show_books(self):
        """顯示所有書籍"""
        if not self.library_data:
            print("目前沒有任何書籍資料。")
            return
        for book in self.library_data:
            print(f"書名: {book['title']}, ISBN: {book['isbn']}, 狀態: {book['status']}")

    def borrow_book(self, isbn):
        """借書，將書籍狀態設為 borrowed"""
        for book in self.library_data:
            if book["isbn"] == isbn:
                if book["status"] == "borrowed":
                    print("此書已被借出。")
                else:
                    book["status"] = "borrowed"
                    print("成功借出書籍！")
                return
        print("找不到對應的 ISBN 書籍。")

    def exit_system(self):
        """儲存資料並退出系統"""
        self.save_data()
        print("系統資料已儲存，程式結束。")


def main():
    library = Library()
    print("=== 圖書管理系統 v1.0 (Modern) ===")

    while True:
        op = input("> ").strip()

        if op == "exit":
            library.exit_system()
            break

        elif op.startswith("add "):
            try:
                raw = op[4:].split("/")
                if len(raw) == 3:
                    title, isbn, status = raw
                    library.add_book(title, isbn, status)
                else:
                    print("格式錯誤！正確格式：add 書名/ISBN/狀態")
            except Exception as e:
                print(f"新增書籍時發生錯誤：{e}")

        elif op == "show":
            library.show_books()

        elif op.startswith("borrow "):
            isbn = op[7:]
            library.borrow_book(isbn)

        else:
            print("未知指令，請重新輸入。")


if __name__ == "__main__":
    main()