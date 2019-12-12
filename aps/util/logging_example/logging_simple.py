"""
Basic creation of a logger and some general usage examples.

Logger.debug(), Logger.info(), Logger.warning(), Logger.error(), and Logger.critical() all create log records
with a message and a level that corresponds to their respective method names.
The message is actually a format string, which may contain the standard string substitution syntax of %s, %d, %f,
and so on.

__author__: kmu
"""

import logging

# Set up the logger and log-file.
logging.basicConfig(filename='example.log',
                    # format='%(levelname)s: [%(asctime)s] %(message)s',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

logging.debug('This message is only shown in debug mode.')
logging.info('This is general information')
logging.warning('Something runs but should be checked.')
logging.error('Something is not working!')
logging.critical('Something is messing up things badly!!!')
