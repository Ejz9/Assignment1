import os
import shutil

def compress_folder(source_dir, output_file):
    print(f"Compressing {source_dir} into {output_file}.zip...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    shutil.make_archive(output_file, 'zip', source_dir)

if __name__ == "__main__":
    compress_folder('data/mal', 'compressed/mal')
    compress_folder('data/ap', 'compressed/ap')
