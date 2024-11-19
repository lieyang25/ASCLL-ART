from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from moviepy.editor import VideoFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import numpy as np
from tkinter import Tk, filedialog
from tqdm import tqdm
import sys

# ASCII 字符集
ASCII_CHARS = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def select_file():
    """弹出文件选择对话框，选择视频文件"""
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    root.tk.call('tk', 'scaling', 2.0)  # 适配高分辨率显示
    file_path = filedialog.askopenfilename(
        title="选择视频文件",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
    )
    root.destroy()  # 关闭 Tk 窗口
    return file_path


def resize_image(image, new_width=120):
    """调整图像大小"""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    return image.resize((new_width, new_height))


def enhance_image(image):
    """增强图像的对比度和锐化效果"""
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    sharpener = ImageEnhance.Sharpness(image)
    image = sharpener.enhance(2)
    return image


def pixel_to_ascii(pixel, ascii_chars=ASCII_CHARS):
    """将像素转换为 ASCII 字符"""
    r, g, b = pixel[:3]
    grayscale_value = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
    ascii_char = ascii_chars[grayscale_value * len(ascii_chars) // 256]
    return ascii_char, (r, g, b)


def convert_frame_to_ascii(frame, new_width=120):
    """将一帧转换为 ASCII 图像"""
    frame_image = Image.fromarray(frame)
    frame_image = resize_image(frame_image, new_width)
    frame_image = enhance_image(frame_image)
    pixels = np.array(frame_image)

    char_width, char_height = 6, 10
    ascii_image = Image.new("RGB", (new_width * char_width, len(pixels) * char_height), "white")
    draw = ImageDraw.Draw(ascii_image)

    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", 10)
    except IOError:
        font = ImageFont.load_default()

    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            ascii_char, color = pixel_to_ascii(pixel)
            draw.text((x * char_width, y * char_height), ascii_char, fill=color, font=font)

    return ascii_image


def video_to_ascii(input_video_path, output_video_path, fps=10):
    """将视频转换为 ASCII 视频"""
    try:
        clip = VideoFileClip(input_video_path)
        frames = []

        # 使用 tqdm 展示进度条
        for frame in tqdm(clip.iter_frames(fps=fps, dtype="uint8"), total=clip.reader.nframes,
                          desc="Processing frames"):
            ascii_frame = convert_frame_to_ascii(frame)
            frames.append(np.array(ascii_frame))

        # 将 ASCII 帧列表转换为视频
        ascii_clip = ImageSequenceClip(frames, fps=fps)
        ascii_clip.write_videofile(output_video_path, codec="libx264")
    except Exception as e:
        print(f"转换过程中发生错误: {e}")
        sys.exit(1)


# 主函数
def main():
    try:
        input_video_path = select_file()
        if not input_video_path:
            print("未选择视频文件")
            return

        output_video_path = "ascii_video.mp4"  # ASCII 视频输出路径
        video_to_ascii(input_video_path, output_video_path, fps=10)
        print(f"ASCII 视频已保存到 {output_video_path}")

    except KeyboardInterrupt:
        print("程序已被用户终止")
        sys.exit(0)

    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)


# 运行主函数
if __name__ == "__main__":
    main()
