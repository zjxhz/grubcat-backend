# coding=utf-8
"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'grubcat.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'grubcat.dashboard.CustomAppIndexDashboard'
"""
from admin_user_stats.base_modules import BaseChart, BaseCharts
from django.contrib.auth import get_user_model

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name
from fanju.models import AuditStatus, User, UserPhoto, MealComment, PhotoComment


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for grubcat.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        # self.children.append(modules.LinkList(
        #     _('Quick links'),
        #     layout='inline',
        #     draggable=False,
        #     deletable=False,
        #     collapsible=False,
        #     children=[
        #         [_('Return to site'), '/'],
        #         [_('Change password'),
        #          reverse('%s:password_change' % site_name)],
        #         [_('Log out'), reverse('%s:logout' % site_name)],
        #     ]
        # ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))


        need_audit_user_count = User.objects.filter(status=AuditStatus.WAIT_TO_AUDIT).count()
        if need_audit_user_count:
            need_audit_user_title = u'待审核用户（<span style="color:red">%s</span>）' % need_audit_user_count
        else:
            need_audit_user_title = u'待审核用户（%s）' % need_audit_user_count

        self.children.append(modules.LinkList(
            u'TODO',
            children=[
                {
                    'title': need_audit_user_title,
                    'url': "%s?status__exact=%s" % (reverse("admin:fanju_user_changelist"), AuditStatus.WAIT_TO_AUDIT) ,
                    'external': False,
                },
            ]
        ))

        self.children.append(RegistrationCharts())

        self.children.append(UploadPhotoCharts())

        self.children.append(PhotoCommentCharts())

        self.children.append(MealCommentCharts())

        # append a recent actions module
        # self.children.append(modules.RecentActions(_('Recent Actions'), 5))




class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for grubcat.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)


class RegistrationChart(BaseChart):
    """
    Dashboard module with user registration charts.

    With default values it is suited best for 2-column dashboard layouts.
    """
    queryset = get_user_model().objects.all()
    date_field = 'date_joined'


class RegistrationCharts(BaseCharts):
    """ Group module with 3 default registration charts """
    title = u'新增用户'
    chart_model = RegistrationChart


class UploadPhotoChart(BaseChart):
    queryset = UserPhoto.objects.all()
    date_field = 'timestamp'


class UploadPhotoCharts(BaseCharts):
    """ Group module with 3 default registration charts """
    title = u'上传照片'
    chart_model = UploadPhotoChart


class MealCommentChart(BaseChart):
    queryset = MealComment.objects.all()
    date_field = 'timestamp'


class MealCommentCharts(BaseCharts):
    """ Group module with 3 default registration charts """
    title = u'饭局评论'
    chart_model = MealCommentChart


class PhotoCommentChart(BaseChart):
    queryset = PhotoComment.objects.all()
    date_field = 'timestamp'


class PhotoCommentCharts(BaseCharts):
    """ Group module with 3 default registration charts """
    title = u'照片评论'
    chart_model = PhotoCommentChart