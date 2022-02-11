from utils import generate_code, file_name_for_code
from web_requests import download_image_from_code


def main():
    for code in generate_code():
        download_image_from_code(code, file_name_for_code(code))
    return


if __name__ == '__main__':
    main()
