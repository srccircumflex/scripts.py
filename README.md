# scripts.py

![py](https://img.shields.io/badge/python-v3.9-informational)

****

- ### DirHead.py

    - **DirHeader** : os.scandir object as portable format
        ```
        {'DirHead.py': {'st_atime': 1642249269,
                'st_mtime': 1642249147,
                'st_size': 6769,
                'st_uid': 1000},
         'LICENSE': {'st_atime': 1642249496,
                'st_mtime': 1642249491,
                'st_size': 1091,
                'st_uid': 1000},
      'dir/': {'st_atime': 1642251819,
                'st_mtime': 1642251819,
                'st_size': 4096,
                'st_uid': 1000}}
        ```
    - **ConvertDirHeader** : full conversion
        ```
      {'DirHead.py': {'st_atime': '22.01.15-13:21',
                'st_mtime': '22.01.15-13:19',
                'st_size': {'B': 6769, 'G': 0, 'K': 7, 'M': 0},
                'st_uid': '1000'},
      'LICENSE': {'st_atime': '22.01.15-13:24',
                'st_mtime': '22.01.15-13:24',
                'st_size': {'B': 1091, 'G': 0, 'K': 1, 'M': 0},
                'st_uid': '1000'},
      'dir/': {'st_atime': '22.01.15-14:03',
                'st_mtime': '22.01.15-14:03',
                'st_size': {'B': 4096, 'G': 0, 'K': 4, 'M': 0},
                'st_uid': '1000'}}
      ```
    
