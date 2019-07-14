from django.db import models
from datetime import datetime
from user.models import User
import uuid


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(verbose_name='分类名称', max_length=32)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=datetime.now())


class AppModel(models.Model):
    id = models.UUIDField(verbose_name="ID", primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='app名', null=True, blank=True, max_length=128)
    categorys = models.ManyToManyField(Category, blank=True, verbose_name="分类")
    read_num = models.IntegerField(verbose_name="查看人数", null=True, blank=True, default=0)
    use = models.IntegerField(verbose_name="使用次数", null=True, blank=True, default=0)
    image_url = models.FileField(verbose_name="封面缩略图", null=True, blank=True, upload_to="uploads/app/images")
    desc = models.CharField(verbose_name="简介", max_length=48, null=True, blank=True)
    is_del = models.BooleanField(verbose_name="是否删除", default=False)
    is_active = models.BooleanField(verbose_name="是否可见", default=True, null=True, blank=True)
    is_Review = models.BooleanField(verbose_name="是否审核", default=True, null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    view = models.OneToOneField("app.ViewContent", verbose_name="html", related_name="app", null=True, blank=True,
                                on_delete=models.SET_NULL)
    html = models.OneToOneField("app.HtmlContent", verbose_name="view", related_name="app", null=True, blank=True,
                                on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    tags = models.ManyToManyField("app.Tags", verbose_name="标签", blank=True)

    class Meta:
        db_table = "appmodel"
        verbose_name_plural = verbose_name = "应用信息"

    @staticmethod
    def get_all():
        return AppModel.objects.all()

    @staticmethod
    def get_by_id(id):
        try:
            app = AppModel.objects.get(id=id)
        except AppModel.DoesNotExist:
            return None
        return app


class ViewContent(models.Model):
    view_content = models.TextField(verbose_name="代码")
    change_time = models.DateTimeField(verbose_name="修改时间", auto_now_add=True)
    download = models.CharField(verbose_name="下载路径", default="", blank=True,null=True, max_length=256)

    class Meta:
        db_table = "view_content"
        verbose_name_plural = verbose_name = "app后台内容"


class HtmlContent(models.Model):
    html_content = models.TextField(verbose_name="html代码")
    change_time = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)

    class Meta:
        db_table = "html_content"
        verbose_name_plural = verbose_name = "app页面内容"


class Tags(models.Model):
    tag_name = models.CharField(verbose_name="标签名称", max_length=32)
    add_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    change_time = models.DateTimeField(verbose_name="修改时间", auto_now_add=True)

    class Meta:
        db_table = "tags"
        verbose_name_plural = verbose_name = "标签表"
