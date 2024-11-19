from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from tkinter import Tk, filedialog
import numpy as np

# 细化的 ASCII 字符集，按明暗顺序排列
ASCII_CHARS = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def select_image():
    """弹出文件选择对话框，选择图片文件"""
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    root.tk.call('tk', 'scaling', 2.0)  # 适配高分辨率显示
    file_path = filedialog.askopenfilename(
        title="选择图片文件",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    root.destroy()  # 关闭 Tk 窗口
    return file_path



def resize_image(image, new_width=350):
    """调整图像大小，增加新宽度以提升细节"""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    return image.resize((new_width, new_height))


def enhance_image(image):
    """增强图像的对比度和锐化效果，使ASCII图更清晰"""
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)  # 增强对比度
    sharpener = ImageEnhance.Sharpness(image)
    image = sharpener.enhance(2)  # 增强锐化
    return image


def pixel_to_ascii(pixel, ascii_chars=ASCII_CHARS):
    """根据像素亮度选择合适的 ASCII 字符"""
    r, g, b = pixel[:3]
    grayscale_value = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
    ascii_char = ascii_chars[grayscale_value * len(ascii_chars) // 256]
    return ascii_char, (r, g, b)


def convert_image_to_ascii_image(image_path, new_width=350, output_path="ascii_image.png"):
    # 打开图像并调整大小
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(e)
        return

    image = resize_image(image, new_width)
    image = enhance_image(image)  # 增强图像
    pixels = np.array(image)

    # 提高字符大小，增加字符密度
    char_width = 7
    char_height = 12

    # 创建用于绘制的图片
    ascii_image = Image.new("RGB", (new_width * char_width, len(pixels) * char_height), "white")
    draw = ImageDraw.Draw(ascii_image)

    # 使用等宽字体
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", 10)  # 使用更小的字号以增加细节
    except IOError:
        font = ImageFont.load_default()

    # 绘制 ASCII 图
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            ascii_char, color = pixel_to_ascii(pixel)
            draw.text((x * char_width, y * char_height), ascii_char, fill=color, font=font)

    # 保存生成的 ASCII 图片
    ascii_image.save(output_path)
    print(f"ASCII 图片已保存到 {output_path}")


# 主函数
def main():
    # 选择图片文件
    image_path = select_image()
    if not image_path:
        print("未选择图片文件")
        return

    # 转换图片并保存为 ASCII 图像
    convert_image_to_ascii_image(image_path, new_width=350, output_path="ascii_image.png")


# 运行主函数
if __name__ == "__main__":
    main()
