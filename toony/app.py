from threading import Thread
from typing import Optional

import rumps

from toony import accounts, toontown, config


__POPULATION_KEY: Optional[str] = None

AppInstance = rumps.App('Toony', title='TTR')


def __make_menu():
    global __POPULATION_KEY

    menu = []

    for username, info in accounts.load().items():
        menu_item = __make_account_menu_item(username, info['password'], info['toon'])
        menu.append(menu_item)

    menu_item = rumps.MenuItem(title='Add Account', callback=__add_account_item)
    menu.append(menu_item)

    __POPULATION_KEY = f'Population: {toontown.api.get_population()}'
    menu_item = rumps.MenuItem(title=__POPULATION_KEY)
    menu.append(menu_item)

    return menu


def __make_account_menu_item(username: str, password: str, toon: str):
    menu_item = rumps.MenuItem(title=toon or password)
    login_button = rumps.MenuItem(title='Login', callback=__login)
    login_button.username = username
    login_button.password = password

    delete_button = rumps.MenuItem(title='Delete', callback=__delete_account_item)
    delete_button.username = username

    menu_item.add(login_button)
    menu_item.add(delete_button)

    return menu_item


def __login(sender):
    def launch_toontown(retries=1):
        if retries <= 0:
            return

        try:
            toontown.update()
            gameserver, playcookie = toontown.login(sender.username, sender.password)
            toontown.launch(gameserver, playcookie)
        except OSError:
            ttr_path = __ask('Input the path to your TTR Folder', 'TTR Folder Path Not Defined')
            config.write('Toontown', 'Path', ttr_path)
            launch_toontown(retries=retries-1)

    thread = Thread(target=launch_toontown)
    thread.start()


def __add_account_item(_):
    if not (username := __ask('Input your username', 'Create Account')):
        return

    if accounts.exists(username):
        rumps.alert('Error', 'Account already exists!')
        return

    if not (password := __ask('Input your password', 'Create Account', secure=True)):
        return

    if not (toon := __ask('Input this account\'s main toon', 'Create Account')):
        return

    menu_item = __make_account_menu_item(username, password, toon)
    AppInstance.menu.insert_before('Add Account', menu_item)

    accounts.create(username, password, toon)


def __delete_account_item(sender):
    AppInstance.menu.pop(sender.username)
    accounts.delete(sender.username)


def __ask(message, title, secure=False):
    return rumps.Window(message=message, title=title, dimensions=(160, 80), cancel='Cancel', secure=secure).run().text


def update_population(_):
    global __POPULATION_KEY

    new_population_key = f'Population: {toontown.api.get_population()}'
    AppInstance.menu.get(__POPULATION_KEY).title = new_population_key
    __POPULATION_KEY = new_population_key


update_population_timer = rumps.Timer(callback=update_population, interval=60)
update_population_timer.start()

AppInstance.menu.update(__make_menu())
