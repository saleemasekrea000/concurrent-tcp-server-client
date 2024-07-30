import os
import socket
import time
import threading
from multiprocessing import Pool, cpu_count
from queue import Queue

SERVER_URL = '127.0.0.1:12345'
CLIENT_BUFFER = 1024
UNSORTED_FILES_COUNT = 100
NUM_THREADS = 10

# following the Producer/consumer model
task_queue = Queue()

def create_directories():
    if not os.path.exists('unsorted_files'):
        os.mkdir('unsorted_files')

    if not os.path.exists('sorted_files'):
        os.mkdir('sorted_files')

def download_unsorted_file():
    while True:
        file_index = task_queue.get()
        if file_index is None:
            break
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            ip, port = SERVER_URL.split(':')
            s.connect((ip, int(port)))
            file = b''
            while True:
                packet = s.recv(CLIENT_BUFFER)
                if not packet:
                    break
                file += packet
            with open(f'unsorted_files/{file_index}.txt', 'wb') as f:
                f.write(file)
        task_queue.task_done()

def download_unsorted_files_multithreaded():
    threads = []
    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=download_unsorted_file)
        threads.append(thread)
        thread.start()
        
    for i in range(UNSORTED_FILES_COUNT):
        task_queue.put(i)
    task_queue.join()
    for _ in range(NUM_THREADS):
        task_queue.put(None)
    for thread in threads:
        thread.join()

def sort_file(file_index):
    with open(f"unsorted_files/{file_index}.txt", "r") as unsorted_file:
        unsorted_list = [int(number) for number in unsorted_file.read().split(',')]
        sorted_list = sorted(unsorted_list)
        with open(f"sorted_files/{file_index}.txt", "w") as sorted_file:
            sorted_file.write(','.join(map(str, sorted_list)))

def sort_files_multiprocessed():
    num_processes = min(cpu_count(), UNSORTED_FILES_COUNT)
    with Pool(processes=num_processes) as pool:
        pool.map(sort_file, range(UNSORTED_FILES_COUNT))

if __name__ == '__main__':
    create_directories()

    tdownload0 = time.monotonic()
    download_unsorted_files_multithreaded()
    tdownload = time.monotonic() - tdownload0
    print(f"Files download time: {tdownload}")

    tsort0 = time.monotonic()
    sort_files_multiprocessed()
    tsort = time.monotonic() - tsort0
    print(f"Sorting time: {tsort}")
