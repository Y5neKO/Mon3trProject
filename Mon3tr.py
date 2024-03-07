import signal
import sys

from core.banner import banner
from core.console import *


def signal_handler(signal, frame):
    print('收到 Ctrl+C，停止程序...')
    sys.exit(0)


def run():
    print(banner)
    main()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    run()
