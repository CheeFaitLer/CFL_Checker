import os, winreg, vdf
def find_steam():
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Valve\\Steam")
    value = winreg.QueryValueEx(key, "InstallPath")[0]
    steam_accid_folder = os.listdir(path=f"{value}")
    a = len(steam_accid_folder)
    # for i in range(len(steam_accid_folder)):
    #     print(steam_accid_folder[0])
    #     steam_accid_folder.pop(0)
    return value

find_steam()

def getvdfinfo():
    path = find_steam()
    path = path + '\\config\\loginusers.vdf'
    pat = vdf.load(open(path))
    pat = vdf.loads(vdf_text)
    vdf_text = vdf.dumps(pat)
    indented_vdf = vdf.dump(pat, pretty=True)
    vdf.dump(pat, open('2file.txt', 'w'), pretty=True)
getvdfinfo()