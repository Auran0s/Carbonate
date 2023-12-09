import yaml

def home_sidebar_menus():
    with open('apps/home/config/home_sidebar_menus.yml') as f:
        menus = yaml.safe_load(f)
    return menus