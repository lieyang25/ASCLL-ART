from tkinter import Tk, filedialog
def select_image():

    root = Tk()
    root.withdraw()
    root.tk.call('tk', 'scaling', 1.0)
    file_path = filedialog.askopenfilename(
        title="选择图片文件",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    root.destroy()
    return file_path

def select_video():

    root = Tk()
    root.withdraw()  # 隐藏主窗口
    root.tk.call('tk', 'scaling', 2.0)  # 适配高分辨率显示
    file_path = filedialog.askopenfilename(
        title="选择视频文件",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
    )
    root.destroy()  # 关闭 Tk 窗口
    return file_path