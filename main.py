from utils import generate_code, file_name_for_code
from web_requests import download_image_from_code, wait_x_seconds_rand


def main():
    for code in generate_code():
        download_image_from_code(code, file_name_for_code(code))
        wait_x_seconds_rand(1)
    return


if __name__ == '__main__':
    main()
