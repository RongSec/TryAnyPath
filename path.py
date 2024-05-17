import argparse
import os
import zipfile
import pandas as pd

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def read_zip_files(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        return {name: zip_ref.read(name).decode('utf-8').splitlines() for name in zip_ref.namelist() if name.endswith('.txt')}

def normalize_path(path):
    # Ensure the path starts with a '/'
    return '/' + path if not path.startswith('/') else path

def has_query_params(path):
    # Check if path has query parameters
    return '?' in path

def extract_first_level_dirs(paths):
    first_level_dirs = set()
    for path in paths:
        normalized_path = normalize_path(path)
        parts = normalized_path.split('/')
        if len(parts) > 1:
            dir_candidate = parts[1].split('?')[0]  # Remove query parameters if present
            if not dir_candidate.endswith(('.json', '.txt')):
                first_level_dirs.add(dir_candidate)
    return first_level_dirs

def generate_concatenated_paths(paths, first_level_dirs):
    concatenated_paths = []
    for path in paths:
        for first_level_dir in first_level_dirs:
            if first_level_dir not in path:
                # Split the path to get the subdirectories and filename
                path_parts = path.split('/')[1:]
                # Concatenate the first level directory with the rest of the path
                new_path = f"/{first_level_dir}/{'/'.join(path_parts)}"
                concatenated_paths.append(new_path)
    return concatenated_paths

def main(file_path, zip_path):
    if zip_path:
        data = read_zip_files(zip_path)
        all_paths = []
        for file_name, paths in data.items():
            all_paths.extend(paths)
    else:
        all_paths = read_txt_file(file_path)

    first_level_dirs = extract_first_level_dirs(all_paths)

    # Normalize paths and create data structures for analysis
    all_paths = [normalize_path(p) for p in all_paths]
    concatenated_paths = generate_concatenated_paths(all_paths, first_level_dirs)

    # Create the DataFrames
    df_paths = pd.DataFrame(all_paths, columns=['Path'])
    df_paths['Type'] = 'Original'
    
    df_concatenated = pd.DataFrame(concatenated_paths, columns=['Path'])
    df_concatenated['Type'] = 'Concatenated'
    
    df_first_level_dirs = pd.DataFrame(list(first_level_dirs), columns=['Path'])
    df_first_level_dirs['Type'] = 'First Level Dir'

    # Combine all DataFrames
    combined_df = pd.concat([df_paths, df_concatenated, df_first_level_dirs], ignore_index=True)

    # Create result directory if it does not exist
    result_dir = 'result'
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # Save the combined DataFrame
    combined_file = os.path.join(result_dir, os.path.splitext(os.path.basename(file_path if file_path else zip_path))[0] + '_paths_analysis.csv')
    combined_df.to_csv(combined_file, index=False)

    print(f"Paths analysis saved to: {combined_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process txt or zip files to extract paths and their analysis.')
    parser.add_argument('-f', '--file', help='Path to the txt file', required=False)
    parser.add_argument('-z', '--zip', help='Path to the zip file containing txt files', required=False)

    args = parser.parse_args()

    if not args.file and not args.zip:
        parser.error('One of the following arguments is required: -f/--file or -z/--zip')

    main(args.file, args.zip)
