import sys
import daemon
import time
import argparse
import json
import logging

import zappa.core


SLEEP_TIME_SECONDS = 5


def main():
    p = create_parser()
    args = p.parse_args(sys.argv[1:])

    with open(args.config) as f:
        config = json.loads(f.read())

    if args.daemon:
        with daemon.DaemonContext():
            run_loop(config)
    else:
        run_loop(config)


def run_loop(config):
    zappa.core.setup_logging(config)
    log = logging.getLogger('brew')

    from pybrew import coordinator
    coordinator = coordinator.Coordinator(config)
    sleep_time = int(config.get('sleep_time', SLEEP_TIME_SECONDS))
    log.info("Entering run loop")
    while True:
        try:
            coordinator.run()
        except:
            log.error("Error running notifier", exc_info=True)

        time.sleep(sleep_time)


def create_parser():
    p = argparse.ArgumentParser()
    p.add_argument('-d', '--daemon', action='store_true',
                   help='will run the client as a daemon')
    p.add_argument('-c',
                   '--config',
                   help='The configuration file, if there is one')
    return p

if __name__ == '__main__':
    main()
