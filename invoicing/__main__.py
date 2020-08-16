#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from invoicing.command_line import Invoicing


def main():
    try:
        Invoicing()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
