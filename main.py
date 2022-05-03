from fhir.resources.bundle import Bundle
import os

MAIN_PATH = os.getcwd()
DATA_PATH = os.path.join(MAIN_PATH, 'data')
os.chdir(DATA_PATH)


def main():
    print(os.listdir(DATA_PATH))
    files_list = os.listdir(DATA_PATH)

    for file in files_list:
        bundle_obj = Bundle.parse_file(file)


if __name__ == '__main__':
    main()
