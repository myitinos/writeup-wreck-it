#! /usr/bin/env python3
# from subprocess import Popen, PIPE
# import subprocess
# import string
# import multiprocessing
# import itertools

from subprocess import Popen, PIPE
from string import ascii_letters, digits
from multiprocessing import Pool, Value
from ctypes import c_bool

# possible chars
chars = ascii_letters + digits + "_"

# r3tURnFroMc0r3bO0ooT
flag = ''

# shared memory
found = Value(c_bool)


def brute(payload: str):
    global found

    # check apabila sudah ditemukan
    if found.value:
        return None

    # bruteforce
    with Popen(["qemu-system-i386",
                "-bios", "1ot.bin",
                "-serial", "stdio",
                "-display", "none"], stdout=PIPE, stdin=PIPE) as p:
        # encode payload ke byte array
        payload_encoded = payload.encode('utf8') + b"\r"

        # read 11 bytes
        p.stdout.read(11)

        # input ke perangkat
        bytes_wrote = p.stdin.write(payload_encoded)
        p.stdin.flush()

        # ambil hasil
        correct = p.stdout.read(bytes_wrote + 5)[-1] == ord('B')

        # matikan process
        p.terminate()

    # set shared memory ke true apabila benar
    if correct:
        found.value = True

    return correct


while True:
    # set found ke false
    found.value = False

    # buat possible flag untuk di brute
    possible_flags = [flag + c for c in chars]

    # bruteforce dengan multiprocessing
    with Pool() as pool:
        result = pool.map(brute, possible_flags)

    try:
        # cari index dari possible flag yang benar
        index = result.index(True)

        # ganti flag dengan possible flag yang benar
        flag = possible_flags[index]
    except ValueError:
        # break ketika tidak ada possible flag yang benar
        break

print("wreck{" + flag + "}")
