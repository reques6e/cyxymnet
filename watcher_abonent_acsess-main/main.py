import requests
from config import settings

headers = {"x-vsaas-api-key": settings.WATCHER_API_KEY, "content-type": "application/json"}

def correcte_address(address):
    correted_address = address.split('.')[-1] # Отбрасываем все кроме адреса
    correted_address=correted_address.lower().strip().replace(', ',' ') # Подгоняем строку к виду как в watcher
    return correted_address

def get_folders(org_id):
    folders = requests.get(url=f"https://clients.apsny.camera/vsaas/api/v2/organizations/{org_id}/folders", headers=headers).json()
    return [folder["id"] for folder in folders]

def get_searched_org_id(searched_address):
    address = correcte_address(searched_address)
    orgs = requests.get(url=f"https://clients.apsny.camera/vsaas/api/v2/domains/1/organizations?search={address}&limit=2000&offset=0&sort=", headers=headers).json()
    selected_address_id = str()
    for org in orgs:
        org_address = correcte_address(org['title'])
        if org_address == address:
            selected_address_id = org['id']
            break;
    return selected_address_id
    
def make_acsess(org_id, user_login, password, user_name):
    data = {
        "login": user_login,
        "password": password,
        "organization_id": org_id,
        "phone":password,
        "name": user_name,
        "note":password,
        "max_sessions":2,
    }
    user_id = requests.post(url=f"https://clients.apsny.camera/vsaas/api/v2/users?trace=sql", headers=headers, json=data).json()['id']
    
    folders = get_folders(org_id)
    org_permition = { "user_id": user_id, "can_view_organization_stats": True, "folders_permissions": folders}
    requests.post(url=f"https://clients.apsny.camera/vsaas/api/v2/organizations/{org_id}/users", json=org_permition, headers=headers).json()
    
    for folder_id in folders:
        folder_permition = { "can_use_actions": True, "can_view_dvr": True, "user_id": user_id}
        requests.post(url=f"https://clients.apsny.camera/vsaas/api/v2/organizations/{org_id}/folders/{folder_id}/users", headers=headers, json=folder_permition).json()

if __name__ == "__main__":
    user_info={'name':'Хасбула Хаджиме','login':'50228228','address':'г. Сухум, ул. Аргун, 15','phone':'79402282228'}
    org_id = get_searched_org_id(user_info['address'])
    make_acsess(org_id, user_info['login'], user_info['phone'], user_info['name'])