from sys import argv
import os
import winreg


def check_name_reg(in_key, name, string, list_path):
    if string in name.lower():
        try:
            path = winreg.QueryValueEx(in_key, "InstallLocation")[0]
            if path == '':
                try:
                    path = winreg.QueryValueEx(in_key, "InstallSource")[0]
                    list_path.append(path)
                except WindowsError:
                    pass
            else:
                list_path.append(path)
        except WindowsError:
            pass


def search_in_reg(string: str, list_path: list):
    string = string.lower()
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall") as h_apps:
        for idx in range(winreg.QueryInfoKey(h_apps)[0]):
            try:
                key = winreg.EnumKey(h_apps, idx)
                in_key = winreg.OpenKey(h_apps, key)
                name = winreg.QueryValueEx(in_key, "DisplayName")[0]
                check_name_reg(in_key, name, string, list_path)
            except WindowsError:
                pass


def get_drives():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ['{0}:'.format(d) for d in letters if os.path.exists('{0}:'.format(d))]


def search_folder(path: str, string: str, list_path: list):
    string = string.lower()
    for root, folder, files in os.walk(path):
        last_folder = os.path.basename(os.path.normpath(root))
        if string in last_folder.lower():
            list_path.append(root)


def search(drives, folders, string, list_path):
    for drive in drives:
        for folder in folders:
            path = drive + '/' + folder
            if os.path.isdir(path):
                search_folder(path, string, list_path)


def normalize_path(list_path: list):
    for i in range(len(list_path)):
        list_path[i] = list_path[i].replace('\\', '/')


def print_all_path(list_path: list):
    normalize_path(list_path)
    list_path = set(list_path)
    print(f"Detected {len(list_path)} locations:")
    for path in list_path:
        print(path)


def main():
    list_path = []
    drives = get_drives()
    folders = ("Program Files", "Program Files (x86)")
    script, input_string = argv
    search(drives, folders, input_string, list_path)
    search_in_reg(input_string, list_path)
    print_all_path(list_path)


if __name__ == '__main__':
    main()