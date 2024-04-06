from typing import List, Union
import argparse
import json
import os


if __name__ == '__main__':
    # Argument parsing
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", help="input gallery JSON path", type=str, required=True)
    ap.add_argument("-o", "--output", help="output file name", type=str, required=True)
    ap.add_argument("-y", "--year", help="year to filter by", nargs="+", type=str, required=True)
    ap.add_argument("-m", "--month", help="month to filter by", nargs="+", type=str, required=False)

    args = ap.parse_args()
    input_path = args.input
    output_file_name = args.output
    year: List[str] = args.year
    month: Union[List[str], None] = args.month

    # Args checking
    if not os.path.isfile(input_path):
        input_path_error = f"{input_path} is not a valid file path."
        raise FileNotFoundError(input_path_error)

    split_path = os.path.split(input_path)
    file_name = split_path[1].lower()
    if not file_name.endswith('.json'):
        vnf_err = f'{file_name} is not a valid JSON file.'
        raise ValueError(vnf_err)

    output_file_name.lower()
    if not output_file_name.endswith('.txt'):
        ovnf_err = f"{output_file_name} should be a txt file."
        raise ValueError(ovnf_err)

    # Load gallery record JSON
    with open(input_path) as f:
        gallery_dict = json.load(f)

    process_list = list()
    for y in year:
        if y not in gallery_dict.keys():
            ynf_err = f"Year {y} does not appear in the gallery."
            raise ValueError(ynf_err)

        year_dict = gallery_dict[y]
        for year_key, year_value in year_dict.items():
            # year_key means month in year y, year_value is a list corresponding to this month.
            if month is None:
                print(f"Adding files for all months in year {y}")
                process_list.extend(year_value)
            elif year_key in month:
                print(f"Adding files for month {year_key} in year {y}")
                process_list.extend(year_value)

    # Save a txt file of files to process.
    with open(os.path.join(split_path[0], output_file_name), 'w') as f:
        for p in process_list:
            f.write(f"{p}\n")
