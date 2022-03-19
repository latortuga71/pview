#!/usr/local/bin/python3

import subprocess
from collections import namedtuple
import sys

Process = namedtuple("Process", "name pid started command")

def check_if_exists(p,plist):
    if p.command == "ps aux":
        return True
    for proc in plist:
        if proc.command == p.command and p.pid == proc.pid:
            return True
    return False

class ProcSnapshot():
    def __init__(self) -> None:
        self.tmp_snapshots = []
        self.original_snapshots = self.take_snapshot()

    def take_snapshot(self):
        snapshots = []
        ps = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE)
        original_snapshot = [x.strip() for x in ps.stdout.decode("utf-8").split("\n")]
        for proc in original_snapshot:
            try:
                proc_split = proc.split()
                if not proc_split:
                    continue
                user = proc_split[0]
                pid = proc_split[1]
                ptime = proc_split[8]
                cmd = " ".join(proc_split[10:])
                p = Process(user,pid,ptime,cmd)
                print(p)
                if p not in snapshots:
                    snapshots.append(p)
            except IndexError as e:
                print(proc_split,file=sys.stderr)
                print(e,file=sys.stderr)
        return snapshots

    def show_processes(self):
        for p in self.original_snapshots:
            print(p)

    def monitor_new_procs(self):
        tmp = []
        ps = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE)
        tmp_snapshot = [x.strip() for x in ps.stdout.decode("utf-8").split("\n")]
        for proc in tmp_snapshot:
            try:
                proc_split = proc.split()
                if not proc_split:
                    continue
                user = proc_split[0]
                pid = proc_split[1]
                ptime = proc_split[8]
                cmd = " ".join(proc_split[10:])
                p = Process(user,pid,ptime,cmd)
                if not check_if_exists(p,self.original_snapshots):
                    self.original_snapshots.append(p)
                    print(p)
            except IndexError as e:
                print(proc_split,file=sys.stderr)
                print(e,file=sys.stderr)
                



if __name__ == "__main__":
    original_snapshot = ProcSnapshot()
    while (True):
        original_snapshot.monitor_new_procs()


