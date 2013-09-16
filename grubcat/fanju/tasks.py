#coding=utf-8
from celery import task
from celery.utils.log import get_task_logger
from django.conf import settings
from fanju.models import User, Meal

logger = get_task_logger(__name__)


@task()
def share_fanju(uid):
    if isinstance(uid, User):
        user = uid
    else:
        user = User.objects.get(pk=uid)
    weibo_client = user.get_webio_client()
    r = weibo_client.short_url.shorten.post(url_long=settings.SITE_DOMAIN)
    fanju_url = r.urls[0].url_short
    share_texts = (u'你敢和志趣相投的陌生人一起吃饭，一起交流吗？反正我敢！ ',
                   u'刚注册了饭聚网，一个严肃却又有趣的陌生人线下聚会平台, 不用再担心被放鸽子了！ ',
                   u'一个靠谱的陌生人线下聚会平台，不用再担心被放鸽子了。赶快来看看吧，因为在这里你可以找到志同道合的朋友，找到心仪的TA哦！ ')

    share_text = "%s%s" % (share_texts[2], fanju_url)
    visible = 2 if settings.DEBUG else 0
    weibo_client.statuses.update.post(uid=user.weibo_id, status=share_text, visible=visible)
    # fanju_pic = open(meal.normal_cover_path, 'rb')
    # weibo_client.statuses.upload.post(status=share_text, pic=fanju_pic)
    # fanju_pic.close()


@task()
def share_meal(uid, meal_id, is_join=False):
    user = User.objects.get(pk=uid)
    meal = Meal.objects.get(pk=meal_id)
    weibo_client = user.get_webio_client()
    r = weibo_client.short_url.shorten.post(url_long=settings.SITE_DOMAIN + meal.get_absolute_url())
    meal_url = r.urls[0].url_short
    if is_join:
        share_text = u"我刚参加了一个活动 “%s”，还有%s个名额！%s" % (meal.topic, meal.left_persons, meal_url)
    else:
        share_text = u"我刚发现一个活动 “%s”，还有%s个名额！%s" % (meal.topic, meal.left_persons, meal_url)

    # visible = 2 if settings.DEBUG else 0
    # share_pic_url = u"%s%s" % (settings.SITE_DOMAIN, meal.normal_cover_url)
    # weibo_client.statuses.upload_url_text.post(status=share_text, url=share_pic_url,visible=1) #need 高级权限

    # weibo_client.statuses.update.post(status=share_text, visible=visible)
    meal_pic = open(meal.normal_cover_path, 'rb')
    weibo_client.statuses.upload.post(status=share_text, pic=meal_pic)
    meal_pic.close()

def follow_fanju_weibo(uid):
    if isinstance(uid, User):
        user = uid
    else:
        user = User.objects.get(pk=uid)
    weibo_client = user.get_webio_client()
    weibo_client.friendships.create.post(uid=settings.WEIBO_OFFICIAL)


@task()
def user_registered(uid):
    user = User.objects.get(pk=uid)
    user.audit_by_machine()
    # share_fanju(user)
    follow_fanju_weibo(user)

###################pubsub notification ################################
