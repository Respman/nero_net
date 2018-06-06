#!/usr/bin/env python3.6

import subprocess
import threading
import psutil
# python3.6 -m pip install psutil


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def subproc(i, t):
    while True:
        # print(f"{i} started!")
        paste = "exec " + f"python3.6 nero_net_v2.py studying {i}"
        proc = subprocess.Popen(paste, stdout=open("/dev/null", "r+b"),
                                shell=True)
        try:
            proc.wait(timeout=t)
        except subprocess.TimeoutExpired:
            kill(proc.pid)
            print(f"{i} killed!")
            continue
        else:
            print(f">>> {i} finished!")
            continue
    return 0


def main():
    thread_pool = list()
    for i in range(1, 5):
        # i*0.1 - граница веса
        thread_pool.append(threading.Thread(target=subproc, args=(i, 5*10)))
        # 20 - время жизни до ямы
        thread_pool[-1].start()
        print(f"Thread {i} started!")
    for i in thread_pool:
        i.join()


if __name__ == "__main__":
    main()
