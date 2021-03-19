import re
import os
import shutil
import argparse
import subprocess

FOLDER_PATH = None

def get_cliparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_folder', default=os.environ.get('SOURCE_FOLDER_PATH'))
    parser.add_argument('--dest_folder', default=os.environ.get('DEST_FOLDER_PATH'))
    return parser


def get_folder_files(absolute_path):
    files = []
    folders = []

    for filename in os.listdir(absolute_path):
        absolute_filename = f'{absolute_path}/{filename}'

        data = {
            'absolute_filename':absolute_filename,
            'filename':filename,
            'relative_path': absolute_path.replace(FOLDER_PATH, '')
        }

        if os.path.isfile(absolute_filename):
            files.append(data)
        if os.path.isdir(absolute_filename):
            folders.append(data)

    return folders, files

def render(src, dest):
    args = ['pandoc', '-f', 'markdown', '-t', 'html5',  '-o', dest, src]
    print(' '.join(args))
    subprocess.run(args, check=True)

if __name__ == '__main__':
    parser = get_cliparser()
    args = parser.parse_args()
    FOLDER_PATH = args.source_folder

    shutil.rmtree(args.dest_folder)
    os.mkdir(args.dest_folder)

    for dirpath, dirnames, filenames in os.walk(args.source_folder):
        dirdest = dirpath.replace(args.source_folder, args.dest_folder)
        for dirname in dirnames:
            os.mkdir(f"{dirdest}/{dirname}")
        
        for filename in filenames:
            render(f"{dirpath}/{filename}",f"{dirdest}/{filename.replace('.md', '.html')}")
        









