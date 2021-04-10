#!/usr/bin/env python3 
'''
File Observer daemon
'''
import time
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

author = 'Marco Espinosa'
version = '1.0'
email = 'hi@marcoespinosa.com'


class FileObserver:
    '''
    File Observer class
    '''

    # Private variables
    watchDirectory = ""

    def __init__(self, path):
        '''
        Default constructor
        @path: path to watch
        '''

        self.observer = Observer()
        self.watchDirectory = path

    def run(self, recursive=True):
        '''
        Starts watcher
        @recursive: Boolean - Wheather the watcher has to check subdirectories or not
        '''

        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.watchDirectory, recursive=recursive)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    '''
    Handler for file observer events
    '''

    @staticmethod
    def on_any_event(event):
        '''
        Static method to handler filesystem event changes 
        '''
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Event is created, you can process it now
            print(f"Watchdog received created event - {event.src_path}.")

        elif event.event_type == 'deleted':
            # Event is deleted, you can process it now
            print(f"Watchdog received deleted event - {event.src_path}.")

        # TODO: Send events to event-manager docker app

def main():
    '''
    Function main
    '''
    parser = argparse.ArgumentParser(description='File observer')
    parser.add_argument('-p', '--path', help='Path to watch',
                       dest='path', metavar='STRING')

    parser.add_argument('-r', '--recursive', help='Set to True to recursive watch',
                       dest='recursive', metavar='BOOLEAN')

    args = parser.parse_args()

    if args.path is not None and args.recursive is not None:
        watch = FileObserver(args.path)
        watch.run(args.recursive)
    else:
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    main()
