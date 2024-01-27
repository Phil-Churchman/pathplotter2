from django.urls import path
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [

    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),

    path("signup/", views.signup, name="signup"),
    path("change_password/", views.change_password, name="change_password"),
    # path("reset_password/", views.reset_password, name="reset_password"),

    path("versions/", views.versions, {'modal': "", "start": ""}, name="versions"),
    path("versions_fail/", views.versions, {'modal': "fail", "start": ""}, name="versions"),
    path("versions_gantt_error/", views.versions, {'modal': "gantt_error", "start": ""}, name="versions"),

    path("", views.versions, {'modal': "", "start": "start"}, name="versions"),
    
    path("index/", views.versions, {'modal': "", "start": "start"}, name="versions"),

    path("versions_archive/", views.versions_archive, name="versions_archive"),

    path("categories/", views.categories, name="categories"),
    # path("new-category/", views.new_category, name="new_category"),
    path("del-category/", views.del_category, name="del_category"),

    path("add-category/", views.add_category, name="add_category"),
    path("del-node/<str:id>/", views.del_node, name="del_node"),

    path("edit-node/<int:node_id>", views.edit_node, name="edit_node"),
    path("edit-link/<int:link_id>", views.edit_link, name="edit_link"),
    path("edit-loop/<int:id>", views.edit_loop, name="edit_loop"),

    path("edit-category/<int:id>", views.edit_category, name="edit_category"),
    path("edit-version/<int:id>", views.edit_version, name="edit_version"),

    path("set-version/<int:id>/", views.set_version, name="set_version"),

    path("set_version_ajax/", views.set_version_ajax, name="set_version_ajax"),

    path("add-version/", views.add_version, name="add_version"),
    path("copy-version/<int:id>", views.copy_version, name="copy_version"),

    path("del-version/<int:id>/", views.del_version, name="del_version"),
    path("archive-version/<int:id>", views.archive_version, name="archive_version"),

    path("update_loops/", views.update_loops, name="update_loops"),
    # path("update_goal_connections/", views.update_goal_connections, name="update_goal_connections"),

    path("edit-network-params/", views.edit_network_params, name="edit_network_params"),
    path("edit-gantt-params/", views.edit_gantt_params, name="edit_gantt_params"),
    
    path("switch/", views.switch, name="switch"),

    path("save_group/", views.save_group, name="save_group"),

    path("edit-param/<str:type>/<str:param>/<str:value>/", views.edit_param, name="edit_param"),
    path("edit-param-post/", views.edit_param_post, name="edit_param_post"),

    path("layout/<str:type>/", views.layout, name="layout"),
  
    path("nodes/<str:category>/", views.nodes, name="nodes"),
    path("links/", views.links, name="links"),

    path("loops/", views.loops, {'modal': False}, name="loops"),
    path("loops_modal/", views.loops, {'modal': True}, name="loops_modal"),


    path("del-node/<str:id>/", views.del_node, name="del_node"),
    path("del-link/<str:id>/", views.del_link, name="del_link"),

    path("add-node/", views.add_node, name="add_node"),
    path("add-node-placed/<int:x>/<int:y>/", views.add_node_placed, name="add_node_placed"),
    
    path("add-link/", views.add_link, name="add_link"),

    path("add-link-defined/", views.add_link_defined, {'backup': True}, name="add_link_defined"),
    path("add-link-defined-nobackup/", views.add_link_defined, {'backup': False}, name="add_link_defined"),

    path("upload-file/", views.upload_file, name="upload_file"),
    path("export-file/", views.export_file, name="export_file"),

    path("upload-node-csv/", views.upload_node_csv, name="upload_node_csv"),
    path("upload-link-csv/", views.upload_link_csv, name="upload_link_csv"),

    path("network/", views.network, {'modal': False}, name="network"),

    path("network_modal/", views.network, {'modal': True}, name="network_modal"),

    path("gantt/<int:gantt_num>/", views.gantt, {'next': False, 'modal': False}, name="gantt"),
    path("gantt_modal/<int:gantt_num>/", views.gantt, {'next': False, 'modal': True}, name="gantt_modal"),

    path("new_pos/", views.new_pos, name="new_pos"),
    path("new_mid/", views.new_mid, name="new_mid"),

    #temp

    path("snapshot/", views.snapshot, name="snapshot"),
    path("load-snapshot/", views.load_snapshot, name="load_snapshot"),
    path("undo/", views.undo, name="undo"),
    path("redo/", views.redo, name="redo"),

    path("export_survey/<str:type>/", views.export_survey, name="export_survey"),

    # path("group_view/", views.group_view, name="group_view"),

    path("disable_redundant/", views.disable_redundant, name="disable_redundant"),

    path("enable_all/", views.enable_all, name="enable_all"),

    # path("update_groups/", views.update_groups, name="update_groups"),

    path("edit-group/<int:id>", views.edit_group, name="edit_group"),

    path("del-ajax/", views.del_ajax, name="del_ajax"),

    path("enabled_loops_only/", views.enabled_loops_only, name="enabled_loops_only"),

    path("export_enabled_nodes/", views.export_enabled_nodes, name="export_enabled_nodes"),

    path("export_links/", views.export_links, name="export_links"),

    path("standardise_nodes/", views.standardise_nodes, name="standardise_nodes"),

    path("export_link_analysis/", views.export_link_analysis, name="export_link_analysis"),

    path("export_standard_nodes/", views.export_standard_nodes, name="export_standard_nodes"),

    path("export_standard_links/", views.export_standard_links, name="export_standard_links"),

    path("export_snapshot/", views.export_snapshot, name="export_snapshot"),

    path("import_snapshot/", views.import_snapshot, name="import_snapshot"),

    path("add_link_standard/", views.add_link_standard, name="add_link_standard"),

    path("apply_link_standards/", views.apply_link_standards, name="apply_link_standards"),

    path("export_version/", views.export_version, name="export_version"),

    path("import_version/", views.import_version, name="import_version"),
]