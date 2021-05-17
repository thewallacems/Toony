import os
import os.path
import subprocess
import time
from pathlib import Path

from toony import config


def launch(gameserver, playcookie):
    executable = os.path.join(config.get('Toontown', 'Path'), 'Toontown Rewritten')

    if not os.path.exists(executable):
        guess_path = os.path.join(Path.home(), 'Library/Application Support/Toontown Rewritten')
        if os.path.exists(guess_path):
            config.write('Toontown', 'Path', guess_path)
            executable = guess_path
        else:
            raise OSError('Toontown Rewritten path not defined or does not exist')

    env = os.environ

    env["TTR_GAMESERVER"] = gameserver
    env["TTR_PLAYCOOKIE"] = playcookie

    os.chdir(os.path.dirname(executable))
    args = f'"{executable}"'
    subprocess.Popen(args=args, shell=True, env=env)
    time.sleep(10)
