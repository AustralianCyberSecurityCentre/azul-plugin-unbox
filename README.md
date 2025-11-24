# Azul Plugin Unbox

Unbox is a common package and abstraction used by Azul for plugins that handle
archive and compression formats. It is also extended to handle some executable
packing formats like UPX.

It includes a password guessing option for formats that support password protection.
This is seeded from:

- Common known password lists via config
- Password dictionaries supplied in events from upstream plugins/services

## Development Installation

To install azul-plugin-unbox for development run the command
(from the root directory of this project):

Different plugins have their own system requirements for required application/tools.
See: `unbox` install for more information or check out the Dockerfile.

```
# install system dependencies
apt-get install -y --no-install-recommends $(grep -vE "^\s*(#|$)" debian.txt | tr "\n" " ")
# install non apt dependencies
sudo ./install-custom-packages.sh
# install package
pip install -e .
```

## Usage: azul-plugin-unbox

Acts as a multiplugin, it's multiplugins handle the following:

### 7zip

Currently configured to process:

- ZIP (handles more compression modes than alternate zip plugin (AES))
- 7ZIP
- ISO
- Windows Installer

Example Output:

```
----- SevenZip results -----
OK

Output features:
  box_compression: test_dir/test_subdir_file.txt - LZMA:16 7zAES:19
                   test_file_1.txt - LZMA:16 7zAES:19
                   test_file_2.txt - LZMA:16 7zAES:19
     box_password: password
         password: password
   box_insertdate: test_file_1.txt - 2016-07-14 06:08:01
                   test_file_2.txt - 2016-07-14 06:08:22
                   test_dir/test_subdir_file.txt - 2016-07-18 03:37:31
         box_type: sevenzip
        box_count: 3
     box_filepath: test_dir/test_subdir_file.txt
                   test_file_1.txt
                   test_file_2.txt

Generated child entities (3):
  {'action': 'extracted'} <binary: 77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0>
    content: 45 bytes
  {'action': 'extracted'} <binary: 816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b>
    content: 50 bytes
  {'action': 'extracted'} <binary: c6eedc388ac70e3b6962f0626434fd664e2c4a6105cc544d36ab11d006bdd5a0>
    content: 39 bytes

Feature key:
  box_compression:  Compression method used on this file entry
  box_password:  Password used to unbox this binary
  password:  Password used to unbox this binary
  box_insertdate:  Date the file was inserted into the archive
  box_type:  The binary is of this box type
  box_count:  Number of items found in the box
  box_filepath:  This entity contains this filepath
```

### arj

Currently configured to process:

- ARJ
  Supports password protected archives.

Example Output:

```
----- Arj results -----
OK

Output features:
      password: password
     box_count: 3
      box_type: arj
  box_filepath: test_file_1.txt
                test_file_2.txt
                test_subdir_file.txt
  box_password: password

Generated child entities (3):
  {'action': 'extracted'} <binary: 77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0>
    content: 45 bytes
  {'action': 'extracted'} <binary: 816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b>
    content: 50 bytes
  {'action': 'extracted'} <binary: c6eedc388ac70e3b6962f0626434fd664e2c4a6105cc544d36ab11d006bdd5a0>
    content: 39 bytes

Feature key:
  password:  Password used to unbox this binary
  box_count:  Number of items found in the box
  box_type:  The binary is of this box type
  box_filepath:  This entity contains this filepath
  box_password:  Password used to unbox this binary
```

### cabinet

Processes Microsoft Cabinet Format (.CAB) files including self-extracting EXE's.
Currently configured to process:

- CAB

Example Output:

```
----- Cab results -----
OK

Output features:
       box_count: 2
        box_type: cab
    box_filepath: test1.txt
                  test2.txt
  box_insertdate: test2.txt - 2018-03-12 00:40:32
                  test1.txt - 2018-03-12 00:40:36

Generated child entities (2):
  {'action': 'extracted'} <binary: a4df9c5a55aa25e967a45401b3fe6955dccc381403c2574b6ef1ef6a9136e063>
    content: 9 bytes
  {'action': 'extracted'} <binary: 837ea69644a4435aacb379c9b3b14087576d5cbeabe8442a35f592e71d42ca72>
    content: 17 bytes

Feature key:
  box_count:  Number of items found in the box
  box_filepath:  This entity contains this filepath
  box_type:  The binary is of this box type
  box_insertdate:  Date the file was inserted into the archive
```

### chm

Processes Microsoft Compiled HTML Help Files, extracting any embedded files.
Currently configured to process:

- CHM

Example Output:

```
----- CHM results -----
OK

Output features:
      box_type: chm
  box_filepath: /Content/Main.htm
                /Content/Page.htm
                /Project.hhc
                /Project.hhk
                /_#_README_#_
     box_count: 5

Generated child entities (5):
  {'action': 'extracted'} <binary: 348773b69aeb3549b7dca28e899adb488b50c9958e99ab26b494eb02646f3d3b>
    content: 136 bytes
  {'action': 'extracted'} <binary: 5e47de2c21ac971e405fcd0bc54888e080a9e317bd0d1737bcac52c1601f5f92>
    content: 449 bytes
  {'action': 'extracted'} <binary: 83302c10e4838a67ceb39d3f11250251135e56e221701f8eecf5263d6de30577>
    content: 379 bytes
  {'action': 'extracted'} <binary: 5edf10501797afcc8c8612a83f847c1f9f0a5c4eac401cab9a9ffab8e01a76c3>
    content: 109 bytes
  {'action': 'extracted'} <binary: 2f6ea5d512de1d24baac526aa837371e7a1b15c5f3f31edb52f88ded4eba57f5>
    content: 78 bytes

Feature key:
  box_type:  The binary is of this box type
  box_filepath:  This entity contains this filepath
  box_count:  Number of items found in the box
```

### pdf

Processes PDF files, extracting their child streams and handling password decryption.
It utilises the `qpdf` tool to produce a decrypted version of the PDF. Owner passwords
(permission restrictions) are trivially stripped and user passwords guessed based on
supplied password dictionaries.

Currently configured to process:

- PDF

Example Output:

```
----- Pdf results -----
OK

Output features:
               password:
           box_password:
  pdf_object_dictionary: 10 - << /BBox [ -112 420 708 420.1 ] /Filter /FlateDecode /Group << /CS /DeviceRGB /K true /S /Transparency >> /Length 8 /Subtype /Form /Type /XObject >>
                         6 - << /Filter /FlateDecode /Length 236 >>
                         13 - << /Filter /FlateDecode /Length 319 >>
                         14 - << /Filter /FlateDecode /Length 8210 /Length1 12652 >>
               box_type: pdf
              box_count: 5

Generated child entities (4):
  {'action': 'extracted'} <binary: e6b611d975aae6bbee8e87751f94eafb009ca3ac102f549e3249a96a3f91dec3>
    content: 11084 bytes
  {'action': 'extracted', 'object_id': '6', 'filter': 'FlateDecode'} <binary: 0a1d13ef4359b4f9458911df6e3a27639561ef86ad397702e9903f8cde86a6cb>
    content: 411 bytes
  {'action': 'extracted', 'object_id': '13', 'filter': 'FlateDecode'} <binary: 310f2f065725beace3f3b8bb249c5cfcb597d9c491f2e85be79a51ca7fead6e0>
    content: 570 bytes
  {'action': 'extracted', 'object_id': '14', 'filter': 'FlateDecode'} <binary: 1c84e399ca23ff59969af26a938c85aa92490ef38db571d58a845e3c05924617>
    content: 12652 bytes

Feature key:
  password:  Password used to unbox this binary
  box_password:  Password used to unbox this binary
  pdf_object_dictionary:  Object dictionary/id for the extracted PDF stream
  box_type:  The binary is of this box type
  box_count:  Number of items found in the box
```

### rar

Handles extracting files from RAR archive format.
Currently configured to process:

- RAR
  Supports password protected archives.

Example Output:

```
----- Rar results -----
OK

Output features:
  rar_compression: test_file_1.txt - 51
                   test_file_2.txt - 51
         password: password
     box_filepath: test_file_1.txt
                   test_file_2.txt
   box_insertdate: test_file_1.txt - 2016-07-14 16:08:01
                   test_file_2.txt - 2016-07-14 16:08:22
     box_password: password
        box_count: 2
         box_type: rar

Generated child entities (2):
  {'action': 'unrar'} <binary: 77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0>
    content: 45 bytes
  {'action': 'unrar'} <binary: 816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b>
    content: 50 bytes

Feature key:
  rar_compression:  Compression used on the contained file
  password:  Password used to unbox this binary
  box_filepath:  This entity contains this filepath
  box_insertdate:  Date the file was inserted into the archive
  box_password:  Password used to unbox this binary
  box_count:  Number of items found in the box
  box_type:  The binary is of this box type
```

## Usage: azul-unixarchive

This plugin handles unix system archive and compression formats.
Currently configured to process:

- GZIP
- TAR
- BZIP2

Example Output:

```
----- UnixArchive results -----
OK

Output features:
          box_type: archive
      box_filepath: testdir/.testing
                    testdir/test.yaml
                    testdir/README.md
         box_count: 3
  archive_encoding: utf-8

Generated child entities (27):
  {'action': 'extracted'} <binary: 89829064945e65947a902e8b0bb8cb3b58b0d469ac291a62a3058ae9ff266556>
    content: 463 bytes
  {'action': 'extracted'} <binary: 88fbd1ef10e1c27809297180d1ae0960f0b5bf1f52f826566d87bb7c6a408731>
    content: 2183 bytes
  {'action': 'extracted'} <binary: 1c0008dbcd3883f86fc4aa9c53f0cc4a7c5a146e731a58d1a337518d3539d9de>
    content: 275 bytes

Feature key:
  box_count:  Number of items found in the box
  archive_encoding:  Character Encoding used by this archive
  box_type:  The binary is of this box type
  box_filepath:  This entity contains this filepath
```

### upx

Unpacks UPX packed executables for several OSes (Windows, Linux, MacOS).
Currently configured to process:

- Win32 EXE
- Win32 DLL
- DOS EXE
- ELF
- Mach-O

Example Output:

```
----- UPX results -----
OK

Output features:
  upx_version: 3.94
    box_count: 1
     box_type: upx

Generated child entities (1):
  {'action': 'unpacked'} <binary: 38a241ffbc8665eca72bbbd15e1e04d79f745fec7e3c31c3b12c1eaf820abb1c>
    content: 161792 bytes

Feature key:
  box_count:  Number of items found in the box
  box_type:  The binary is of this box type
  upx_version:  Detected upx version used to pack executable
```

Automated usage in system:

```
azul-upx --server http://azul-dispatcher.localnet/
```

### zip

Extracts contents of zip files using python's inbuilt `zipfile` package.
Currently configured to process:

- ZIP
  Supports password protected archives. (more robust than 7zip and handles some files that 7zip won't)

Note: This does not support all possible encryption/compression modes and
as such, it is generally recommended to use 7zip in preference,
which has more comprehensive support.

Example Output:

```
----- Zip results -----
OK

Output features:
         box_type: zip
         password: password
     box_password: password
        box_count: 2
     box_filepath: test_file_1.txt
                   test_file_2.txt
   box_insertdate: test_file_1.txt - 2016-07-14 16:08:02
                   test_file_2.txt - 2016-07-14 16:08:22
  zip_compression: 0

Generated child entities (2):
  {'action': 'unzipped'} <binary: 77f285fd549654a7f9a54ec4dfc7597fcfd66b6622c3b31b60047204f0a213f0>
    content: 45 bytes
  {'action': 'unzipped'} <binary: 816ac3e617f55165dd748c5b6ff16fd05b79bf5104bfd41274635019b239d02b>
    content: 50 bytes

Feature key:
  box_type:  The binary is of this box type
  password:  Password used to unbox this binary
  box_password:  Password used to unbox this binary
  box_count:  Number of items found in the box
  box_filepath:  This entity contains this filepath
  box_insertdate:  Date the file was inserted into the archive
  zip_compression:  Compression used on this zip file
```
## Python Package management

This python package is managed using a `setup.py` and `pyproject.toml` file.

Standardisation of installing and testing the python package is handled through tox.
Tox commands include:

```bash
# Run all standard tox actions
tox
# Run linting only
tox -e style
# Run tests only
tox -e test
```

## Dependency management

Dependencies are managed in the requirements.txt, requirements_test.txt and debian.txt file.

The requirements files are the python package dependencies for normal use and specific ones for tests
(e.g pytest, black, flake8 are test only dependencies).

The debian.txt file manages the debian dependencies that need to be installed on development systems and docker images.

Sometimes the debian.txt file is insufficient and in this case the Dockerfile may need to be modified directly to
install complex dependencies.
