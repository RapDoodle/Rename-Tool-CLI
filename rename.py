import os
import re
import shutil
import argparse


def format_check(filename: str, allowed_formats: list):
    """Check whether the extension is allowed."""
    return filename.lower().endswith(allowed_formats)


def file_parts(filepath: str):
    """Separate the filename and file extension from file path"""
    f_sep = filepath.rsplit('.', 1)
    f_name = f_sep[0]
    f_ext = f_sep[1] if len(f_sep) > 1 else ''
    return f_name, f_ext


def y_n_choice(msg = 'Do you want to continue?'):
    choice = input(msg + ' [Y/n] ')
    return True if (choice == 'Y' or choice == 'y' or choice == '') else False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', 
        '--path', 
        metavar='DIR', 
        required=True, 
        help='source path')
    parser.add_argument(
        '-d', 
        '--dst', 
        metavar='DIR', 
        required=False, 
        default=None, 
        help='destination path (optional)')
    parser.add_argument(
        '-m', 
        '--match', 
        metavar='STRING', 
        required=False, 
        default=None,
        help='the filename to be matched')
    parser.add_argument(
        '--include-extensions', 
        action='store_true',
        default=False, 
        help='include file extensions for matching and replacing')
    parser.add_argument(
        '--use-regex', 
        action='store_true',
        default=False, 
        help='use regular expression for matching')
    parser.add_argument(
        '--ignore-case', 
        action='store_true',
        default=False, 
        help='ignore case')
    parser.add_argument(
        '-f', 
        '--format-filter', 
        metavar='STRING', 
        required=False,
        default=None,
        help='case insensitive formats separated by comma (,)')
    parser.add_argument(
        '-r', 
        '--replace', 
        metavar='STRING', 
        required=False,
        default='',
        help='replaced string')
    parser.add_argument(
        '-e', 
        '--enumerate', 
        action='store_true',
        help='enumerate items')
    parser.add_argument(
        '--enumerate-from', 
        metavar='INT', 
        required=False,
        default=1, 
        type=int, 
        help='starting number of enumeration (default: 1)')
    parser.add_argument(
        '--enumerate-style', 
        choices=[1, 2, 3, 4, 5, 6], 
        metavar='INT', 
        required=False,
        default=1, 
        type=int, 
        help='enumerate style')
    parser.add_argument(
        '--no-confirm', 
        action='store_true',
        default=False, 
        help='no confirmation before renaming')
    args = parser.parse_args()

    filenames = os.listdir(args.path)
    filenames.sort()

    # Filter by file formats
    if args.format_filter is not None:
        allowed_formats = (*args.format_filter.lower().split(','), )
        filenames = list(filter(lambda x: format_check(x, allowed_formats), filenames))

    # Default arguments
    if args.match is None:
        args.match = '.*'
        args.use_regex = True

    # Not really used in this stage. Used in future developments
    mappings = {}

    # Get the rename mapping
    for idx, filename in enumerate(filenames):
        new_name = filename

        (f_name, f_ext) = file_parts(filename)

        if not args.include_extensions:
            new_name = f_name

        # Option: ignore case
        re_flags = 0
        if args.ignore_case:
            re_flags = re.IGNORECASE

        # Compile regex
        if args.use_regex:
            regex = re.compile(args.match, flags=re_flags)
        else:
            regex = re.compile(re.escape(args.match), flags=re_flags)
        
        # Replace with pattern
        if regex.search(new_name) is not None:
            new_name = regex.sub(args.replace, new_name)
        else:
            continue
        
        # Add the file extension back
        if not args.include_extensions:
            new_name += '.' + f_ext

        mappings[filename] = {
            'new_name': new_name,
        }
    
    num_match = len(mappings)
    if num_match == 0:
        print('No matching files found.')
        exit()

    # Add item count
    if args.enumerate:
        num_digits = len(str(len(filenames)))
        enum_count = args.enumerate_from
        for filename, info in mappings.items():
            # Add index number
            (f_name, f_ext) = file_parts(info['new_name'])

            # Enumerate styles
            if args.enumerate_style == 1:
                f_name += str(enum_count).zfill(num_digits)
            elif args.enumerate_style == 2:
                f_name += ' ' + str(enum_count).zfill(num_digits)
            elif args.enumerate_style == 3:
                f_name += '(' + str(enum_count).zfill(num_digits) + ')'
            elif args.enumerate_style == 4:
                f_name += ' (' + str(enum_count).zfill(num_digits) + ')'
            elif args.enumerate_style == 5:
                f_name += '[' + str(enum_count).zfill(num_digits) + ']'
            elif args.enumerate_style == 6:
                f_name += ' [' + str(enum_count).zfill(num_digits) + ']'
            new_name = f"{f_name}.{f_ext}"

            mappings[filename]['new_name'] = new_name
            enum_count = enum_count + 1


    # Confirm with users
    if not args.no_confirm:
        print('The following files are about to be renamed:')
        for filename, file_info in mappings.items():
            print(f"{filename} -> {file_info['new_name']}")
        print(f'There are {num_match} files in {os.path.abspath(args.path)} to be processed.')
        if args.dst is not None:
            print(f'The renamed files will be saved in {os.path.abspath(args.dst)}')
        if not y_n_choice():
            exit()

    # Create destination folder is not exists
    if args.dst is not None and not os.path.exists(args.dst):
        os.mkdir(args.dst)

    # Copy or rename the file
    idx = 1
    for filename, info in mappings.items():
        # Progress info
        print(f"Processing {idx}/{num_match}", end='\r')
        
        src_path = os.path.join(args.path, filename)
        if args.dst is not None:
            # Copy the files
            shutil.copyfile(
                src_path,
                os.path.join(args.dst, info['new_name']))
        else:
            # Rename the files
            os.rename(src_path, os.path.join(args.path, info['new_name']))

        idx = idx + 1
    
    print('\nDone.')