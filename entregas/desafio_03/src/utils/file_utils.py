def unzip_files(zip_file_path, extract_to):
    import zipfile
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def load_csv(file_path):
    import pandas as pd
    return pd.read_csv(file_path)