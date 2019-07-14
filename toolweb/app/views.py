from django.shortcuts import render, Http404, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View
from django.utils.decorators import method_decorator
from .models import AppModel, HtmlContent, ViewContent
from django.http import JsonResponse
from datetime import datetime
from toolweb.settings import BASE_DIR
import json, os, importlib
import random


# Create your views here.
class AppListView(View):

    def get(self, request, **kwargs):
        result = {"code": 200, "apps": [], "error": None}
        apps = AppModel.get_all()
        al = []
        for app in apps:
            apl = {}
            apl["id"] = app.id
            apl["name"] = app.name
            apl["read_num"] = app.read_num
            apl["image_url"] = str(app.image_url)
            apl["desc"] = app.desc
            apl["user"] = "admin"
            apl["time"] = app.add_time.strftime("%Y-%m-%d")
            al.append(apl)
        result["apps"] = al

        return JsonResponse(result)


class GetUserAppsView(View):

    def get(self, request, **kwargs):
        return render(request, "app/myapps.html")

    def post(self, request, **kwargs):
        result = {"code": 200, "apps": [], "error": None}
        apps = AppModel.objects.filter(creator=request.user)
        al = []
        for app in apps:
            apl = {}
            apl["id"] = app.id
            apl["name"] = app.name
            apl["read_num"] = app.read_num
            apl["image_url"] = str(app.image_url)
            apl["desc"] = app.desc
            apl["user"] = "admin"
            apl["time"] = app.add_time.strftime("%Y-%m-%d")
            al.append(apl)
        result["apps"] = al

        return JsonResponse(result)


@method_decorator(csrf_exempt, name="dispatch")
class AppContentView(View):
    """
    返回用户定义app的页面 从库中获取html，如果没有返回详情页面
    """

    template_name = "app/app_html.html"

    def get(self, request, **kwargs):
        id = self.kwargs.get("id", None)
        app = AppModel.get_by_id(id)
        if app and app.html:
            # 如果有这个app,对这个app进行封装
            html = app.html.html_content
            return render(request, self.template_name, {"id": id, "html": html, "app_name": app.name})
        elif app:
            return HttpResponseRedirect("/app/info/" + str(app.id) + "/")
        else:
            raise Http404("页面没有找到")

    def post(self, request, **kwargs):
        # 提交后查询id 找到对应这个的content
        id = self.kwargs.get("id", None)
        app = AppModel.get_by_id(id)
        if app:
            print(type(app.view.download))
            print(os.getcwd())
            # 如果下载路径为空则下载到服务器，存储下载路径
            if not app.view.download or app.view.download == "" or app.view.download is None:
                # 引入文件
                name = self.saveMode(app)
                print(name)
                path = "static.cache_view." + name
                module = importlib.import_module(path)
                # 动态导入模块的类
                model = getattr(module, "result")
                data = model(request.POST)

            else:
                # 读取
                print('模块名', app.view.download)
                try:
                    path = "static.cache_view." + app.view.download
                    module = importlib.import_module(path)
                except Exception as e:
                    # 重新下载导入
                    print("导入模块报错:", e)
                    name = self.saveMode(app)
                    path = "static.cache_view." + name
                    module = importlib.import_module(path)

                # 动态导入模块的类
                model = getattr(module, "result")
                data = model(request.POST)
            # 如果发生修改，修改完把下载路径删除，至为None
            # 检测路径 为None下载到服务器，如果发生修改，下载路径删除

            return JsonResponse({"code": 200, "data": data})
        raise Http404

    def saveMode(self, app):
        # 下载
        now = datetime.now().strftime("%H%M%S")
        name = "".join([str(random.randint(1, 6)) for _ in range(4)]) + now
        path = os.path.join(BASE_DIR, "static", "cache_view", name + ".py").replace("\\", "/")
        with open(path, "w", encoding="utf-8") as f:
            f.write(app.view.view_content)
        app.view.download = name
        app.view.save()
        return name


class CreateAppView(View):
    def get(self, request, **kwargs):
        return render(request, "app/create_app.html")

    def post(self, request, **kwargs):
        result = {}
        app_name = request.POST.get("app_name", None)
        desc = request.POST.get("desc", None)
        app_type = request.POST.get("app_type", None)
        file = request.FILES.get("img", None)

        if app_name and desc and app_type:
            app = AppModel()
            app.name = app_name
            app.desc = desc

            if file:
                facename = file.name
                # 得到后缀
                suffix = facename.split('.')[1]
                name = datetime.now().strftime("%Y%m%d-%H%M%S") + '.' + suffix
                app.image_url = os.path.join("app-img", name)
                # 存储进去
                dirs = os.path.join(BASE_DIR, 'static', 'app-img', name)
                with open(dirs, "wb") as f:
                    for i in file.chunks():
                        f.write(i)
                    f.close()
            app.save()
            return HttpResponseRedirect("/app/info/" + str(app.id) + "/")
        else:
            if not app_name:
                result["name_error"] = "应用名称为必填项"
            elif not desc:
                result["desc_error"] = "简介为必填项"
            else:
                result["type_error"] = "类型为必填项"
        return render(request, "app/create_app.html", result)


class AppInfoView(View):
    def get(self, request, **kwargs):
        id = self.kwargs.get("id")
        app = AppModel.get_by_id(id)
        return render(request, "app/app_info.html", {"app": app})


class ChangeHtmlView(View):
    def get(self, request, **kwargs):
        id = request.GET.get("key")
        app = AppModel.get_by_id(id)
        if not app:
            raise Http404
        if not app.html:
            content = ""
        else:
            content = app.html.html_content

        return render(request, "app/html_add.html", {"id": id, "content": content})

    def post(self, request, **kwargs):
        result = {"code": 200, "data": None}
        content = request.POST.get("content", None)
        id = request.POST.get("key", None)

        app = AppModel.get_by_id(id)
        if not app:
            raise Http404
        # 先存 html
        html = HtmlContent(html_content=content)
        html.save()

        # app 存
        app.html = html
        app.save()

        result["data"] = id
        return JsonResponse(result)


class ChangeView(View):
    """ 编辑后台代码 """

    def get(self, request, **kwargs):
        id = request.GET.get("key")
        app = AppModel.get_by_id(id)
        if not app:
            raise Http404
        if not app.view:
            print(1)
            path = os.path.join(os.getcwd(), "utils", "default_view.txt")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                f.close()
        else:
            print(2)
            content = app.view.view_content

        return render(request, "app/view_add.html", {"id": id, "content": content})

    def post(self, request, **kwargs):
        result = {"code": 200, "data": None}
        content = request.POST.get("content", None)
        id = request.POST.get("key", None)

        app = AppModel.get_by_id(id)
        if not app:
            raise Http404
        # 先存 view 代码
        view = ViewContent(view_content=content)
        view.save()

        # app 存
        app.view = view
        app.save()
        # 返回id
        result["data"] = id
        return JsonResponse(result)


class PreHtmlView(View):
    """ 预览html 代码"""

    def get(self, request, **kwargs):
        id = request.GET.get("key", None)
        app = AppModel.get_by_id(id)
        if app and app.html:
            # 如果有这个app,对这个app进行封装
            html = app.html.html_content
            return render(request, "app/pre_html.html", {"html": html, "app_name": app.name})
        elif app:
            return HttpResponseRedirect("/app/info/" + str(app.id) + "/")
        else:
            raise Http404("页面没有找到")
