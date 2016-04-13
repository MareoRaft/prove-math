# watchdog imports
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# helper imports
import re
import subprocess

###Comment to be deleted.

class BabelEventHandler (FileSystemEventHandler):


    def on_created(self, event):
        print('A file or directory has been created.')
        return self.on_created_or_modified(event)

    def on_modified(self, event):
        print('A file or directory has been modified.')
        return self.on_created_or_modified(event)

    def on_created_or_modified(self, event):
        print('The event is: "' + str(event) + '".')
        if re.search(r'\.js$', event.src_path):
            print('Found a new or modified js file.  Attempting to find paths and then run babel...')
            in_path = event.src_path
            print('in_path is ' + in_path)
            out_path = re.sub(r'scripts6/', 'scripts/', in_path)
            print('out_path is ' + out_path)
            try:
                print(subprocess.check_output('babel ' + str(in_path) + ' > ' + str(out_path), shell=True))
                print('success.')
            except Exception as e:
                print(e)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = BabelEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
