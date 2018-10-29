"""
@author Gatsby Lee
@since 2018

@note: hard-coded storage type
"""

REDIS_KEY_TEMPLATE = 'list:{}_completed_tasks'

class PingbackApp(object):

    @classmethod
    def add_pingback(cls, storage_engine, task_id, post_id):
        pass
