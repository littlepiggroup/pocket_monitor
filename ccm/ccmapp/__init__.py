from ccm.ccmapp.videomgr.videomgr import VideoSchedulerThread


def startup():
    print 'Start VideoSchedulerThread'
    my_thread = VideoSchedulerThread()
    my_thread.start()
    print 'VideoSchedulerThread started.'

# startup() TODO: enable it for collecting video. python manage.py runserver --noreload

# default_app_config = 'ccm.ccmapp.apps.CcmappConfig'