import sys
import daemon
import argparse
import json
import logging

import zappa.core


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

    from pybrew import co2_counter
    counter = co2_counter.Counter(config)
    log.info("Entering run loop")
    counter.run()


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
