from os import listdir
from os.path import isfile, join

import pjson

test_data_dir_path = "data"

if __name__ == "__main__":
    file_names = [f for f in listdir(
        test_data_dir_path) if isfile(join(test_data_dir_path, f))]

    for file_name in file_names:
        # for file_name in ['y_number_double_close_to_zero.json']:
        if file_name.startswith("y_"):
            file_content = ""
            with open(f"{test_data_dir_path}/{file_name}") as f:
                file_content = f.read()

                try:
                    result = pjson.parse(file_content)
                    # print(result)
                except Exception as e:
                    print(file_name)
                    raise e

        if file_name.startswith("n_"):
            file_content = ""
            with open(f"{test_data_dir_path}/{file_name}") as f:
                result = None
                try:
                    file_content = f.read()
                    result = pjson.parse(file_content)
                except Exception as e:
                    continue

                print(file_name, result)
                break
