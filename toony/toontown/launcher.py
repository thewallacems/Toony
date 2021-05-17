import os
import os.path
import subprocess
import time

from toony import config


def launch(gameserver, playcookie):
    executable = os.path.join(config.get('Toontown', 'Path'), 'Toontown Rewritten')

    if not os.path.exists(executable):
        raise OSError('Toontown Rewritten path not defined or does not exist')

    env = os.environ

    env["TTR_GAMESERVER"] = gameserver
    env["TTR_PLAYCOOKIE"] = playcookie

    os.chdir(os.path.dirname(executable))
    args = f'"{executable}"'
    subprocess.Popen(args=args, shell=True, env=env)
    time.sleep(10)
