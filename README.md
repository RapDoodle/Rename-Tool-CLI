# Rename Tool CLI
Rename multiple files according to user-defined criteria in command line

## Examples
Here are some examples. For detailed usage, please read the next section. Note: For Windows users, replace `python3` in the examples with `python`.

1. Rename all files only to contain index numbers (with regular expression). For example, rename `3C7A2474.JPG` to `002.JPG` where `002` is the second file in the folder.
    ```bash
    $ python3 rename.py --path /home/my_folder --match ".*" --use-regex --enumerate
    ```

1. Rename all `foo` to `bar` (without regular expression). For example, rename `image_foo.jpg` to `image_bar.jpg`.
    ```bash
    $ python3 rename.py --path /home/my_folder --match "foo" --replace "bar" 
    ```

1. Rename all `JPG` and `CR3` files in the folder to names starting with `IMG` and ends (not including extension) with enumeration. Then, store all files in another folder. For example, copy `3C7A2474.JPG` from `my_folder`, and store it in `my_folder_2` as `IMG (01).JPG`.
    ```bash
    $ python3 rename.py --path /home/my_folder --match ".*" --use-regex --replace "IMG" --enumerate --enumerate-style 4 --format-filter JPG,CR3 --dst /home/my_folder_2
    ```
    
    Note: 

        1. Values in `format-filter` are case insensitive. The search will include `JPG`, `jpg`, `CR3`, and `cr3`.

        2. `enumerate-style` is predefined. Please read the next section for more information.

## Usage

### Command help
```
usage: rename.py [-h] -p DIR [-d DIR] [-m STRING] [--include-extensions]
                 [--use-regex] [--ignore-case] [-f STRING] [-r STRING] [-e]
                 [--enumerate-from INT] [--enumerate-style INT] [--no-confirm]

optional arguments:
  -h, --help            show this help message and exit
  -p DIR, --path DIR    source path
  -d DIR, --dst DIR     destination path (optional)
  -m STRING, --match STRING
                        the filename to be matched
  --include-extensions  include file extensions for matching and replacing
  --use-regex           use regular expression for matching
  --ignore-case         ignore case
  -f STRING, --format-filter STRING
                        case insensitive formats separated by comma (,)
  -r STRING, --replace STRING
                        replaced string
  -e, --enumerate       enumerate items
  --enumerate-from INT  starting number of enumeration (default: 1)
  --enumerate-style INT
                        enumerate style
  --no-confirm          no confirmation before renaming
```

### Enumeration options

- Style
    The program supports six predefined enumeration suffix templates. By default, template `1` is used. To specify another style, use `--enumerate-style <style-id>`.

    1. No bracket (without space)
        `IMG.jpg` to `IMG01.jpg`

    2. No bracket (with space)
        `IMG.jpg` to `IMG 01.jpg`

    3. Bracket (without space)
        `IMG.jpg` to `IMG(01).jpg`

    4. Bracket (with space)
        `IMG.jpg` to `IMG (01).jpg`

    5. Square bracket (without space)
        `IMG.jpg` to `IMG[01].jpg`

    6. Square bracket (with space)
        `IMG.jpg` to `IMG [01].jpg`

- Starting index
    The program supports enumeration starting from any index. By default, `1` is used. To change the starting index, use `--enumerate-from <INT>`.

    For example, to start from `0`, add `--enumerate-from 0`.

### Other options

- Ignore confirmation

    By default, the program will prompt users for confirmation, showing the files' old and new name, source folder, and destination folder (in any), before proceeding. The user may opt for ignoring the confirmation by specifying `--no-confirm`.

# License
This program is licensed under the Apache-2.0 License. You may use the software for any purpose, to distribute it, to modify it, and to distribute modified versions of the software under the terms of the license, without concern for royalties.