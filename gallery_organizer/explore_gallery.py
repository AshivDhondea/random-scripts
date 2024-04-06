from typing import List
import argparse
import json
import os


FILE_TYPES: List[str] = ['.json', '.txt', '.png', '.jpeg']

if __name__ == '__main__':
    # Argument parsing
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", help="input path", type=str, required=True)
    ap.add_argument("-o", "--output", help="output path", type=str, required=True)
    ap.add_argument("-f", "--filetype", help="File type", type=str, required=True, choices=FILE_TYPES)

    args = ap.parse_args()
    input_path = args.input
    output_path = args.output
    file_type = args.filetype.lower()

    # Args checking
    if not os.path.isdir(input_path):
        input_path_error = f"{input_path} is not a valid directory"
        raise NotADirectoryError(input_path_error)

    if not os.path.isdir(output_path):
        output_path_error = f"{output_path} is not a valid directory."
        raise NotADirectoryError(output_path_error)

    # Get all file paths.
    files: List[str] = [f for f in os.listdir(input_path) if f.endswith(file_type)]
    if not files:
        fnf_error = f"No files of type {file_type} found in {input_path}"
        raise FileNotFoundError(fnf_error)

    date_dict = dict()
    rejected_files = list()

    for f in files:
        split_file_name = f.split('_')
        if len(split_file_name[0]) != 10:
            rejected_files.append(os.path.join(input_path, f))
            continue

        if split_file_name[0].count('-') == 2:
            year_month_split = split_file_name[0].split('-')
            year = year_month_split[0]
            month = year_month_split[1]
            date_dict[year] = date_dict.get(year, dict())
            date_dict[year][month] = date_dict.get(year).get(month, [])
            date_dict[year][month].append(f)

    # Save the gallery dictionary as a json file.
    json_path = os.path.join(output_path, 'gallery_record.json')
    with open(json_path, 'w') as f:
        json.dump(date_dict, f, indent=4)

    # Keep a record of rejected files.
    rejected_file_path = os.path.join(output_path, 'rejected_files.txt')
    with open(rejected_file_path, 'w') as f:
        for rejected in rejected_files:
            f.write(f"{rejected}\n")

    print(f"Job completed on {input_path}")
