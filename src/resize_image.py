def resize_image(image, new_with=350):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_with * aspect_ratio * 0.55)
    return image.resize((new_with,new_height))