from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
import os
from .models import *
from .forms import *
from .utilities import *
import pickle
import csv
from io import StringIO
import copy


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # dont logout the user.
            # messages.success(request, "Password changed.")
            return redirect("/")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "registration/change_password.html", {'form':form})

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # update_session_auth_hash(request, form.user) # dont logout the user.
            # messages.success(request, "Password changed.")
            return redirect("/")
    else:
        form = PasswordResetForm(request.user)

    return render(request, "registration/reset_password.html", {'form':form})

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form':form})

@login_required
def categories(request):

    [version, state, currentversion] = current_version(request)
    state = "/categories/"
    setattr(currentversion, "state", state)
    currentversion.save()
    form = CategoryForm

    template = loader.get_template('categories.html')

    categories = sorted(Category.objects.filter(version=version), key = lambda x: x.category_code)
    for i in categories:
        i.editable = (i.category_code != ">")
        i.save()

    context = {
        'form': form,
        'categories': categories,
        'version': version.name
        }
    return HttpResponse(template.render(context, request))

@login_required
def versions(request, **kwargs):
    if CurrentVersion.objects.filter(user=request.user).count() == 0:
        CurrentVersion.objects.create(user=request.user)

    if kwargs["start"] == "start":
        check_db()
    template = loader.get_template('versions.html')
    user = request.user
    versions = Version.objects.filter(user=user, archive=False).order_by("name")
    # if CurrentVersion.objects.filter(user=request.user).count() == 0:
    #     CurrentVersion.objects.create(user=request.user, version = list(versions)[0])    
    # versions = list(Version.objects.filter(user=user, archive=False).order_by("name"))
    # versions = sorted(versions,key = lambda x: x.name)
    [version, state, currentversion] = current_version(request)
    state = "/versions/"
    if currentversion != None:
        setattr(currentversion, "state", state)
        currentversion.save()
    # form = VersionForm
    for i in versions:
        if i == version:
            i.current = True
            i.save()
        else:
            i.current = False
            i.save()
    fail_modal = False
    gantt_error_modal = False
    if kwargs["modal"] == "fail":
        fail_modal = True
    elif kwargs["modal"] == "gantt_error":
        gantt_error_modal = True
    
    # nodes = list(Node.objects.filter(version=version, enabled=True))
    # categories = list(Category.objects.filter(version=version, enabled=True))
    # for i in list(nodes):
    #     if i.category not in categories:
    #         i.delete()
        
    # nodes = list(Node.objects.filter(version=version))
    # categories = list(Category.objects.filter(version=version))   

    # try: 
    #     node_standards = list(set([i.node_standard.code for i in nodes]))
    #     category_codes = list(set([i.category_code for i in categories]))
    #     standardise = True
    #     for i in node_standards:
    #         if i not in category_codes:
    #             standardise=False
    #             break
    # except:
    #     standardise = False

    # standardise = True

    context = {
    # 'form': form,
    # 'standardise': standardise,
    'versions': versions,
    'version_not_selected': not check_version_selected(version),
    # 'version_not_selected': len(versions) == 0,

    'fail_modal': fail_modal,
    'gantt_error_modal': gantt_error_modal
    }
    return HttpResponse(template.render(context, request))

@login_required
def versions_archive(request):
    template = loader.get_template('versions_archive.html')
    user = request.user
    versions = Version.objects.filter(user=user, archive=True)
    [version, state, currentversion] = current_version(request)
    state = "/versions_archive/"
    if currentversion != None:
        setattr(currentversion, "state", state)
        currentversion.save()
    form = VersionForm
    for i in versions:
        if i == version:
            i.current = True
            i.save()
        else:
            i.current = False
            i.save()
    context = {
        'form': form,
        'versions': versions,
        'version_not_selected': not check_version_selected(version)
        }
    return HttpResponse(template.render(context, request))

@login_required
def nodes(request, category):
    [version, state, currentversion] = current_version(request)
    state = "/nodes/"+category+"/"
    setattr(currentversion, "state", state)
    currentversion.save()
    template = loader.get_template('nodes.html')
    if category == "all":
        nodes = Node.objects.filter(version=version)
    else:
        nodes = Node.objects.filter(version=version, category=category)
    nodes = sorted(list(nodes), key=lambda x: [x.category.category_code, x.node_code])
    categories = sorted(Category.objects.filter(version=version), key = lambda x: x.category_code)
    add_form = NodeForm
    add_form.initial = {"enabled": True, "weight": 1}
    if category == "all":
        category_text = "All categories"
    else:
        category_text = Category.objects.get(id=category)
        nodes = list(Node.objects.filter(version=version))
    categories = list(Category.objects.filter(version=version))   

    # try: 
    #     node_standards = list(set([i.node_standard.code for i in nodes]))
    #     category_codes = list(set([i.category_code for i in categories]))
    #     standardise = True
    #     for i in node_standards:
    #         if i not in category_codes:
    #             standardise=False
    #             break
    # except:
    #     standardise = False
    
    standardise = True

    context = {
        'nodes': nodes,
        'categories': categories,
        'form': add_form,
        'category': category_text,
        'standardise': standardise,
        'version': version.name
        }
    return HttpResponse(template.render(context, request))

@login_required
def links(request):
    [version, state, currentversion] = current_version(request)
    state = "/links/"
    setattr(currentversion, "state", state)
    currentversion.save()
    template = loader.get_template('links.html')
    form = LinkForm(version=version)
    from_category = "All"
    to_category = "All"   

    if request.method == 'POST':

        form = LinkForm(request.POST, version=version)
        from_category = request.POST.get("from_category")
        to_category = request.POST.get("to_category")

    links = list(Link.objects.filter(version=version))
    if from_category != "All":
        links = list(filter(lambda x: str(x.from_node.category.id) == str(from_category), links))
    if to_category != "All":
        links = list(filter(lambda x: str(x.to_node.category.id) == str(to_category), links))
    links = sorted(links, key=lambda x: [x.from_node.category.category_code, x.from_node.node_code, x.to_node.category.category_code, x.to_node.node_code])
    categories = sorted(Category.objects.filter(version=version), key = lambda x: x.category_code)
    for i in categories:
        if str(i.id) == str(from_category):
            i.from_category = True
        else:
            i.from_category = False
    for i in categories:
        if str(i.id) == str(to_category):
            i.to_category = True
        else:
            i.to_category = False   
        i.save() 

    context = {
        'form': form,
        'links': links,
        'categories': categories,
        'superuser': request.user.is_superuser,
        'version': version.name
        }
    return HttpResponse(template.render(context, request))

@login_required
def loops(request, **kwargs):
    [version, state, currentversion] = current_version(request)
    state = "/loops/"
    setattr(currentversion, "state", state)
    currentversion.save()
    modal = kwargs["modal"]
    network_params = NetworkParam.objects.get(version=version)

    # Update loops and set Model to efficient if false response

    if network_params.Model_choice == "AC":
        if updateloops(request)==False:
            network_params.Model_choice = "EF"
            network_params.save()
            modal = True
            updateloops(request)
    else:
        updateloops(request)

    set_loops_enabled(request)
    
    network_params = NetworkParam.objects.get(version=version)

    if network_params.Enabled_loops_only:
        loops= list(Loop.objects.filter(version=version, enabled=True))
    else:
        loops= list(Loop.objects.filter(version=version))

    for i in loops:
        i.loop_code = get_loop_code(i)
        i.save()
    if network_params.Model_choice == "AC":
        model = "Accurate"
    else:
        model = "Efficient"

    template = loader.get_template('loops.html')
    loops = sorted(loops, key=lambda x: x.loop_code)
    context = {
        'loops': loops,
        'modal': modal,
        'model': model,
        'enabled_loops_only': NetworkParam.objects.get(version=version).Enabled_loops_only,
        'version': version.name
        }
    return HttpResponse(template.render(context, request))

@login_required
def network(request, **kwargs):
    [version, state, currentversion] = current_version(request)
    state = "/network/"
    setattr(currentversion, "state", state)
    currentversion.save()

    params = NetworkParam.objects.get(version=version)

    if params.Enabled_select == Enabled_select_option.objects.get(option="All"):
        goal_connections(request, False)
    elif params.Enabled_select == Enabled_select_option.objects.get(option="Enabled only"):
        goal_connections(request, True)

    if version == None:
        return
    template = loader.get_template('network.html')

    colour_dict = create_colour_dict(request)
    nodes = Node.objects.filter(version=version)   
    max_y = 0
    for n in nodes:
        n.colour = colour_dict[n.category]
        ypos = n.ypos
        if ypos != None:
            if ypos > max_y:
                max_y = ypos
    links = Link.objects.filter(version=version)
    colour_ref = {i.category_code + ": " + i.category_text: colour_dict[i] for i in colour_dict.keys()}
    colour_ref2 = {i.id: colour_dict[i] for i in colour_dict.keys()}
    params = get_network_params(version)
    snapshot = take_snapshot(request)
    nodes = snapshot["Node"]
    for i in nodes:
        del i["notes"]
    links = snapshot["Link"]
    for i in links:
        del i["notes"]    
    categories = snapshot["Category"]
    n_unplaced = []
    data = get_data(request)
    conn_nodes = connected_nodes(data)
    for n in nodes:
        category = list(filter(lambda a: a["id"] == n["category"], categories))[0]
        n["colour"] = colour_ref2[n["category"]]
        n["category_enabled"] = category["enabled"]
        
        n["full_label"] = category["category_code"] + n["node_code"] + ": " + n["node_text"]
        n["short_label"] = category["category_code"] + n["node_code"]
        
        if params["Enabled_select"] == "Enabled only":
            n["show"] = n["enabled"] and category["enabled"]
        elif params["Enabled_select"] == "Disabled only":
            n["show"] = not n["enabled"] or not category["enabled"]
        else:
            n["show"] = True
        
        if n["id"] not in conn_nodes and not params["Show_unconnected"]:
            n["show"] = False

        if n["placed"] == False and n["show"] == True:
            n_unplaced.append(n)

    if len(list(filter(lambda x: x["connected_to_goal"] == False and x["show"] == True, nodes))) == 0:
        conn_to_goal_legend = [False]
    else:
        conn_to_goal_legend = [True]

    n_per_row = params["Plot_width"] // 50
    counter_row = 0
    counter_column = 0
    for n in n_unplaced:
        n["xpos"] = 25 + counter_column * 50
        n["ypos"] = params["Plot_height"] + 25 + counter_row * 50
        if counter_column == n_per_row - 1:
            counter_row +=1
            counter_column = 0
        else:
            counter_column +=1

    if len(n_unplaced) == 0:
        unplaced_height = 0
    else:
        unplaced_height = (counter_row + 1) * 50 + 50
    legend_loop = False
    legend_group = False
    for l in links:
        from_node = list(filter(lambda a: a["id"] == l["from_node"], nodes))[0]
        to_node = list(filter(lambda a: a["id"] == l["to_node"], nodes))[0]
        l["xpos1"] = from_node["xpos"]
        l["xpos2"] = to_node["xpos"]
        l["ypos1"] = from_node["ypos"]
        l["ypos2"] = to_node["ypos"]
        l["from_node_enabled"] = from_node["enabled"] and from_node["category_enabled"]
        l["to_node_enabled"] = to_node["enabled"] and to_node["category_enabled"]

        if from_node in n_unplaced or to_node in n_unplaced:
            l["xmid"] = (l["xpos1"] + l["xpos2"])/2
            l["ymid"] = (l["ypos1"] + l["ypos2"])/2

        if params["Enabled_select"] == "Enabled only":
            l["show"] = l["enabled"] and l["from_node_enabled"] and l["to_node_enabled"]
        elif params["Enabled_select"] == "Disabled only":
            l["show"] = not l["enabled"] or not l["from_node_enabled"] or not l["to_node_enabled"]
        else:
            l["show"] = True

        if (params["Enabled_select"] == "All" and l["in_group"]) or (params["Enabled_select"] == "Enabled only" and l["in_enabled_group"]):
            l["colour"] = "cornflowerblue"
            legend_group = True
        elif (params["Enabled_select"] == "All" and l["in_loop"]) or (params["Enabled_select"] == "Enabled only" and l["in_enabled_loop"]):
            l["colour"] = "burlywood"
            legend_loop = True
        else:
            l["colour"] = "lightgrey"
    network_data = json.dumps([categories, nodes, links, params])
    loop_options = True
    context = {
        'svg_height': max(max_y + 40, params["Plot_height"] + unplaced_height),
        'plot_width': params["Plot_width"],
        "params": json.dumps(params),
        "colour_ref": json.dumps(colour_ref),
        "network_data": network_data.replace("'", ""),
        "loop_options": loop_options,
        "enabled": params["Enabled_select"],
        "modal": kwargs["modal"],
        "conn_to_goal_legend": json.dumps(conn_to_goal_legend),
        "legend_group": json.dumps([legend_group]),
        "legend_loop": json.dumps([legend_loop]),
        'version': version.name
        }

    return HttpResponse(template.render(context, request))

@login_required
def gantt(request, gantt_num, **kwargs):

    [version, state, currentversion] = current_version(request)

    params = GanttParam.objects.get(version=version)

    if params.Enabled_only:
        goal_connections(request, True)
    else:
        goal_connections(request, False)

    # Prevent navigation to gantt > 0 if not from gantt view

    if gantt_num != 0 and state[:7] != "/gantt/":
        return HttpResponseRedirect("/gantt/0/")

    enabled_only = GanttParam.objects.get(version=version).Enabled_only

    links, nodes, node_dict, node_dict_lookup = get_links_nodes(request, enabled_only)

    # Check if conditions for producing Gantt true

    goals = list(filter(lambda x: x.category.category_code == ">" , nodes))

    # goals = nodes.objects.filter(category__in=Category.objects.filter(category_code=">"))
    if len(goals) == 0 or len(nodes) == 0 or len(links) == 0 or len(goals) == len(nodes):
        return HttpResponseRedirect("/versions_gantt_error/")
    link_to_goal = False
    for i in links:
        if i.from_node not in goals and i.to_node in goals:
            link_to_goal = True
            break
    
    if link_to_goal == False:
        return HttpResponseRedirect("/versions_gantt_error/")
    
    # Set state

    # state = "/gantt/" + str(gantt_num) + "/"
    state = "/gantt/" + str(0) + "/"
    setattr(currentversion, "state", state)
    currentversion.save()

    template = loader.get_template('gantt.html')
    network_params = NetworkParam.objects.get(version=version)
    # gantt_params = GanttParam.objects.get(version=version)
    
    modal = kwargs["modal"]
    if network_params.Model_choice == "AC":
        if updateloops(request)==False:
            network_params.Model_choice = "EF"
            network_params.save()
            try:
                gantt_data, params, node_id_dict, group_id_dict, gantt_num, gantt_tot = build_gantt_alternative(request)
            except:
                return HttpResponseRedirect("/versions_gantt_error/")
            modal = True
        else:
            try:
                gantt_data, params, node_id_dict, group_id_dict, gantt_num, gantt_tot = build_gantt(request, gantt_num)
            except:
                try:
                    gantt_data, params, node_id_dict, group_id_dict, gantt_num, gantt_tot = build_gantt(request, 0)
                except:
                    return HttpResponseRedirect("/versions_gantt_error/")
    else:
        try:
            gantt_data, params, node_id_dict, group_id_dict, gantt_num, gantt_tot = build_gantt_alternative(request)
        except:
            return HttpResponseRedirect("/versions_gantt_error/")

    if params["Enabled_only"]:
        enabled_text = "Enabled only"
    else:
        enabled_text = "All"

    if params["Apply_groups"]:
        groups_text = "Groups"
    else:
        groups_text = "No groups"    

    if params["Durations"] == "With durations":
        duration_text = "Durations"
    else:
        duration_text = "No durations"

    if network_params.Model_choice == "AC":
        model_text = "Accurate"
    else:
        model_text = "Efficient"
    context = {
        "gantt_data": json.dumps(gantt_data).replace("'", ""),
        "node_id_dict": json.dumps(node_id_dict),
        "group_id_dict": json.dumps(group_id_dict),
        "enabled": enabled_text,
        "modal": modal,
        "model": model_text,
        "accurate": network_params.Model_choice == "AC",
        "gantt_num": gantt_num,
        "gantt_tot": gantt_tot,
        "groups": groups_text,
        "durations": duration_text,
        'version': version.name
    }
    return HttpResponse(template.render(context, request))

#delete functions

@login_required
def del_category(request):

    [version, state, currentversion] = current_version(request)
    if request.method == "POST":
        category_id = request.POST["del_category"]
        Category.objects.get(id=category_id, version=version).delete()
        add_backup(request, "generic")
        
    return HttpResponseRedirect(state)

@login_required
def del_node(request, id):
    try:
        if Node.objects.get(id=id).version.user != request.user:
            return HttpResponseRedirect("/nodes/all/")
    except:
        return HttpResponseRedirect("/nodes/all/")
    [version, state, currentversion] = current_version(request)
    Node.objects.get(id=id).delete()
    add_backup(request, "generic")
        
    return HttpResponseRedirect(state)

@login_required
def del_link(request, id):
    try:
        if Link.objects.get(id=id).version.user != request.user:
            return HttpResponseRedirect("/links/") 
    except:
        return HttpResponseRedirect("/links/")    
    [version, state, currentversion] = current_version(request)
    # if Link.objects.get(id=id).version.user != request.user:
    #     return HttpResponseRedirect("/links/")
    Link.objects.get(id=id, version=version).delete()
    add_backup(request, "generic")
        
    return HttpResponseRedirect(state)

@login_required
def del_version(request, id):
    try:
        if Version.objects.get(id=id).user != request.user:
            return HttpResponseRedirect("/versions/")
    except:
        return HttpResponseRedirect("/versions/")
    Version.objects.get(id=id).delete()
    
    return HttpResponseRedirect("/versions_archive/")

@login_required
def del_ajax(request):
    [version, state, currentversion] = current_version(request)
    if request.method == 'POST':
        post_data=json.loads(request.POST.get('post_data'))
        backup = post_data["backup"]
        ob_type = post_data["ob_type"]
        id = post_data["id"]
        if ob_type == "link":
            html = "links.html"
            try:
                link = Link.objects.get(id=id)
                link.delete()
            except:
                pass
        elif ob_type == "node":
            html = "nodes.html"
            try:
                node = Node.objects.get(id=id)
                node.delete()
            except:
                pass
        elif ob_type == "category":
            html = "categories.html"
            try:
                category = Category.objects.get(id=id)
                category.delete()
                
            except:
                pass
            
        if backup:
            add_backup(request, "generic")
    return render(request,html)  

#archive

@login_required
def archive_version(request, id):
    try:
        if Version.objects.get(id=id).user != request.user:
            return HttpResponseRedirect("/versions/")
    except:
        return HttpResponseRedirect("/versions/")
    [version, state, currentversion] = current_version(request)
    version=Version.objects.get(id=id)
    archived = version.archive
    if archived == False:
        # if version.id == id:
        #     currentversion.delete()
        setattr(version, "archive", True)
        version.save()
        return HttpResponseRedirect("/versions/")
    else:
        setattr(version, "archive", False)
        version.save()
        return HttpResponseRedirect("/versions_archive/")

# edit functions

@login_required
def edit_node(request, node_id):
    try:
        if Node.objects.get(id=node_id).version.user != request.user:
            return HttpResponseRedirect("/nodes/all/")
    except:
        return HttpResponseRedirect("/nodes/all/")
    [version, state, currentversion] = current_version(request)

    instance = Node.objects.get(id=node_id)
    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
        post.update({"version": version})
        # form = NodeForm(request.POST, instance=instance, version=version)
        form = NodeForm(post, instance=instance, version=version)
        form.version = version
        if form.is_valid():
            new_node = form.save(commit=False)
            
            if new_node.node_standard == None:
                new_node.node_standard = NodeStandard.objects.get(code="-")
            new_node.save()
            add_backup(request, "generic")
            return HttpResponseRedirect(state)
    else:
        form = NodeForm(instance=instance, version=version, initial={"version": version})
    
    context = {}
    context["node"] = instance
    context["form"] = form
    context["node_id"] = node_id
    context["name"] = Node.objects.get(id=node_id).category.category_code + Node.objects.get(id=node_id).node_code + ": " + Node.objects.get(id=node_id).node_text
    return render(request, 'edit-node.html', context)

@login_required
def edit_loop(request, id):
    try:
        if Loop.objects.get(id=id).version.user != request.user:
            return HttpResponseRedirect("/loops/")
    except:
        return HttpResponseRedirect("/loops/")
    [version, state, currentversion] = current_version(request)

    # currentversion.state = "/edit-loop/" + str(id)
    # currentversion.save()
    instance = Loop.objects.get(id=id, version=version)
    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
        post.update({"version": version})
        form = LoopForm(post, instance=instance, version=version)
        if form.is_valid():
            form.save()
            add_backup(request, "generic")
        return HttpResponseRedirect("/loops/")
    else:
        form = LoopForm(instance=instance, version=version, initial={"version": version})
    links = list(instance.links.all())
    links_sorted = [sorted(links, key = lambda x: x.from_node.category.category_code + x.from_node.node_code)[0]]
    for i in range(len(links) - 1):
        to_node = links_sorted[-1].to_node
        next_link = list(filter(lambda x: x.from_node == to_node, links))[0]
        links_sorted.append(next_link)
    links = sorted(links, key = lambda x: x.from_node.category.category_code + x.from_node.node_code)
    context = {}
    context["links"] = links_sorted
    context["form"] = form
    context["id"] = id
    context["name"] = get_loop_code(Loop.objects.get(id=id))
    context["version"] = version

    return render(request, 'edit-loop.html', context) 

@login_required
def edit_group(request, id):
    
    # Check object belongs to logged-in user
    try:
        if Grouped.objects.get(id=id).version.user != request.user:
            return HttpResponseRedirect("/gantt/0/")
    except:
        return HttpResponseRedirect("/gantt/0/")
    [version, state, currentversion] = current_version(request)

    instance = Grouped.objects.get(id=id, version=version)
    if request.method == 'POST':

        form = GroupedForm(request.POST, instance=instance, version=version)
        if form.is_valid():
            form.save()
            # updategroups(request)
            add_backup(request, "generic")        
        return HttpResponseRedirect("/gantt/0/")
    else:
        form = GroupedForm(instance=instance, version=version, initial={"version": version})
    
    context = {}
    context["loops"] = instance.loops.all()
    context["form"] = form
    context["id"] = id
    context["version"] = version

    return render(request, 'edit-group.html', context) 

@login_required
def edit_version(request, id):
    # Check object belongs to logged-in user
    try:
        if Version.objects.get(id=id).user != request.user:
            return HttpResponseRedirect("/versions/")
    except:
        return HttpResponseRedirect("/versions/")
    version = Version.objects.get(id=id)
    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
        post.update({"user": request.user}) 
        form = VersionForm(post, instance=version, user=request.user, other_users=False) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/versions/")
    else:
        form = VersionForm(instance=version, user=request.user, other_users=False, initial={"user": request.user})

    context = {}
    context["form"] = form
    context["id"] = id
    context["name"] = Version.objects.get(id=id).name
    context["version"] = version.name
    return render(request, 'edit-version.html', context)    

@login_required
def edit_link(request, link_id):
    try:
        if Link.objects.get(id=link_id).version.user != request.user:
            return HttpResponseRedirect("/links/") 
    except:
        return HttpResponseRedirect("/links/")        
    [version, state, currentversion] = current_version(request)

    link = Link.objects.get(id=link_id, version=version)
    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
        post.update({"version": version})
        form = LinkForm(post, instance=link, version=version) 
        if form.is_valid():
            form.save()
            add_backup(request, "generic")
            
        return HttpResponseRedirect(state)
    else:
        form = LinkForm(instance=link, version=version, initial={"version": version})

    context = {}
    context["from_node"] = link.from_node
    context["to_node"] = link.to_node
    context["form"] = form
    context["link_id"] = link_id
    context["version"] = version
    from_node = link.from_node
    to_node = link.to_node
    context["name"] = from_node.category.category_code + from_node.node_code + ": " + from_node.node_text + " -- " + to_node.category.category_code + to_node.node_code + ": " + to_node.node_text
    return render(request, 'edit-link.html', context)  

@login_required
def edit_category(request, id):
    try:
        if Category.objects.get(id=id).version.user != request.user:
            return HttpResponseRedirect("/categories/") 
    except:
        return HttpResponseRedirect("/categories/")    

    [version, state, currentversion] = current_version(request)

    category = Category.objects.get(id=id, version=version)
    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
        post.update({"version": version})
        form = CategoryForm(post, instance=category, version=version) 
        if form.is_valid():
            form.save()
            add_backup(request, "generic")
            
        return HttpResponseRedirect(state)
    else:
        context = {}
        context["form"] = CategoryForm(instance=category, version=version, initial={"version": version})
        context["id"] = id
        context["name"] = Category.objects.get(id=id).category_code + ": " + Category.objects.get(id=id).category_text
        context["version"] = version
    return render(request, 'edit-category.html', context)     

# Add functions

@login_required
def add_node(request):
    [version, state, currentversion] = current_version(request)
    context = {}
    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
        post.update({"version": version})
        # form = NodeForm(request.POST, version=version)
        form = NodeForm(post, version=version)
        # form = NodeForm(request.POST)
        if form.is_valid():
            new_node = form.save(commit=False)
            if new_node.node_standard == None:
                new_node.node_standard = NodeStandard.objects.get(code="-")
            new_node.save()
            add_backup(request, "generic")
            return HttpResponseRedirect(state)
    else:
        # form = NodeForm(version=version, initial={"version": version})
        form = NodeForm(version=version)
        # form = NodeForm()
    
    context['form'] = form
    context["version"] = version
    return render(request, 'add-node.html', context)

@login_required
def add_node_placed(request, x, y):

    x = int(x)
    y = int(y)

    [version, state, currentversion] = current_version(request)
    context = {}
    if request.method == 'POST':
        form = NodeForm(request.POST, version=version)
        if form.is_valid():
            new_node = form.save()
            if new_node.node_standard == None:
                new_node.node_standard = NodeStandard.objects.get(code="-")
                new_node.save()
            add_backup(request, "generic")
            return HttpResponseRedirect("/network/")
        
    else:
        form = NodeForm(version=version, initial={"version": version, "xpos": x, "ypos": y, "placed": True})
    
    context['form'] = form
    return render(request, 'add-node-placed.html', context)

@login_required
def add_link(request):
    [version, state, currentversion] = current_version(request)
    context = {}

    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
        post.update({"version": version})
        form = LinkForm(post, version=version)
        from_node = request.POST.get("from_node")
        to_node = request.POST.get("to_node")
        existing = Link.objects.filter(from_node=from_node, to_node=to_node)
        node0 = Node.objects.get(id=from_node)
        node1 = Node.objects.get(id=to_node)
        if existing.count() == 0:
            if form.is_valid():
                form.save()
                new_link = Link.objects.get(from_node=node0, to_node=node1)
                new_link.xmid = (node0.xpos + node1.xpos)/2
                new_link.ymid = (node0.ypos + node1.ypos)/2
                new_link.save()
                add_backup(request, "generic")
                return HttpResponseRedirect("/links/")
    else:
        form = LinkForm(version=version, initial={"version": version})
        form.initial = {"enabled": True, "weight": 1}
        

    context['form'] = form
    context["version"] = version
    return render(request, 'add-link.html', context)

@login_required
def add_category(request):
    [version, state, currentversion] = current_version(request)
    context = {}    
    
    if request.method == 'POST':
        post = copy.deepcopy(request.POST)
        post.update({"version": version})
        form=CategoryForm(post, version=version)
        if form.is_valid():
            form.save()
            add_backup(request, "generic")
            return HttpResponseRedirect(state)

        else:
            context['form'] = form
            context["version"] = version
            return render(request, 'add-category.html', context)

    else:
        form = CategoryForm(version=version, initial={"version": version})
        form.initial = {"enabled": True}   
        context['form'] = form
        context["version"] = version
        return render(request, 'add-category.html', context)

@login_required    
def add_version(request):
    if request.method == 'POST':    
        post = copy.deepcopy(request.POST)
        post.update({"user": request.user})  
        form = VersionForm(post, user=request.user, other_users=False)
      
        if form.is_valid():
            version = form.save()
            if CurrentVersion.objects.all().count() == 0:
                CurrentVersion.objects.create(user=request.user, version=version)

            return HttpResponseRedirect("/versions/")
        else:
            context = {}
            context['form'] = form
            context["version"] = version
            return render(request, 'add-version.html', context)

    context = {}
    form = VersionForm(user=request.user, other_users=False, initial={"user": request.user})
    context['form'] = form
    context["version"] = version
    return render(request, 'add-version.html', context)

# enable / disable

@login_required
def switch(request):
    if request.method == 'POST':
        post_data=json.loads(request.POST.get('post_data'))
        id = post_data["id"]
        ob_type = post_data["ob_type"]
        if ob_type == "link":
            link = Link.objects.get(id=id)
            setattr(link, "enabled", not link.enabled)
            link.save()
        elif ob_type == "node":
            node = Node.objects.get(id=id)
            setattr(node, "enabled", not node.enabled)
            node.save()
        elif ob_type == "category":
            category = Category.objects.get(id=id)
            setattr(category, "enabled", not category.enabled)
            category.save()
        add_backup(request, "generic")
    return render(request,"nodes.html")   

@login_required
def save_group(request):
    if request.method == 'POST':
        post_data=json.loads(request.POST.get('post_data'))
        id = post_data["id"]
        loop = Loop.objects.get(id=id)
        setattr(loop, "group", not loop.group)
        loop.save()
        add_backup(request, "generic")
    return render(request,"nodes.html")   

@login_required
def enabled_loops_only(request):
    [version, state, currentversion] = current_version(request)

    if request.method == 'POST':
        post_data=json.loads(request.POST["post_data"])
        if post_data == "checked":
            checked = True
        else:
            checked = False

        network_params = NetworkParam.objects.get(version=version)
        setattr(network_params, "Enabled_loops_only", not checked)
        network_params.save()
        add_backup(request, "generic")
        
    return HttpResponseRedirect("/loops/")

# edit params

@login_required
def edit_network_params(request):
    [version, state, currentversion] = current_version(request)
    instance = NetworkParam.objects.get(version=version)
    if request.method == 'POST':
        form = NetworkParamForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            add_backup(request, "generic")

            return HttpResponseRedirect(state)
    else:
        context = {}
        context["form"] = NetworkParamForm(instance=instance)
        context["action"] = "/edit-network-params/"
        context["version"] = version
    return render(request, 'edit-network-params.html', context) 

@login_required
def edit_gantt_params(request):
    [version, state, currentversion] = current_version(request)
    instance = GanttParam.objects.get(version=version)
    if request.method == 'POST':

        form = GanttParamForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            add_backup(request, "generic")

            return HttpResponseRedirect(state)
    else:
        context = {}
        context["form"] = GanttParamForm(instance=instance)
        context["action"] = "/edit-gantt-params/"
        context["version"] = version
    return render(request, 'edit-gantt-params.html', context) 

@login_required
def edit_param(request, type, param, value):
    [version, state, currentversion] = current_version(request)
    value = value.replace("_", " ")
    if type == "network":
        model = NetworkParam
    else:
        model = GanttParam

    model_object = model.objects.get(version=version)
    if model._meta.get_field(param).get_internal_type() == "ForeignKey":
        ref_model = model._meta.get_field(param).related_model
        ref_model_object = ref_model.objects.get(option=value)
        
        setattr(model_object, param, ref_model_object)
        model_object.save()
    else:
        setattr(model_object, param, value)
        model_object.save()
    add_backup(request, "generic")
    return HttpResponseRedirect(state)

@login_required
def edit_param_post(request):
    [version, state, currentversion] = current_version(request)
    if request.method == 'POST':

        [paramtype, param, value] = json.loads(request.POST["post_data"])
    if paramtype == "network":
        model = NetworkParam
    else:
        model = GanttParam    
    model_object = model.objects.get(version=version)
    if model._meta.get_field(param).get_internal_type() == "ForeignKey":
        ref_model = model._meta.get_field(param).related_model
        ref_model_object = ref_model.objects.get(option=value)
        
        setattr(model_object, param, ref_model_object)
        model_object.save()
    else:
        setattr(model_object, param, value)
        model_object.save()
    add_backup(request, "generic")
    if type == "network":
        return HttpResponseRedirect("/network/")
    else:
        return HttpResponseRedirect("/gantt/0/")

# Version functions

@login_required
def set_version(request, id):
    if Version.objects.get(id=id).user != request.user:
        return HttpResponseRedirect("/versions/")

    [v, state, currentversion] = current_version(request)
    if currentversion != None:
        if currentversion.version != None:
            if CurrentVersion.objects.get(user=request.user).version.id == id:
                return HttpResponseRedirect("/versions/")
    version = Version.objects.get(id=id)

    if CurrentVersion.objects.filter(user=request.user).count() == 0:
        currentversion = CurrentVersion.objects.create(user=request.user, version=version)
        currentversion.save()
        add_backup(request, "generic")
    # elif CurrentVersion.objects.get(user=request.user).version.id == id:
    #     CurrentVersion.objects.get(user=request.user, version=version).delete()
    else:
        setattr(currentversion, "version", version)
        currentversion.history = None
        currentversion.save()
        add_backup(request, "generic")

    objects = NetworkParam.objects.filter(version=version)
    if objects.count() == 0:
        NetworkParam.objects.create(version=version)
    objects = GanttParam.objects.filter(version=version)
    if objects.count() == 0:
        GanttParam.objects.create(version=version)  
    objects = Category.objects.filter(version=version, category_code=">")
    if objects.count() == 0:
        Category.objects.create(version=version, category_code=">", category_text="Goals")
    return HttpResponseRedirect("/versions/")

@login_required
def set_version_ajax(request):
    if request.method == 'POST':
        post_data=json.loads(request.POST.get('post_data'))
        id = post_data["id"]
    
        [v, state, currentversion] = current_version(request)

        if currentversion.version != None:
            if CurrentVersion.objects.get(user=request.user).version.id == id:
                return HttpResponseRedirect("/versions/")
        version = Version.objects.get(id=id)

        if CurrentVersion.objects.filter(user=request.user).count() == 0:
            currentversion = CurrentVersion.objects.create(user=request.user, version=version)
            currentversion.save()
            add_backup(request, "generic")
        # elif CurrentVersion.objects.get(user=request.user).version.id == id:
        #     CurrentVersion.objects.get(user=request.user, version=version).delete()
        else:
            setattr(currentversion, "version", version)
            currentversion.history = None
            currentversion.save()
            add_backup(request, "generic")

        objects = NetworkParam.objects.filter(version=version)
        if objects.count() == 0:
            NetworkParam.objects.create(version=version)
        objects = GanttParam.objects.filter(version=version)
        if objects.count() == 0:
            GanttParam.objects.create(version=version)  
        objects = Category.objects.filter(version=version, category_code=">")
        if objects.count() == 0:
            Category.objects.create(version=version, category_code=">", category_text="Goals")

    return render(request,"versions.html") 

@login_required
def copy_version(request, id):
    try:
        if Version.objects.get(id=id).user != request.user:
            return HttpResponseRedirect("/versions/")
    except:
        return HttpResponseRedirect("/versions/")

    old_ver = Version.objects.get(id=id)
    if request.method == "POST":
        form = VersionCopyForm(request.POST, user=request.user, other_users=True)

        id = request.POST["id"]
        if form.is_valid():
            new_ver = form.save()
            make_copy(old_ver, new_ver)
            return HttpResponseRedirect("/versions/")
    context = {}
    form = VersionCopyForm(user=request.user, other_users=True, initial={'name': old_ver.name, "user": request.user})
    context['form'] = form
    context["id"] = id
    context["name"] = Version.objects.get(id=id).name
    context["version"] = old_ver
    return render(request, 'copy-version.html', context)

# Loop functions

@login_required
def update_loops(request):

    # Used if update loops selected from network view

    [version, state, currentversion] = current_version(request)
    params = NetworkParam.objects.get(version=version)
    if params.Model_choice == "EF":
        updateloops(request)
    else:
        if not updateloops(request):
            params.Model_choice = "EF"
            params.save()
            updateloops(request)
            return HttpResponseRedirect(state[:-1] + "_modal/")
                
    return HttpResponseRedirect(state)

# Node, link and category functions

@login_required
def add_link_defined(request, **kwargs):
    backup = kwargs["backup"]
    [version, state, currentversion] = current_version(request)
    if request.method == 'POST':
        data=json.loads(request.POST["post_data"])
     
        from_node = Node.objects.get(id=data["from_node"])
        to_node = Node.objects.get(id=data["to_node"])
        Link.objects.create(from_node=from_node, to_node=to_node, xmid=(from_node.xpos + to_node.xpos)/2, ymid=(from_node.ypos + to_node.ypos)/2,version=version)
        if backup:
            add_backup(request, "generic")

    return HttpResponseRedirect("/network/")

@login_required
def new_pos(request):
    [version, state, currentversion] = current_version(request)

    if request.method == "POST":
        returned_data = json.loads(request.POST.get("post_data"))
        node = Node.objects.get(id=returned_data["id"], version=version)
        backup = returned_data["backup"]
        setattr(node, "xpos", returned_data["xpos"])
        setattr(node, "ypos", returned_data["ypos"])
        setattr(node, "placed", True)
        node.save()
        
        for i in Link.objects.filter(version=version):
            if node in [i.from_node, i.to_node]:
                setattr(i, "xmid", (i.from_node.xpos + i.to_node.xpos)/2)
                setattr(i, "ymid", (i.from_node.ypos + i.to_node.ypos)/2)
                i.save()
        if backup:
            add_backup(request, "generic")
    return HttpResponseRedirect("/network/")

@login_required
def new_mid(request):
    [version, state, currentversion] = current_version(request)
    if request.method == "POST":
        returned_data = json.loads(request.POST.get("post_data"))
        link = Link.objects.get(id=returned_data["id"], version=version)
        from_node = link.from_node
        to_node = link.to_node
        xmid_lin = (from_node.xpos + to_node.xpos)/2
        ymid_lin = (from_node.ypos + to_node.ypos)/2
        setattr(link, "xmid", xmid_lin + (returned_data["xmid_draw"] - xmid_lin) * 2)
        setattr(link, "ymid", ymid_lin + (returned_data["ymid_draw"] - ymid_lin) * 2)
        link.save()
        add_backup(request, "generic")

    return HttpResponseRedirect("/network/")

@login_required
def enable_all(request):
    [version, state, currentversion] = current_version(request)
    categories = list(Category.objects.filter(version=version))
    nodes = list(Node.objects.filter(version=version))
    links = list(Link.objects.filter(version=version))

    for i in categories:
        i.enabled = True
        i.save()
    for i in nodes:
        i.enabled = True
        i.save()    
    for i in links:
        i.enabled = True
        i.save()
    add_backup(request, "generic")
    return HttpResponseRedirect(state)

# Network functions

@login_required
def layout(request, type):
    if type == "network":
        auto_layout_network(request)
        add_backup(request, "generic")
    elif type == "columns":
        auto_layout_columns(request)
        add_backup(request, "generic")
    elif type == "links":
        auto_layout_links(request)
        add_backup(request, "generic")    
    
    return HttpResponseRedirect("/network/")

@login_required
def snapshot(request):

    [version, state, currentversion] = current_version(request)
    data = take_snapshot(request)

    return HttpResponseRedirect(state)

@login_required
def load_snapshot(request):

    [version, state, currentversion] = current_version(request)
    reverse_snapshot()

    return HttpResponseRedirect(state)

@login_required
def index(request):
    user = request.user
    template = loader.get_template('index.html')
    CurrentVersion.objects.filter(user=user).delete()
    context = {
        "version_not_selected": True
        }
    return HttpResponse(template.render(context, request))

# Redundant links

@login_required
def disable_redundant(request):
    disable_redundant_links(request)
    add_backup(request, "generic")
    return HttpResponseRedirect("/network/")

# Undo / redo

@login_required
def undo(request):
    [version, state, currentversion] = current_version(request) 
    history = pickle.loads(currentversion.history)
    backup, restore, data_last = history[0], history[1], history[2]

    if len(backup) == 0:
        return HttpResponseRedirect(state)

    backup, restore, data_last = do_undo(request, backup, restore, data_last)

    currentversion.history = pickle.dumps([backup, restore, data_last])
    currentversion.save()

    return HttpResponseRedirect(state)

@login_required
def redo(request):

    # global backup, restore, data_last 

    [version, state, currentversion] = current_version(request)
    history = pickle.loads(currentversion.history)
    backup, restore, data_last = history[0], history[1], history[2]

    if len(restore) == 0:
        return HttpResponseRedirect(state)

    backup, restore, data_last = do_redo(request, backup, restore, data_last)
    currentversion.history = pickle.dumps([backup, restore, data_last])
    currentversion.save()

    return HttpResponseRedirect(state)

# File import / export

@login_required
def upload_file(request):
    [v, state, currentversion] = current_version(request)

    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES, user=request.user, other_users=False)

        if form.is_valid():
            
            if request.FILES:
                myfile = request.FILES.get('myfile')
                filedata = json.load(myfile)
                version = form.save()

                # if currentversion != None:
                #     setattr(currentversion, "history", None)
                #     currentversion.save()
                # else:
                # CurrentVersion.objects.create(user=request.user, version=version)
                if CurrentVersion.objects.all().count() == 0:
                    CurrentVersion.objects.create(user=request.user, version=version)
                import_data(filedata, version)
                # add_backup(request, "generic")
                return HttpResponseRedirect("/versions/")

        context = {}
        context['form'] = form
        return render(request, 'upload-file.html', context)
    else:
        context = {}
        form = VersionForm(user=request.user, other_users=False, initial={"user": request.user})
        context['form'] = form
    return render(request, 'upload-file.html', context)

@login_required
def export_file(request):
    [version, state, currentversion] = current_version(request)
    if version == None:
        return
    dataset = json.dumps(export_data(request), indent=4)
    response = HttpResponse(dataset, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=data.json'
    return response

@login_required
def upload_node_csv(request):
    if request.method == 'POST':
        try:
            if request.FILES['myfile']:
                myfile = request.FILES['myfile']
                content = StringIO(myfile.read().decode('utf-8-sig'))
                importfile = csv.reader(content, dialect="excel")
                import_csv(request, importfile)
                add_backup(request, "generic")
                return HttpResponseRedirect("/versions/")
    
        except:
            return HttpResponseRedirect("/versions_fail/")

    return render(request, 'upload-node-csv.html')

@login_required
def upload_link_csv(request):
    if request.method == 'POST':
        try:
            mincount = request.POST.get("mincount")        

            if request.FILES['myfile']:
                myfile = request.FILES['myfile']
                content = StringIO(myfile.read().decode('utf-8-sig'))
                import_link_csv(request, content, mincount)
                add_backup(request, 'generic')
                return HttpResponseRedirect("/versions/")
        except:
            return HttpResponseRedirect("/versions_fail/")

    return render(request, 'upload-link-csv.html')

@login_required
def export_survey(request, type):
    [version, state, currentversion] = current_version(request)

    def sort_node_list(node_list):
        node_list = sorted(node_list, key=lambda x: x.category.category_code + x.node_code)
        node_list_start = []
        ref = [">", "B", "E"]
        for i in ref:
            for j in list(node_list):
                if j.category.category_code == i:
                    node_list_start.append(node_list.pop(node_list.index(j)))
        return node_list_start + node_list        


    if type == "full":
        file = os.path.join(os.getcwd(), "pathplotter", "add_link_template.json")
    elif type == "simple":
        file = os.path.join(os.getcwd(), "pathplotter", "add_link_template_simple.json")

    f = open(file)
    add_link_template = json.load(f)
    f.close()

    node_list = list(Node.objects.filter(version=version))

    node_list = sort_node_list(node_list)

    node_text_list = [j.category.category_code + j.node_code + " - " + j.node_text for j in node_list]

    if type == "full":

        for i in add_link_template["top_container"]["children"][0]["children"][1]["children"]:
            for j in i["options"]:
                # option_template = j
                id = j["id"]
                break
            break
        for i in range(len(add_link_template["top_container"]["children"][0]["children"][1]["children"])):
            add_link_template["top_container"]["children"][0]["children"][1]["children"][i]["options"] = []
            value = 1

            for node_text in node_text_list:
                add_link_template["top_container"]["children"][0]["children"][1]["children"][i]["options"].append({'class': 'SelectionOption', 'id': id, 'is_not_applicable': False, 'is_other': False, 'screen_to_message': False, 'text': node_text, 'value': value})
                value +=1
                id +=1
    
    elif type == "simple":

        i = add_link_template["top_container"]["children"][0]["children"][1]
        for j in i["options"]:
            # option_template = j
            id = j["id"]
            break

        for i in range(len(add_link_template["top_container"]["children"][0]["children"])-1):
            add_link_template["top_container"]["children"][0]["children"][i+1]["options"] = []
            value = 1

            for node_text in node_text_list:
                add_link_template["top_container"]["children"][0]["children"][i+1]["options"].append({'class': 'SelectionOption', 'id': id, 'is_not_applicable': False, 'is_other': False, 'screen_to_message': False, 'text': node_text, 'value': value})
                value +=1
                id +=1
    
    dataset = json.dumps(add_link_template, indent=4)
    response = HttpResponse(dataset, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=survey.json'

    return response

@login_required
def export_enabled_nodes(request):
    [version, state, currentversion] = current_version(request)
    enabled_nodes = list(Node.objects.filter(version=version, enabled=True))
    for i in list(enabled_nodes):
        if i.category.enabled == False:
            enabled_nodes.remove(i)

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="enabled_nodes.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["Version", "Category code", "Node code", "Description", "Standard"])
    for i in enabled_nodes:
        if i.node_standard != None:
            writer.writerow([version.name, str(i.category.category_code), str(i.node_code), i.node_text, i.node_standard.code + ": " + i.node_standard.name])
        else:
            writer.writerow([version.name, str(i.category.category_code), str(i.node_code), i.node_text, ""])

    return response

@login_required
def export_links(request):
    [version, state, currentversion] = current_version(request)
    links = list(Link.objects.filter(version=version))

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="links.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["Version", "From node", "To node", "Enabled", "Notes"])
    for i in links:
        if i.notes != None:
            writer.writerow([version.name, i.from_node.category.category_code + ": " + i.from_node.node_text , i.to_node.category.category_code + ": " + i.to_node.node_text, i.enabled, i.notes])
        else:
            writer.writerow([version.name, i.from_node.category.category_code + ": " + i.from_node.node_text , i.to_node.category.category_code + ": " + i.to_node.node_text, i.enabled, ""])

    return response

@login_required
def export_link_analysis(request):
    [version, state, currentversion] = current_version(request)
    enabled_nodes = list(Node.objects.filter(version=version, enabled=True))
    for i in list(enabled_nodes):
        if i.category.enabled == False:
            enabled_nodes.remove(i)
    
    enabled_links = list(Link.objects.filter(version=version, enabled=True))

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="link_analysis.csv"'},
    )    
    writer = csv.writer(response)
    writer.writerow(["Enabled node", "From links count", "To links count"])

    for i in enabled_nodes:
        from_links_count = 0
        to_links_count = 0
        
        for j in enabled_links:
            if j.to_node == i:
                from_links_count +=1
            if j.from_node == i:
                to_links_count +=1

        writer.writerow([i.category.category_code + i.node_code + ": " + i.node_text, from_links_count, to_links_count])

    return response

@login_required
def export_standard_nodes(request):
    # [version, state, currentversion] = current_version(request)

    standard_nodes = NodeStandard.objects.all()

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="standard_nodes.csv"'},
    )    
    writer = csv.writer(response)
    writer.writerow(["Code", "Name", "Combined"])

    for i in standard_nodes:

        writer.writerow([i.code, i.name.replace("/", "-"), i.code + ": " + i.name.replace("/", "-")])

    return response

@login_required
def export_standard_links(request):
    # [version, state, currentversion] = current_version(request)

    standard_links = LinkStandard.objects.all()

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="standard_links.csv"'},
    )    
    writer = csv.writer(response)
    writer.writerow(["From node", "To node"])

    for i in standard_links:

        writer.writerow([i.from_node.code + ": " + i.from_node.name, i.to_node.code + ": " + i.to_node.name])

    return response

@login_required
def export_snapshot(request):
    # [version, state, currentversion] = current_version(request)

    data = take_snapshot(request)

    response = HttpResponse(
        content_type="application/pkl",
        headers={"Content-Disposition": 'attachment; filename="snapshot.pkl"'},
    )    
    pickle.dump(data, response, protocol=pickle.HIGHEST_PROTOCOL)

    return response

@login_required
def import_snapshot(request):
    [v, state, currentversion] = current_version(request)

    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES, user=request.user, other_users=False)

        if form.is_valid():
            
            if request.FILES:
                myfile = request.FILES.get('myfile')
                filedata = pickle.load(myfile)
                version = form.save()
                if currentversion != None:
                    currentversion.version = version
                    currentversion.history = None
                    currentversion.gantt_buffer = None
                    currentversion.save()
                else:
                    CurrentVersion.objects.create(user=request.user, version=version)
                # if CurrentVersion.objects.all().count() == 0:
                #     CurrentVersion.objects.create(user=request.user, version=version)
                reverse_snapshot(request, filedata)
                add_backup(request, "generic")
                return HttpResponseRedirect("/versions/")

        context = {}
        context['form'] = form
        return render(request, 'import_snapshot.html', context)
    else:
        context = {}
        form = VersionForm(user=request.user, other_users=False, initial={"user": request.user})
        context['form'] = form
    return render(request, 'import_snapshot.html', context)

# Standardise nodes

@login_required
def standardise_nodes(request):
    [version, state, currentversion] = current_version(request)

    # for i in list(Category.objects.filter(version=version, enabled=False)):
    #     i.delete()
    # for i in list(Node.objects.filter(version=version, enabled=False)):
    #     i.delete()
    # for i in list(Link.objects.filter(version=version, enabled=False)):
    #     i.delete()    

    # nodes = list(Node.objects.filter(version=version, enabled=True))
    # links = list(Link.objects.filter(version=version, enabled=True))

    nodes = list(Node.objects.filter(version=version))
    links = list(Link.objects.filter(version=version))   

    node_code_list = [i.node_code for i in nodes]
    node_code_list.sort()
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    # counter0 = alphabet.index(node_code_list[-1][0]) + 1

    counter0 = 0
    counter1 = 0

    node_standard_dict = {}
    category_codes = [i.category_code for i in list(Category.objects.filter(version=version))]
    for i in list(nodes):
        if i.node_standard == None or i.node_standard.code == "-" or i.node_standard.code not in category_codes:
            i.node_code = alphabet[counter0] + alphabet[counter1]
            i.temp = True
            i.save()
            nodes.remove(i)
            if counter1 < len(alphabet) - 1:
                counter1 +=1
            elif counter1 == len(alphabet) - 1  and counter0 == len(alphabet) - 1:
                return HttpResponseRedirect("/versions_fail/")                
            else:
                counter1 = 0
                counter0 +=1   
        # existing_standard = Node.objects.filter(version=version, category=Category.objects.get(version=version, category_code=i.node_standard.code), node_text=i.node_standard.name).exclude(node_code=i.node_code)
        else:
            existing_standard = Node.objects.filter(version=version, category=Category.objects.get(version=version, category_code=i.node_standard.code), node_text=i.node_standard.name, temp=True)
            
            if existing_standard.count() == 1:
                new_node = list(existing_standard)[0]
                if i.duration > new_node.duration:
                    new_node.duration = i.duration
                if i.weight > new_node.weight:
                    new_node.weight = i.weight
                if i.notes != None:
                    if new_node.notes != None:
                        new_node.notes = new_node.notes + " -- " + i.notes
                    else: new_node.notes = i.notes
                if i.enabled == True:
                    new_node.enabled == True
                new_node.save()
            elif existing_standard.count() == 0:
                # new_node = Node.objects.create(version=version, duration=i.duration, weight=i.weight, notes=i.notes, node_standard = i.node_standard, category=Category.objects.get(version=version, category_code=i.node_standard.code), node_code=alphabet[counter0]+ alphabet[counter1], node_text=i.node_standard.name)
                new_node = Node.objects.create(version=version, duration=i.duration, weight=i.weight, notes=i.notes, node_standard = i.node_standard, category=Category.objects.get(version=version, category_code=i.node_standard.code), node_code=alphabet[counter0]+ alphabet[counter1], node_text=i.node_standard.name, enabled=i.enabled, temp=True)
                if counter1 < len(alphabet) - 1:
                    counter1 +=1
                elif counter1 == len(alphabet) - 1  and counter0 == len(alphabet) - 1:
                    return HttpResponseRedirect("/versions_fail/")               
                else:
                    counter1 = 0
                    counter0 +=1            
            # else:
            #     existing_standard = list(existing_standard)
            #     existing_standard = sorted(existing_standard, key = lambda x: x.node_code)
            #     new_node = existing_standard[-1]
            node_standard_dict[i] = new_node

    for i in links:
        if i.from_node in node_standard_dict.keys():
            from_node = node_standard_dict[i.from_node]
        else:
            from_node = i.from_node
        if i.to_node in node_standard_dict.keys():
            to_node = node_standard_dict[i.to_node]
        else:
            to_node = i.to_node        
        if from_node == to_node: continue
        if Link.objects.filter(version=version, from_node=from_node, to_node=to_node).count() == 0:
            Link.objects.create(version=version, from_node=from_node, to_node=to_node)

    for i in list(Node.objects.filter(version=version, temp=False)):
        i.delete()
    for i in list(Node.objects.filter(version=version)):
        i.temp=False
        i.save()
    
    # nodes = list(Node.objects.filter(version=version))
    # node_code_list = [i.node_code for i in nodes]
    # node_code_list.sort()
    # counter0_delta = alphabet.index(node_code_list[0][0])
    # counter1_delta = alphabet.index(node_code_list[0][1])

    # for i in node_code_list:
    #     node = Node.objects.get(version=version, node_code=i)
    #     node.node_code = alphabet[alphabet.index(node.node_code[0]) - counter0_delta] + alphabet[alphabet.index(node.node_code[1]) - counter1_delta]
    #     node.save()
    
    add_backup(request, "generic")
    return HttpResponseRedirect(state)
    
@login_required
def add_link_standard(request):


    if request.method == 'POST':
        post_data=json.loads(request.POST.get('post_data'))
        id = post_data["id"]
        html = "links.html"

    try:
        if Link.objects.get(id=id).version.user != request.user:
            return render(request,html) 
    except:
        return render(request,html)     

    [version, state, currentversion] = current_version(request)

    link = Link.objects.get(id=id)

    if NodeStandard.objects.filter(code = link.from_node.category.category_code, name=link.from_node.node_text).count() == 0:
        return render(request,html) 
    else:
        from_node_standard = NodeStandard.objects.get(code = link.from_node.category.category_code, name=link.from_node.node_text)
    if NodeStandard.objects.filter(code = link.to_node.category.category_code, name=link.to_node.node_text).count() == 0:
        return render(request,html) 
    else:
        to_node_standard = NodeStandard.objects.get(code = link.to_node.category.category_code, name=link.to_node.node_text)    
    if LinkStandard.objects.filter(from_node = from_node_standard, to_node = to_node_standard).count() != 0:
        return render(request,html) 
    else:
        LinkStandard.objects.create(from_node = from_node_standard, to_node = to_node_standard)
        
    return render(request,html) 

@login_required
def apply_link_standards(request):
    [version, state, currentversion] = current_version(request)

    category_code_list = [i.category_code for i in list(Category.objects.filter(version=version))]

    link_standards = list(LinkStandard.objects.all())
    for i in list(link_standards):
        if i.from_node.code not in category_code_list or i.to_node.code not in category_code_list:
            link_standards.remove(i)


    for i in link_standards:
        if Node.objects.filter(version=version, category=Category.objects.get(version=version, category_code=i.from_node.code), node_text=i.from_node.name).count() == 0:
            continue
        else:
            from_node = Node.objects.get(category=Category.objects.get(version=version, category_code=i.from_node.code), node_text=i.from_node.name)
        if Node.objects.filter(version=version, category=Category.objects.get(version=version, category_code=i.to_node.code), node_text=i.to_node.name).count() == 0:
            continue
        else:
            to_node = Node.objects.get(category=Category.objects.get(version=version, category_code=i.to_node.code), node_text=i.to_node.name)
        if Link.objects.filter(version=version, from_node = from_node, to_node = to_node).count() != 0:
            continue
        else:
            
            Link.objects.create(version=version, from_node = from_node, to_node = to_node, notes="Standard link added", xmid=(from_node.xpos + to_node.xpos)/2, ymid=(from_node.ypos + to_node.ypos)/2)


    add_backup(request, "generic")
    return HttpResponseRedirect("/links/")