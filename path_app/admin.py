from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *
from .forms import *


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
class NodeResource(resources.ModelResource):
    class Meta:
        model = Node
class LinkResource(resources.ModelResource):
    class Meta:
        model = Link
class GanttParamResource(resources.ModelResource):
    class Meta:
        model = GanttParam
class MultiParamResource(resources.ModelResource):
    class Meta:
        model = MultiParam
class NetworkParamResource(resources.ModelResource):
    class Meta:
        model = NetworkParam
class Enabled_select_optionResource(resources.ModelResource):
    class Meta:
        model = Enabled_select_option
class Label_optionResource(resources.ModelResource):
    class Meta:
        model = Label_option
class Auto_layout_optionResource(resources.ModelResource):
    class Meta:
        model = Auto_layout_option
class Start_month_optionResource(resources.ModelResource):
    class Meta:
        model = Start_month_option
class Start_year_optionResource(resources.ModelResource):
    class Meta:
        model = Start_year_option
class Order_by_optionResource(resources.ModelResource):
    class Meta:
        model = Order_by_option
class X_axis_optionResource(resources.ModelResource):
    class Meta:
        model = X_axis_option
class Timing_optionResource(resources.ModelResource):
    class Meta:
        model = Timing_option
class Duration_optionResource(resources.ModelResource):
    class Meta:
        model = Duration_option

class CategoryStandardResource(resources.ModelResource):
    class Meta:
        model = CategoryStandard

class CategoryStandardAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryStandardResource]

class NodeStandardResource(resources.ModelResource):
    class Meta:
        model = NodeStandard

class NodeStandardAdmin(ImportExportModelAdmin):
    resource_classes = [NodeStandardResource]

class LinkStandardResource(resources.ModelResource):

    class Meta:
        model = LinkStandard

class LinkStandardAdmin(ImportExportModelAdmin):
    resource_classes = [LinkStandardResource]    

# Register your models here.

admin.site.register(Category)
admin.site.register(Node)
admin.site.register(Link)
admin.site.register(Loop)
admin.site.register(Enabled_select_option)
admin.site.register(Label_option)
admin.site.register(Auto_layout_option)
admin.site.register(NetworkParam)
admin.site.register(Start_month_option)
admin.site.register(Start_year_option)
admin.site.register(Order_by_option)
admin.site.register(X_axis_option)
admin.site.register(Timing_option)
admin.site.register(Duration_option)
admin.site.register(GanttParam)
admin.site.register(MultiParam)
admin.site.register(Version)
admin.site.register(CurrentVersion)
admin.site.register(Grouped)
admin.site.register(NodeStandard, NodeStandardAdmin)
admin.site.register(LinkStandard, LinkStandardAdmin)
admin.site.register(CategoryStandard, CategoryStandardAdmin)

