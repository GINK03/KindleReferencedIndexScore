from __future__ import print_function
import sys
import os


if __name__ == '__main__':
    with open('./stash/idf_base.txt', 'r') as file:
        for line in file.read().split('\n'):
            print(line)

