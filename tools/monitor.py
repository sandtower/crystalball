import os
import subprocess
import sys
import time

def monitor_process(key_word, cmd):
    proc = subprocess.Popen(['ps -ef | grep %r | grep -v grep' % key_word], shell=True, stdout=subprocess.PIPE)
    proc_info_list = proc.communicate()[0].split('\n')
    if len(proc_info_list) > 0 and len(proc_info_list[0]) > 0:
        return

    sys.stderr.write('process[%s] is lost, run [%s]\n' % (key_word, cmd))
    subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)

def main():
    while True:
        cmd = '/home/crystalball/tools/start.sh'
        monitor_process("period_gather", cmd)
        monitor_process("strategy_engine", cmd)
        monitor_process("backtest", cmd)
        time.sleep(10)

if __name__ == "__main__":
    main()
