from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Process, Manager
from tabulate import tabulate
from config import *

import subprocess
import shutil
import psutil
import time
import math
import sys
import os

no_test_passed = 0
no_success = [0] * 4
max_duration = [0] * 4
accumulated_duration = [0] * 4
peak_memory_usage = [0] * 4
program_tasks = ["Generating input", "Running brute", "Running solution", "Comparing outputs"]

def bold(text): return f"\033[1m{text}\033[0m"

def yellow(text): return f"\033[33m{bold(text)}\033[0m"
def green(text): return f"\033[32m{bold(text)}\033[0m"
def red(text): return f"\033[31m{bold(text)}\033[0m"
def magenta(text): return f"\033[95m{bold(text)}\033[0m"

def compile_program(source, old, des, log):
    if os.path.exists(source) and os.path.exists(old) and os.path.exists(f'{BINARY_PATH}/{des}'):
        with open(source, 'r') as f1, open(old, 'r') as f2:
            if f1.read() == f2.read():
                print("- Compiling", yellow(source), magenta('- SKIPPED'))
                return
            
    shutil.copyfile(source, old)
    start = time.time()
    crr = time.time()
    no = 0
    
    with open(log, 'w') as f:
        proc = subprocess.Popen(f'g++ {ARGUMENTS} {source} -o {BINARY_PATH}/{des}', stderr=f)
        
        while (proc.poll() == None):
            end = time.time()
            duration = end - crr

            if duration > TERMINAL_UPDATE_TIME:  
                crr = time.time()
                no += 1
                print("- Compiling", yellow(source), '.' * no)
                no = no % 3
                print("\033[1A\033[2K", end='')

        end = time.time()
        duration = end - start

        if proc.returncode == 0:
            print("- Compiling", yellow(source), green('✔ SUCCESS'), f'({duration:.3f}s)')
        else:
            print("- Compiling", yellow(source), red('✖ FAILED'), f'({duration:.3f}s)')
            sys.exit(f'\n{red('ERROR')} Compilation for {yellow(source)} failed (see {yellow(log)} for details)')

def run_program(path, program_index, in_path, out_path, timelimit, memorylimit, test_dir, test_no, queue, stop_event):
    if stop_event.is_set():
        return
    
    start = time.time()
    peak_mem = 0.0

    with open(in_path, 'r') as in_file, open(out_path, 'w') as out_file:
        proc = subprocess.Popen(path, stdin=in_file, stdout=out_file, stderr=subprocess.DEVNULL)
        ps_proc = psutil.Process(proc.pid)

        while (proc.poll() == None):            
            end = time.time()
            elapsed = end - start

            try:
                mem = ps_proc.memory_full_info()
                peak_mem = max(peak_mem, mem.peak_wset / (1024 * 1024))
            except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                pass 

            if peak_mem > memorylimit:
                proc.kill()
                raise Exception(f'\n{red(f'✖ TEST {test_no}')} Failed to execute {yellow(path)} {magenta('MEMORY LIMIT EXCEEDED')} (>{memorylimit}MB) (see {yellow(test_dir)} for test details)')

            if elapsed > timelimit:
                proc.kill()
                raise Exception(f'\n{red(f'✖ TEST {test_no}')} Failed to execute {yellow(path)} {magenta('TIME LIMIT EXCEEDED')} (>{timelimit}s) (see {yellow(test_dir)} for test details)')
        
        if proc.returncode != 0:
            raise Exception(f'\n{red(f'✖ TEST {test_no}')} Failed to execute {yellow(path)} {magenta('RUNTIME ERROR')} (exit code {proc.returncode}) (see {yellow(test_dir)} for test details)')

    queue.put([program_index, end - start, peak_mem])

def clear_folder(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def trim_content(path):
    result_lines = []
    hidden_lines = 0

    with open(path, 'r') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            if i < MAX_LINES:
                if len(line) > MAX_LINE_LENGTH:
                    line = line[:MAX_LINE_LENGTH - 3] + "..."
                result_lines.append(line)
            else:
                hidden_lines += 1

    if hidden_lines > 0:
        result_lines.append("(...)")
        result_lines.append(f"({hidden_lines} more hidden line(s))")

    return "\n".join(result_lines)

def run_test(i, queue, test_queue, stop_event):
    if stop_event.is_set():
        return
    
    test_dir = OUTPUT_PATH + f'/test{i + 1}'
    os.makedirs(test_dir)
    test_queue.put(test_dir)

    test_in = test_dir + '/input.txt'
    brute_out = test_dir + '/output_brute.txt'
    sol_out = test_dir + '/output_solution.txt'
    checker_out = test_dir + '/checker.txt'
    
    if test_queue.qsize() > MAX_STORED_TESTS and MAX_STORED_TESTS > 0:
        shutil.rmtree(test_queue.get())

    run_program(BINARY_PATH + '/gen.exe', 0, LOG_PATH + '/empty.txt', test_in, GENERATOR_TIMELIMIT, GENERATOR_MEMORYLIMIT, test_dir, i + 1, queue, stop_event)
    run_program(BINARY_PATH + '/brute.exe', 1, test_in, brute_out, BRUTE_TIMELIMIT, BRUTE_MEMORYLIMIT, test_dir, i + 1, queue, stop_event)
    run_program(BINARY_PATH + '/sol.exe', 2, test_in, sol_out, SOLUTION_TIMELIMIT, SOLUTION_MEMORYLIMIT, test_dir, i + 1, queue, stop_event)
    run_program([BINARY_PATH + '/checker.exe', sol_out, brute_out], 3, LOG_PATH + '/empty.txt', checker_out, CHECKER_TIMELIMIT, CHECKER_MEMORYLIMIT, test_dir, i + 1, queue, stop_event)

    if stop_event.is_set():
        return

    checker_message = ''
    with open(checker_out, 'r') as f:
        checker_message = f.read()
    
    diff_path = LOG_PATH + '/diff.txt'
    diff_input = trim_content(test_in)
    diff_sol = trim_content(sol_out)
    diff_brute = trim_content(brute_out)

    if checker_message != '':
        if os.stat(diff_path).st_size == 0:
            with open(diff_path, 'w') as f:
                f.write('Input:\n')
                f.writelines(diff_input)

                f.write('\n\nYour output:\n')
                f.writelines(diff_sol)

                f.write('\n\nBrute output:\n')
                f.writelines(diff_brute)

                f.write('\n\nChecker message:\n')
                f.write(checker_message)
        
        os.startfile(os.path.abspath(diff_path))
        raise Exception(f'\n{red(f'✖ TEST {i + 1} | {checker_message}')} (see {yellow(test_dir)} for test details)')

    queue.put([-1, -1, -1])

def log(clear):
    if clear == True:
        for _ in range(10):
            print("\033[1A", end='\r')

    headers = ['Task', 'Passed', 'Progress', 'Max Time', 'Average Time', 'Max Memory']
    rows = []

    for i in range(4):
        rows.append([program_tasks[i], 
                     green(f'{no_success[i]}/{MAX_TESTS}') if MAX_TESTS > 0 else green(f'{no_success[i]}/∞'), 
                     green(f'{math.floor(no_success[i] / MAX_TESTS * 100)}%') if MAX_TESTS > 0 else 'NaN',
                     magenta(f'{max_duration[i]:.3f}s'),
                     magenta(f'{(accumulated_duration[i] / max(no_success[i], 1)):.3f}s'),
                     yellow(f'{peak_memory_usage[i]:.3f} MB')])
    
    print()
    print(tabulate(rows, headers=headers, tablefmt="outline", colalign=("left", "center", "center", "center", "center", "center")))
    print()
        
def log_listener(queue, test_queue, stop_event):
    try:
        while True:
            msg = queue.get()
            if msg == "__DONE__" or stop_event.is_set():
                break

            elapsed = msg[1]
            index = msg[0]
            peak_mem = msg[2]

            if index != -1:
                no_success[index] += 1
                max_duration[index] = max(max_duration[index], elapsed)
                peak_memory_usage[index] = max(peak_memory_usage[index], peak_mem)
                accumulated_duration[index] += elapsed
            else:
                global no_test_passed
                no_test_passed += 1
            log(True)
    except KeyboardInterrupt:
        stop_event.set() 
        print(red('Keyboard interupt!!'))
        print(red('Terminating tasks... Do not close the terminal!'))

def main():
    print('\033[?25l', end='')  
    compile_program(SOLUTION_PATH, OLD_PATH + '/sol.cpp', 'sol.exe', LOG_PATH + '/sol_compile.txt')
    compile_program(BRUTE_PATH, OLD_PATH + '/brute.cpp', 'brute.exe', LOG_PATH + '/brute_compile.txt')
    compile_program(GENERATOR_PATH, OLD_PATH + '/gen.cpp', 'gen.exe', LOG_PATH + '/gen_compile.txt')
    compile_program(CHECKER_PATH, OLD_PATH + '/checker.cpp', 'checker.exe', LOG_PATH + '/checker_compile.txt')

    clear_folder(OUTPUT_PATH)
    open(LOG_PATH + '/diff.txt', 'w').close()
    open(LOG_PATH + '/empty.txt', 'w').close()

    manager = Manager()
    queue = manager.Queue()
    test_queue = manager.Queue()
    stop_event = manager.Event()
    start = time.time()

    listener = Process(target=log_listener, args=(queue, test_queue, stop_event))
    listener.start()
    log(False)
    
    all_passed = True
    try:
        with ProcessPoolExecutor(max_workers=MAX_PARALLEL_PROCESSES) as executor:
            futures = set()
            test_id = 0
            while test_id < MAX_TESTS or MAX_TESTS == 0:
                futures.add(executor.submit(run_test, test_id, queue, test_queue, stop_event))
                test_id += 1

                if len(futures) >= 2 * MAX_PARALLEL_PROCESSES or (MAX_TESTS > 0 and test_id >= MAX_TESTS):
                    done, futures = as_completed(futures), set()
                    for f in done:
                        try:
                            f.result()
                        except Exception as e:
                            print(e)
                            print(red('Terminating tasks... Do not close the terminal!'))
                            stop_event.set() 
                            all_passed = False
                            break
                    if not all_passed:
                        break
                    
    except KeyboardInterrupt:
        stop_event.set() 

        all_passed = False
        for pending in futures:
            pending.cancel()

    queue.put("__DONE__")
    listener.join()
    
    if all_passed:
        print(green(f'✔ All tests passed! ({(time.time() - start):.3f}s)'))
    print('\033[?25h', end='')

if __name__ == "__main__": 
    main()