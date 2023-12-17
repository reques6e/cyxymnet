import requests
from config import settings
from progress.bar import FillingSquaresBar

headers = {"x-vsaas-api-key": settings.WATCHER_API_KEY, "content-type": "application/json"}

def get_all_orgs():
    orgs = requests.get(url="https://clients.apsny.camera/vsaas/api/v2/organizations?limit=50000", headers=headers).json()
    return [org["id"] for org in orgs]

def get_user_org(user_id):
    orgs = requests.get(url=f"https://clients.apsny.camera/vsaas/api/v2/users/{user_id}", headers = headers).json()['organizations']
    return orgs

def get_folders(org_id):
    folders = requests.get(url=f"https://clients.apsny.camera/vsaas/api/v2/organizations/{org_id}/folders", headers=headers).json()
    return [folder["id"] for folder in folders]

def org_acsess(user_id, org_id, folders):
    url = f"https://clients.apsny.camera/vsaas/api/v2/organizations/{org_id}/users"
    org_permition = {
        "user_id": user_id,
        "can_view_organization_plists": False,
        "can_edit_organization_plists": False,
        "can_edit_organization_users": False,
        "can_edit_organization_cameras": False,
        "can_view_organization_stats": True,
        "folders_permissions": folders,
    }
    return requests.post(url=url, json=org_permition, headers=headers).json()

def folder_acsess(user_id, org_id, folder_id):
    folder_permition = {
        "can_use_actions": True,
        "can_use_ptz": False,
        "can_view_dvr": True,
        "user_id": user_id
    }
    return requests.post(url=f"https://clients.apsny.camera/vsaas/api/v2/organizations/{org_id}/folders/{folder_id}/users", headers=headers, json=folder_permition).json()

if __name__ == "__main__":
    get_user_id = int(input('Введите ID пользователя от которого берем организации:'))
    put_user_id = int(input('Введите ID пользователя которому выдаем доступ:'))
    orgs = get_user_org(get_user_id)
    bar = FillingSquaresBar('Загрузка...', max = len(orgs))
    for org_id in orgs:
        folders = get_folders(org_id)
        org_acsess(put_user_id, org_id, folders)
        for folder_id in folders:
            folder_acsess(put_user_id, org_id, folder_id)
        bar.next()
    print("\n")