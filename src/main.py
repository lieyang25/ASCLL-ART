from select_file import select_image
def main():

    image_path = select_image()
    if not image_path:
        return
    output_path = select_path()
    create_image_to_Acsll(image_path)

if __name__ == '__main__':
    main()