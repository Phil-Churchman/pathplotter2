from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *
from .forms import *

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
admin.site.register(Version)
admin.site.register(CurrentVersion)
admin.site.register(Grouped)
admin.site.register(NodeStandard, NodeStandardAdmin)
admin.site.register(LinkStandard, LinkStandardAdmin)

