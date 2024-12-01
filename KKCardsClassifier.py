import os
import shutil
from dataclasses import dataclass
from typing import Optional
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

# 基本卡片類型 - 按照優先順序排列
CARD_TYPES = [
    "KStudio",            # 優先檢查KStudio
    "KoiKatuCharaSun",    # 接著檢查最特殊的版本
    "KoiKatuCharaSP",     # 再檢查SP版本
    "KoiKatuCharaS",      # 再檢查S版本
    "KoiKatuChara",       # 最後檢查基礎版本
    "KoiKatuClothes",
    # "AIS_Chara",
    # "AIS_Clothes",
    # "AIS_Housing",
    # "AIS_Studio",
    # "RG_Chara",
    # "EroMakeChara",
    # "EroMakeClothes",
    # "EroMakeMap",
    # "EroMakePose",
    # "EroMakeHScene",
    # "HCPChara",
    # "HCPClothes",
    # "HCChara",
    # "HCClothes"
]
TRANSLATIONS = {
    "en": {
        "title": "KK Cards Classifier",
        "select_folder": "Select Folder",
        "start": "Start Classification",
        "language": "Language",
        "processing": "Processing...",
        "done": "Classification Complete!",
        "select_input": "Please select input folder",
        "selected_folder": "Selected folder: {}",
        "processing_file": "Processing file: {}",
        "total_processed": "Total files processed: {}",
        "no_folder": "Please select a folder first!"
    },
    "zh": {
        "title": "KK卡片分類器",
        "select_folder": "選擇資料夾",
        "start": "開始分類",
        "language": "語言",
        "processing": "處理中...",
        "done": "分類完成！",
        "select_input": "請選擇輸入資料夾",
        "selected_folder": "已選擇資料夾: {}",
        "processing_file": "正在處理檔案: {}",
        "total_processed": "共處理檔案數: {}",
        "no_folder": "請先選擇資料夾！"
    }
}

@dataclass
class CardInfo:
    type: str
    has_timeline: Optional[bool] = None
    duration: Optional[float] = None

class CardClassifier:
    def __init__(self, input_folder: str):
        self.input_folder = input_folder
        self.output_folder = os.path.join(input_folder, "classified")

    def has_valid_files(self):
        """Check if there are any .png files in the input folder."""
        for root, _, files in os.walk(self.input_folder):
            if "classified" not in root:
                for file in files:
                    if file.endswith(('.png')):
                        return True
        return False
    def check_card_type(self, file_path: str) -> CardInfo:
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                content_str = content.decode('utf-8', errors='ignore')

            # 先檢查是否為KStudio
            if "KStudio" in content_str:
                card_info = CardInfo(type="KStudio")
                
                # 在這裡完成所有內容檢查
                has_uppercase_timeline = "Timeline" in content_str
                has_lowercase_timeline = "timeline" in content_str
                duration = None

                # 如果有大寫Timeline，檢查duration
                if has_uppercase_timeline:
                    if "duration" in content_str:
                        dur_pos = content_str.find("duration")
                        search_pos = dur_pos + len("duration")
                        
                        while search_pos < len(content_str):
                            if content_str[search_pos].isdigit():
                                num_start = search_pos
                                num_end = num_start
                                while num_end < len(content_str) and (content_str[num_end].isdigit() or content_str[num_end] == '.'):
                                    num_end += 1
                                try:
                                    duration = float(content_str[num_start:num_end])
                                except ValueError:
                                    pass
                                break
                            search_pos += 1

                # 設置timeline類型和duration
                if has_uppercase_timeline:
                    card_info.has_timeline = "dynamic"
                    card_info.duration = duration
                elif has_lowercase_timeline:
                    card_info.has_timeline = "static"
                else:
                    card_info.has_timeline = "none"
                
                return card_info

            # 如果不是KStudio，檢查其他類型
            for base_type in CARD_TYPES[1:]:
                if base_type in content_str:
                    return CardInfo(type=base_type)

            return CardInfo(type="Unknown")

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return CardInfo(type="Unknown")
        


    def classify_files(self, update_progress=None, update_status=None):
        """Classifies files into different categories, including handling non-PNG files."""
        # Create the classified folder
        os.makedirs(self.output_folder, exist_ok=True)

        processed_files = 0
        total_files = 0

        # Calculate total files (both PNG and non-PNG)
        for root, _, files in os.walk(self.input_folder):
            if "classified" not in root:
                total_files += len(files)

        # Process files
        for root, _, files in os.walk(self.input_folder):
            if "classified" not in root:
                for file in files:
                    file_path = os.path.join(root, file)

                    # Update status
                    if update_status:
                        update_status(f"Processing: {file}")

                    # Check if file is a PNG
                    if not file.lower().endswith('.png'):
                        # Handle non-PNG files
                        not_png_dir = os.path.join(self.output_folder, "not_png")
                        os.makedirs(not_png_dir, exist_ok=True)
                        shutil.move(file_path, os.path.join(not_png_dir, file))
                    else:
                        # Process PNG files (example: categorize based on card type)
                        card_info = self.check_card_type(file_path)

                        if card_info.type == "Unknown":
                            target_dir = os.path.join(self.output_folder, "Unknown_cards")
                        else:
                            target_dir = os.path.join(self.output_folder, card_info.type)

                        os.makedirs(target_dir, exist_ok=True)
                        shutil.move(file_path, os.path.join(target_dir, file))

                    # Update progress
                    processed_files += 1
                    if update_progress:
                        update_progress(int(processed_files / total_files * 100))

        # Update status once done
        if update_status:
            update_status("Classification complete!")
        return True



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.input_folder = ""
        self.setup_ui()

    def setup_ui(self):
        self.title("KK Cards Classifier")
        self.geometry("500x200")

        # 移除預設的邊框和填充
        style = ttk.Style()
        style.configure("TFrame", background="white")
        style.configure("TButton", padding=0)
        style.configure("TLabel", background="white")

        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Folder selection
        self.folder_label = ttk.Label(main_frame, text="Selected folder: ")
        self.folder_label.pack(fill="x")
        
        ttk.Button(main_frame, text="Select Folder", 
                  command=self.select_folder).pack(fill="x", pady=(5,10))

        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                      maximum=100)
        self.progress.pack(fill="x", pady=(0,5))
        
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.pack(fill="x")

        # Start button
        self.start_button = ttk.Button(main_frame, text="Start Classification", 
                                     command=self.start_classification)
        self.start_button.pack(pady=(10,0))

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder = folder
            self.folder_label.config(text=f"Selected folder: {folder}")

    def update_progress(self, value):
        self.progress_var.set(value)
        self.update_idletasks()

    def update_status(self, text):
        self.status_label.config(text=text)
        self.update_idletasks()

    def start_classification(self):
        if not self.input_folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return

        self.start_button.config(state="disabled")
        self.progress_var.set(0)
        self.status_label.config(text="Processing...")

        classifier = CardClassifier(self.input_folder)
        
        def classify_thread():
            success = classifier.classify_files(self.update_progress, self.update_status)
            if success:
                self.status_label.config(text="Classification complete!")
                messagebox.showinfo("Complete", "Classification complete!")
            else:
                self.status_label.config(text="No .png files found!")
                messagebox.showinfo("No Files", "No .png files found in the selected folder!")
            self.start_button.config(state="normal")

        thread = threading.Thread(target=classify_thread)
        thread.daemon = True
        thread.start()
def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()