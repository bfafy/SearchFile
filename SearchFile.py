import os
import chardet
from tkinter import filedialog, messagebox, ttk, simpledialog
import tkinter as tk
import threading

# 创建窗口
window = tk.Tk()

# 设置窗口标题
window.title("查找文件")

# 创建“选择文件夹”按钮回调函数
def on_select_folder():
    folder_path.set(filedialog.askdirectory())

# 创建“查找”按钮回调函数
def on_search():
    target_text = search_text.get()
    result_text.delete('1.0', tk.END)  # 清空结果框
    for root, dirs, files in os.walk(folder_path.get()):  #遍历指定文件夹
        for file_name in files:
            _, file_ext = os.path.splitext(file_name)
            if file_ext in allowed_file_extensions:
                file_path = os.path.join(root, file_name)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # 将文件大小转换为MB
                if file_size <= max_file_size_mb:
                    # 使用线程读取文件内容
                    t = threading.Thread(target=read_file, args=(file_path, target_text))
                    t.start()

# 读取文件内容的函数
def read_file(file_path, target_text):
    with open(file_path, "rb") as f:
        content = f.read()
        encoding = chardet.detect(content)['encoding']
    try:
        with open(file_path, "r", encoding=encoding, errors="replace") as f:
            file_content = f.read()
            if target_text in file_content:
                result_text.insert(tk.END, file_path + "\n")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

# 创建“清除记录”按钮回调函数
def on_clear():
    result_text.delete('1.0', tk.END)  # 清空结果框

# 创建输入框和相关变量
search_text = tk.StringVar(value="")
search_label = tk.Label(window, text="查找内容：")
search_label.pack()
search_entry = tk.Entry(window, textvariable=search_text)
search_entry.pack()

# 创建“选择文件夹”按钮和相关变量
folder_path = tk.StringVar(value="")
select_folder_button = tk.Button(window, text="选择文件夹", command=on_select_folder)
select_folder_button.pack()
folder_label = tk.Label(window, textvariable=folder_path)
folder_label.pack()

# 创建“可选文件类型”复选框和相关变量
file_types_frame = ttk.Frame(window)
file_types_frame.pack(fill=tk.X, padx=5, pady=5)

allowed_file_extensions = [".txt", ".js", ".html"]  # 可选文件类型

file_types_label = tk.Label(file_types_frame, text="可选文件类型：")
file_types_label.pack(side=tk.LEFT)

file_type_variables = {}

for ext in allowed_file_extensions:
    var = tk.BooleanVar(value=False)  # 默认取消选择状态
    file_type_variables[ext] = var
    cb = ttk.Checkbutton(file_types_frame, text=ext, variable=var, command=lambda: update_allowed_file_extensions())
    cb.pack(side=tk.LEFT, padx=2)

def update_allowed_file_extensions():
    global allowed_file_extensions
    allowed_file_extensions.clear()
    for ext, var in file_type_variables.items():
        if var.get():
            allowed_file_extensions.append(ext)
    for ext in custom_file_extensions:
        if ext not in allowed_file_extensions:
            allowed_file_extensions.append(ext)

# 创建“添加文件类型”按钮和相关函数
custom_file_extensions = []  # 自定义文件类型

def add_custom_file_extension():
    new_ext = simpledialog.askstring("添加文件类型", "请输入需要添加的文件类型（如 .pdf）")
    if new_ext and new_ext[0] == "." and new_ext not in allowed_file_extensions:
        custom_file_extensions.append(new_ext)
        var = tk.BooleanVar(value=False)  # 默认取消选择状态
        file_type_variables[new_ext] = var
        cb = ttk.Checkbutton(file_types_frame, text=new_ext, variable=var, command=lambda: update_allowed_file_extensions())
        cb.pack(side=tk.LEFT, padx=2)

add_custom_extension_button = tk.Button(window, text="添加文件类型", command=add_custom_file_extension)
add_custom_extension_button.pack()

# 创建“最大文件大小”输入框和相关变量
max_file_size_mb = 5  # 最大文件大小（MB）
max_file_size_var = tk.StringVar(value=str(max_file_size_mb))
max_file_size_label = tk.Label(window, text="最大文件大小（MB）：")
max_file_size_label.pack()
max_file_size_entry = tk.Entry(window, textvariable=max_file_size_var)
max_file_size_entry.pack()

# 创建“查找”按钮
search_button = tk.Button(window, text="查找", command=on_search)
search_button.pack()

# 创建“清除记录”按钮
clear_button = tk.Button(window, text="清除记录", command=on_clear)
clear_button.pack()

# 创建结果框
result_text = tk.Text(window)
result_text.pack()

# 进入消息循环
window.mainloop()
