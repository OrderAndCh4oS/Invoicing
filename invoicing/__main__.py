# -*- coding: utf-8 -*-

import sys

from command_line import Invoicing


def main():
    try:
        Invoicing()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
