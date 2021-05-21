from threading import Thread

import rumps

from toony import accounts, toontown, config


AppInstance = rumps.App('Toony', title='TTR')


def __make_menu():
    menu = []

    for username, info in accounts.load().items():
        menu_item = __make_account_menu_item(username, info['password'], info['toon'])
        menu.append(menu_item)

    menu_item = rumps.MenuItem(title='Add Account', callback=__add_account_item)
    menu.append(menu_item)

    population = toontown.api.get_population()
    population_title = f'Population: {population}'
    menu_item = rumps.MenuItem(title=population_title)
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
    retries_amount = max(config.get('Toontown', 'LoginRetries'), 1)

    def launch_toontown(retries=retries_amount):
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
    dimensions = config.get('App', 'AskWindowDimensions')
    w, h = dimensions[0], dimensions[1]
    return rumps.Window(message=message, title=title, dimensions=(w, h), cancel='Cancel', secure=secure).run().text


def __update_population(_):
    population_menu_item = next(v for k, v in AppInstance.menu.items() if 'Population' in k)
    population = toontown.api.get_population()
    population_menu_item.title = f'Population: {population}'


__update_population_interval = config.get('App', 'PopulationUpdateInterval', cls=int)
__update_population_timer = rumps.Timer(callback=__update_population, interval=__update_population_interval)
__update_population_timer.start()

AppInstance.menu.update(__make_menu())
