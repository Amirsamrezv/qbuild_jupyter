#!/usr/bin/env python3
import codecs
import json
import os
import shutil
import tempfile
import zipfile
from copy import deepcopy
from zipfile import ZipFile

VALID_MODES = ['dir', 'zip']
SOLUTION = 'solution.ipynb'
DUMPER = 'dumper.py'
REQUIRED_FILES = [
    SOLUTION,
    DUMPER,
]

DUMPER_MARKDOWN_CELL = {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
       "پس از ذخیره کردن ادیتور جوپیتر\n",
       "کد زیر را اجرا کنید تا فایل زیپ پاسخ برای شما ساخته شود،\n",
       "سپس فایل زیپ را در سامانه ارسال کنید.\n"
   ]
}

DUMPER_CODE_CELL = {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": []
}


class InvalidMode(Exception):
    pass


class InvalidInitial(Exception):
    pass


def validate_initial_files(initial_dir_files):
    for required_file in REQUIRED_FILES:
        if required_file not in initial_dir_files:
            raise InvalidInitial(f'{required_file} not found in initial.')


def append_dumper_cells_to_quera_solution_json(solution_json, dumper_code_lines):
    # append dumper markdown
    solution_json['cells'].append(DUMPER_MARKDOWN_CELL)

    # append dumper code
    dumper_code_cell = deepcopy(DUMPER_CODE_CELL)
    dumper_code_cell['source'] = dumper_code_lines
    solution_json['cells'].append(dumper_code_cell)

    return solution_json


def rewrite_solution_file_with_dumper_codes(nonquera_solution_path, nonquera_dumper_path):
    with open(nonquera_solution_path, 'r') as solution_file:
        solution_txt = solution_file.read()
    solution_json = json.loads(solution_txt)

    with open(nonquera_dumper_path, 'r') as dumper_file:
        dumper_code_lines = dumper_file.readlines()

    solution_json = append_dumper_cells_to_quera_solution_json(solution_json, dumper_code_lines)

    # write solution
    solution_txt = json.dumps(solution_json, indent=1, ensure_ascii=False)

    with open(nonquera_solution_path, 'w') as solution_file:
        solution_file.write(solution_txt)

    return


def convert_initial_dir_to_nonquera_in_temp_file(initial_dir):

    initial_dir_files = os.listdir(initial_dir)
    validate_initial_files(initial_dir_files)

    # create temp file and archive
    temp_file = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp_file, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(initial_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file == SOLUTION:
                rewrite_solution_file_with_dumper_codes(
                    nonquera_solution_path=file_path,
                    nonquera_dumper_path=os.path.join(initial_dir, DUMPER)
                )

            if file != DUMPER:
                archive.write(file_path, os.path.relpath(file_path, initial_dir))
    archive.close()
    return temp_file


def convert_initial_zip_to_nonquera_in_temp_file(zip_path):
    extract_tmp_directory = tempfile.TemporaryDirectory()
    extract_tmp_path = extract_tmp_directory.name

    # extract zip to temporary directory
    with ZipFile(zip_path, 'r') as zip_obj:
        zip_obj.extractall(extract_tmp_path)

    temp_file = convert_initial_dir_to_nonquera_in_temp_file(initial_dir=extract_tmp_path)
    return temp_file


def convert_initial_dir_to_nonquera_in_path(initial_dir, nonquera_dir=None, challenge_name=None):

    initial_dir_files = os.listdir(initial_dir)
    validate_initial_files(initial_dir_files)

    if not challenge_name:
        challenge_name = os.path.basename(initial_dir)

    if not nonquera_dir:
        nonquera_dir = os.path.dirname(initial_dir)

    if not os.path.exists(nonquera_dir):
        os.makedirs(nonquera_dir)

    nonquera_extract_dir_path = f'{nonquera_dir}/{challenge_name}_nonquera'
    nonquera_extract_zip_path = f'{nonquera_extract_dir_path}.zip'

    if os.path.exists(nonquera_extract_dir_path):
        shutil.rmtree(nonquera_extract_dir_path)

    if os.path.exists(nonquera_extract_zip_path):
        os.remove(nonquera_extract_zip_path)

    # copy all initial files
    os.system(f'cp -r "{initial_dir}" "{nonquera_extract_dir_path}"')

    nonquera_solution_path = f'{nonquera_extract_dir_path}/{SOLUTION}'
    nonquera_dumper_path = f'{nonquera_extract_dir_path}/{DUMPER}'

    rewrite_solution_file_with_dumper_codes(nonquera_solution_path, nonquera_dumper_path)

    # remove nonquera dumper file
    os.remove(nonquera_dumper_path)

    # zip
    shutil.make_archive(nonquera_extract_dir_path, 'zip', nonquera_extract_dir_path)

    return nonquera_extract_dir_path, nonquera_extract_zip_path


def convert_initial_zip_to_nonquera_in_path(zip_path, nonquera_dir=None):
    zip_name = os.path.basename(zip_path)
    challenge_name = '.'.join(zip_name.split('.')[:-1])
    zip_dir = os.path.dirname(zip_path)

    extract_tmp_directory = tempfile.TemporaryDirectory()
    extract_tmp_path = extract_tmp_directory.name

    if not nonquera_dir:
        nonquera_dir = f'{zip_dir}/{challenge_name}_nonquera'

    # extract zip to temporary directory
    with ZipFile(zip_path, 'r') as zip_obj:
        zip_obj.extractall(extract_tmp_path)

    # convert temporary dir
    nonquera_extract_dir_path, nonquera_extract_zip_path = convert_initial_dir_to_nonquera_in_path(
        initial_dir=extract_tmp_path,
        nonquera_dir=nonquera_dir,
        challenge_name=challenge_name
    )

    return nonquera_extract_dir_path, nonquera_extract_zip_path


def convert_initial_to_nonquera_in_temp_file(path, mode):
    if mode not in VALID_MODES:
        raise InvalidMode(f'mode muse be one of {VALID_MODES}')

    temp_file = None
    if mode == 'dir':
        temp_file = convert_initial_dir_to_nonquera_in_temp_file(path)
    elif mode == 'zip':
        temp_file = convert_initial_zip_to_nonquera_in_temp_file(path)

    return temp_file


def convert_initial_to_nonquera_in_path(path, mode, nonquera_dir=None):
    if mode not in VALID_MODES:
        raise InvalidMode(f'mode muse be one of {VALID_MODES}')

    nonquera_extract_dir_path, nonquera_extract_zip_path = None, None

    if mode == 'dir':
        nonquera_extract_dir_path, nonquera_extract_zip_path = convert_initial_dir_to_nonquera_in_path(
            initial_dir=path,
            nonquera_dir=nonquera_dir,
        )

    elif mode == 'zip':
        nonquera_extract_dir_path, nonquera_extract_zip_path = convert_initial_zip_to_nonquera_in_path(
            zip_path=path,
            nonquera_dir=nonquera_dir
        )

    return nonquera_extract_dir_path, nonquera_extract_zip_path
