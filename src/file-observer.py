#!/usr/bin/env python3
'''
File Observer daemon
'''
import time
import argparse
import requests
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from urllib3.exceptions import NewConnectionError
from requests.exceptions import RequestException


author = 'Marco Espinosa'
version = '1.0'
email = 'hi@marcoespinosa.com'


def configure_logging(name):
    '''
    Function to configure loggind
    @name: logger name
    @return logger
    '''
    level = logging.DEBUG

    log_setup = logging.getLogger(name)

    # Formatting logger output
    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Setting logger to console
    log_handler = logging.StreamHandler()

    # Setting formatter
    log_handler.setFormatter(formatter)

    # Setting level
    log_setup.setLevel(level)

    # Creating handler to configured logger
    log_setup.addHandler(log_handler)

    # Set logger
    return logging.getLogger(name)


# Configure logger
logger = configure_logging("file-observer")


class FileObserver:
    '''
    File Observer class
    '''

    # Private variables
    watchDirectory = ""
    address = ""
    port = 0

    def __init__(self, path, address="", port=0):
        '''
        Default constructor
        @path: path to watch
        '''

        self.observer = Observer()
        self.watchDirectory = path
        self.address = address
        self.port = port

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
            event_handler, self.watchDirectory, recursive=recursive)
        self.observer.start()

        try:
            while True:
                # Execution every 5 seconds
                time.sleep(5)
        except:
            self.observer.stop()
            logger.info("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    '''
    Handler for file observer events
    '''
    address = ""
    port = 0

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

        elif event.event_type in ['created', 'deleted']:
            logger.info(
                f"Watchdog received {event.event_type} event - {event.src_path}.")
            Handler.__send_event(event.event_type, event.src_path)

    @staticmethod
    def __send_event(event, payload):
        '''
        Send event to webservice
        '''
        if Handler.address != "" and Handler.port != 0:
            logger.info(
                f"Sending {event} with {payload} to webservice")

            try:
                r = requests.get(
                    f'{Handler.address}:{Handler.port}/{event}/\"{payload}\"')
            except RequestException:
                logger.error(f'Request ERROR.')
                return

            if r.status_code == 200:
                logger.info('OK')
            else:
                logger.error(f'Request ERROR: {r.status_code}')


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

    # Get arguments
    parser = argparse.ArgumentParser(description='File observer')
    parser.add_argument('-p', '--path', help='Path to watch',
                        dest='path', metavar='STRING')

    parser.add_argument('-r', '--recursive', help='Set to True to recursive watch',
                        dest='recursive', metavar='BOOLEAN')

    parser.add_argument('-e', '--enable-webservice', help='Set to True to send events to webservice',
                        dest='enablewebservice', metavar='BOOLEAN')

    parser.add_argument('-a', '--address',
                        help='Webservice host address or FQDN. Mandatory if enable-webservice set to True',
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
            if args.enablewebservice == True and (args.address is None or args.port is not None):
                exit_fail(parser)
            else:
                address = args.address
                port = args.port
        # Creation of FileObserver instance
        logger.info(f'Monitoring changes in {args.path}')
        logger.info(f'Send events to {address}:{port}')

        watch = FileObserver(args.path, address, port)
        # Launch of FileObserver
        watch.run(args.recursive)
    else:
        exit_fail(parser)

    exit(0)


if __name__ == '__main__':
    main()
