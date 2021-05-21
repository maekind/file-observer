#!/usr/bin/env python3
# encoding:utf-8
'''
File Observer daemon
'''
import time
import argparse
import requests
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
from requests.exceptions import RequestException
from lib.logger import Logger


__author__ = 'Marco Espinosa'
__version__ = '1.0'
__email__ = 'hi@marcoespinosa.com'


class FileObserver:
    '''
    File Observer class
    '''

    # Private variables
    watch_directory = ""
    address = ""
    port = 0

    def __init__(self, logger, path, address="", port=0):
        '''
        Default constructor
        @path: path to watch
        '''

        self.observer = Observer()
        self.watch_directory = path
        self.address = address
        self.port = port
        self.logger = logger

    def run(self, recursive=True):
        '''
        Starts watcher
        @recursive: Boolean - Wheather the watcher has to check subdirectories or not
        '''

        event_handler = Handler()

        # If webservice enabled, we set host and port variables
        if self.address != "" and self.port != 0:
            event_handler.set_address(self.address)
            event_handler.set_port(self.port)

        self.observer.schedule(
            event_handler, self.watch_directory, recursive=recursive)
        self.observer.start()

        try:
            while True:
                # Execution every 5 seconds
                time.sleep(5)
        except:
            self.observer.stop()
            self.logger.info("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    '''
    Handler for file observer events
    '''
    address = ""
    port = 0
    logger = None

    @staticmethod
    def set_logger(logger):
        '''
        Function to set logger
        '''
        Handler.logger = logger

    @staticmethod
    def set_address(value):
        '''
        Setter for host variable
        '''
        Handler.address = value

    @staticmethod
    def set_port(value):
        '''
        Setter for port variable
        '''
        Handler.port = value

    @staticmethod
    def on_any_event(event):
        '''
        Static method to handler filesystem event changes
        '''
        if event.is_directory:
            return None

        if event.event_type in ['created', 'deleted']:
            Handler.logger.info(
                f"Watchdog received {event.event_type} event - {event.src_path}.")
            Handler.__send_event(event.event_type, event.src_path)

    @staticmethod
    def __send_event(event, payload):
        '''
        Send event to webservice
        '''
        if Handler.address != "" and Handler.port != 0:
            Handler.logger.info(
                f"Sending {event} with {payload} to webservice")

            try:
                req = requests.get(
                    f'{Handler.address}:{Handler.port}/{event}/{payload}')
            except RequestException:
                Handler.logger.error('Request ERROR.')
                return

            if req.status_code == 200:
                Handler.logger.info('OK')
            else:
                Handler.logger.error(f'Request ERROR: {req.status_code}')


def exit_fail(parser):
    '''
    Exit program with errors
    '''
    parser.print_help()
    exit(1)


def main():
    '''
    Function main
    '''
    # Configure logger
    logger = Logger("File-observer")

    # Get arguments
    parser = argparse.ArgumentParser(description='File observer')
    parser.add_argument('-p', '--path', help='Path to watch',
                        dest='path', metavar='STRING')

    parser.add_argument('-r', '--recursive', help='Set to True to recursive watch',
                        dest='recursive', metavar='BOOLEAN')

    parser.add_argument('-e', '--enable-webservice',
                        help='Set to True to send events to webservice',
                        dest='enablewebservice', metavar='BOOLEAN')

    parser.add_argument('-a', '--address',
                        help='''Webservice host address or FQDN.
                            Mandatory if enable-webservice set to True''',
                        dest='address', metavar='STRING')

    parser.add_argument('-o', '--port',
                        help='Webservice port. Mandatory if enable-webservice set to True',
                        dest='port', metavar='INT')

    args = parser.parse_args()

    # Check for arguments
    if args.path is not None and args.recursive is not None:

        address = ""
        port = 0

        if args.enablewebservice is not None:
            # If enablewebservice, host and port have to be provided
            if args.enablewebservice is True and (args.address is None or args.port is not None):
                exit_fail(parser)
            else:
                address = args.address
                port = args.port
        # Creation of FileObserver instance
        logger.info(f'Monitoring changes in {args.path}')
        logger.info(f'Send events to {address}:{port}')

        watch = FileObserver(logger, args.path, address, port)
        # Launch of FileObserver
        watch.run(args.recursive)
    else:
        exit_fail(parser)

    exit(0)


if __name__ == '__main__':
    main()
