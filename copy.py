import sys
import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from watchdog.observers.polling import PollingObserverVFS  
from watchdog.events import PatternMatchingEventHandler 

class MyHandler(PatternMatchingEventHandler):
    #patterns = ["*.*", ".*"]

    def __init__(self, target_dir,  source_path, **kwargs):
        PatternMatchingEventHandler.__init__(self, **kwargs)
        self._target_dir = target_dir
        self.source_path = source_path

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        if not event.is_directory:
            print('{} {} --> {}'.format(event.src_path,
                                        event.event_type,
                                        self._target_dir))
            files = self.find_files(self.source_path)
            self.copy_files(files,  self._target_dir)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


    def find_files(self,  catalog):
        find_files = []
        for root, dirs, files in os.walk(catalog):
            find_files += [os.path.join(root, name) for name in files]
        return find_files
    
    def copy_files(self,  files,  dist_path):
        for file in files:
            dist = dist_path + datetime.today().isoformat('T') .replace(':','_') + Path(file).suffix
            free_space = shutil.disk_usage(dist_path).free
            print (2 * os.stat(file).st_size)
            if free_space < 2 * os.stat(file).st_size:
               print("Недостаточно памяти!") 
               sys.exit(1)
            shutil.copyfile(file, dist, follow_symlinks=True)
            os.remove(file)
            print(dist)


def find_files(catalog):
    find_files = []
    for root, dirs, files in os.walk(catalog):
        find_files += [os.path.join(root, name) for name in files]
    return find_files
    
def copy_files(files,  dist_path):
    for file in files:
        dist = dist_path + datetime.today().isoformat('T') .replace('.','_') + Path(file).suffix
        free_space = shutil.disk_usage(dist_path).free
        if free_space < 2 * os.stat(file).st_size:
            print("Недостаточно памяти!") 
            sys.exit(1)
        shutil.copyfile(file, dist, follow_symlinks=True)
        os.remove(file)
        print(dist)
  
if __name__ == "__main__":
    if len (sys.argv) < 3:
        print ("Ошибка. Слишком мало параметров.")
        sys.exit (1)

    if len (sys.argv) > 3:
        print ("Ошибка. Слишком много параметров.")
        sys.exit (1)

    source_path = sys.argv[1]
    dist_path = sys.argv[2] 
    
    files = find_files(source_path)
    copy_files(files,  dist_path)
    
    observer = PollingObserverVFS(stat=os.stat, listdir=os.listdir, polling_interval=30)
    observer.schedule(MyHandler(dist_path, source_path, patterns=['*.*','*','.*']),
                      path=source_path)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


