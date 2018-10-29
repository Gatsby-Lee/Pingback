"""
@author Gatsby Lee
@since 2018

@note: hard-coded storage type for Redis
"""
import logging
import time

from pbpy.cexception import IntegrityError

LOGGER = logging.getLogger(__name__)
REDIS_KEY_TEMPLATE = 'sset:{}_completed_tasks'

class PingbackApp(object):

    @classmethod
    def add_pingback(cls, storage_engine, pingback_src, pingback_entry):
        """Add pingback entry into storage ( currently Redis )

            Args:
                storage_engine (obj): instance of storage_engine
                pingback_src (str): used to generate storage namespace
                pingback_entry (tuple): (task_id(str), post_id(str))
            Returns: None
            Exceptions:
                If same pingback_entry exists, then IntegrityError raise.
        """
        LOGGER.debug("%s,%s", pingback_src, pingback_entry)
        storage_namespace = REDIS_KEY_TEMPLATE.format(pingback_src)
        # zadd: O(log(N)), sadd: O(1)
        # SortedSet zadd options:
        #   NX - Don't update already existing elements. Always add new elements.
        sortedset_score = int(time.time())
        # @note: To process pingback task in order of arrival, `SortedSet` is used.
        #  If this use case is unncessary, it's good to change to `Set`
        # @note: redis-py 2.10.6 doesn't support `nx` option in zadd yet.
        #   https://github.com/andymccurdy/redis-py/issues/649#issuecomment-346997655
        # @todo: Either wait until redis-py supports `nx` option
        #  or build redis-py wrapper module.
        # ret_value = storage_engine.zadd(storage_namespace, sortedset_score,
        #                                 pingback_entry)
        ret_value = storage_engine.execute_command('ZADD', storage_namespace, 'NX',
                                                   sortedset_score, pingback_entry)
        if ret_value == 0:
            raise IntegrityError('%s already exists in %s' % \
            (pingback_entry, storage_namespace))
