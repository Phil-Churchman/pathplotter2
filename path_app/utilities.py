import json, pickle
from django.contrib.auth.decorators import login_required
from django.apps import apps
from .models import *
from .forms import *
from django.contrib.auth.models import User, Group
import copy, math
from .loops import get_loops
import django.apps
import pandas as pd

network_lookup = {
"Model choice": "Model_choice",
"Plot height": "Plot_height", 
"Plot width": "Plot_width", 
"Move rate": "Move_rate", 
"Force threshold": "Force_threshold", 
"Target node distance": "Target_node_distance", 
"Link attraction": "Link_attraction", 
"Repulsion": "Repulsion", 
"Boundry repulsion": "Boundry_repulsion", 
"Target boundary distance": "Target_boundary_distance", 
"Max interations": "Max_interations", 
"Link clearance": "Link_clearance", 
"Pair separation": "Pair_separation", 
"Legend x spacing": "Legend_x_spacing", 
"Legend y spacing": "Legend_y_spacing", 
"Legend box pad": "Legend_box_pad", 
"Slow motion": "Slow_motion", 
"Hide links": "Hide_links", 
"Enabled select": ["Enabled_select", Enabled_select_option], 
"Link midpoints": "Link_midpoints", 
"Labels": ["Labels", Label_option], 
"JPG output resolution": "JPG_output_resolution", 
"Show arrows": "Show_arrows", 
"Include 'Goals' in key": "Include_Goals_in_key", 
"Auto-layout": ["Auto_layout", Auto_layout_option],
"Show unconnected": "Show_unconnected", 
"Enabled loops only": "Enabled_loops_only",
}

network_export = [
"Plot height", 
"Plot width", 
"Move rate", 
"Force threshold", 
"Target node distance", 
"Link attraction", 
"Repulsion", 
"Boundry repulsion", 
"Target boundary distance", 
"Max interations", 
"Link clearance", 
"Pair separation", 
"Legend x spacing", 
"Legend y spacing", 
"Legend box pad", 
"Slow motion", 
"Hide links", 
"Enabled select", 
"Link midpoints", 
"Labels", 
"JPG output resolution", 
"Show arrows", 
"Include 'Goals' in key", 
"Auto-layout",
]

gantt_lookup = {

"Plot height": "Plot_height", 
"Plot width": "Plot_width", 
"X-axis" : ["X_axis", X_axis_option],
"Time unit if 'Count'" : "Time_unit_if_Number",
"Start month if 'Month'" : ["Start_month_if_Month", Start_month_option],
"Start year" : ["Start_year", Start_year_option],
"Max X ticks" : "Max_X_ticks",
"Order by" : ["Order_by", Order_by_option],
"Plot padding" : "Plot_padding",
"Internal padding" : "Internal_padding",
"Legend limit" : "Legend_limit",
"Legend x spacing" : "Legend_x_spacing",
"Legend y spacing" : "Legend_y_spacing",
"Legend box pad" : "Legend_box_pad",
"Top margin" : "Top_margin",
"Right margin" : "Right_margin",
"Y axis space" : "Y_axis_space",
"X axis space" : "X_axis_space",
"Pixels per row" : "Pixels_per_row",
"Bar padding" : "Bar_padding",
"Tick length" : "Tick_length",
"Path optimisation max steps" : "Path_optimisation_max_steps",
"JPG output resolution" : "JPG_output_resolution",
"Timing" : ["Timing", Timing_option],
"Durations" : ["Durations", Duration_option],
"Show out seq." : "Show_out_seq",
"Enabled only" : "Enabled_only",
"Apply groups" : "Apply_groups"
}
node_standard = [
("-",	"Not defined"),
(">",	"Road freight decarbonisation goal"),
("1",	"Align energy, infrastructure, vehicle timelines"),
("1",	"Align to vehicle replacement cycles / used market"),
("1",	"Clear cut off dates"),
("1",	"Deliver quick wins (e.g. fridges)"),
("1",	"Front load long lead time activities"),
("1",	"Prioritise freight applications"),
("2",	"Align solutions to operation requirements"),
("2",	"Ancillary equipment power solutions"),
("2",	"Define technology standards"),
("2",	"E-fuel yes-no"),
("2",	"ERS yes-no"),
("2",	"Full system cost and emissions view"),
("2",	"H2 yes-no"),
("2",	"Motive technology choice per use case"),
("2",	"Select energy storage solution(s) - H2 or other"),
("2",	"Select solutions based on cost and efficiency"),
("2",	"Wait for new battery solutions yes-no"),
("3",	"Charging / fuelling capacity / coverage"),
("3",	"Define infrastructure funding / who pays"),
("3",	"Infrastructure sharing"),
("3",	"Land allocation for infrastructure"),
("3",	"National energy capacity / connection prioritisation"),
("3",	"Wider energy system alignment"),
("4",	"Create incentives for leasing companies"),
("4",	"Create incentives for operators"),
("4",	"Create incentives for public authorities"),
("4",	"Create last mile incentives"),
("4",	"Disincentivise fossil fuels"),
("4",	"Establish government / industry partnerships"),
("4",	"Implement emissions monitoring / VECTO"),
("4",	"Provide green project / innovation support"),
("4",	"Provide incentive duration guarantee"),
("4",	"Secure incentive funding"),
("4",	"Subsidise additional cost / first movers"),
("4",	"Tax regime supporting green transport"),
("5",	"Align planning process / regulations / speed"),
("5",	"Attract / subsidise development of skills"),
("5",	"Collaboration between authorities"),
("5",	"Develop collaboration framework"),
("5",	"Develop government / planning skills"),
("5",	"Develop maintenance and repair facilities"),
("5",	"Develop technology skills"),
("5",	"Secure capability / capacity fundng"),
("B",	"Battery range"),
("B",	"Collaboration barriers / competition"),
("B",	"Competition for public funds"),
("B",	"Coordination complexity"),
("B",	"Cost of charging on route"),
("B",	"First mover disadvantage"),
("B",	"Green H2 supply"),
("B",	"Grid / DNO capacity"),
("B",	"Higher TCO"),
("B",	"Impacts on vehicle capacity"),
("B",	"Infrastructure chicken and egg"),
("B",	"Lack of customer demand for decarbonisation"),
("B",	"Lack of delivery capability / resources"),
("B",	"Planning constraints"),
("B",	"Policy uncertainty"),
("B",	"Skills shortage"),
("B",	"SME viability of new solutions"),
("B",	"Technology uncertainty / confidence"),
("B",	"Up front vehicle cost"),
("B",	"Vehicle availability / cost"),
("E",	"Consolidation centres / delivery hubs / lockers"),
("E",	"Corporate ESG goals"),
("E",	"Decouple transport energy price from markets"),
("E",	"Delivery sharing"),
("E",	"Electricity supply decarbonisation"),
("E",	"Framework decarbonisation principles per operator type"),
("E",	"Last mile innovation / solutions"),
("E",	"Local policy driving change"),
("E",	"National energy / transport strategy"),
("E",	"New vehicle delivery models (e.g. OEM turnkey)"),
("E",	"Operator collaboration framework"),
("E",	"Political support / commitment to funding"),
("E",	"Potential resource sharing between operators"),
("E",	"Potential vehicle retrofitting"),
("E",	"Public / operator awareness raising"),
("E",	"Shared / aggregate data"),
("E",	"Trials / early adopter experience"),
("E",	"Working condition regulation (last mile)"),
]

gantt_export = [
"Plot height", 
"Plot width", 
"X-axis",
"Time unit if 'Count'",
"Start month if 'Month'",
"Start year",
"Max X ticks",
"Order by",
"Plot padding",
"Internal padding",
"Legend limit",
"Legend x spacing",
"Legend y spacing",
"Legend box pad",
"Top margin",
"Right margin",
"Y axis space",
"X axis space",
"Pixels per row",
"Bar padding",
"Tick length",
"Path optimisation max steps",
"JPG output resolution",
"Timing",
"Durations",
"Show out seq.",
"Enabled only",
"Apply groups"
]

ref_models = {
    Start_month_option: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    Enabled_select_option: ["All", "Enabled only", "Disabled only"],
    Label_option: ["Full labels", "Short labels", "No labels"],
    Auto_layout_option: ["Network", "Columns"],
    Start_year_option: ["2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"],
    Order_by_option: ["Time", "Category"],
    X_axis_option: ["Month", "Year", "Number"],
    Timing_option: ["Earliest", "Latest"],
    Duration_option: ["With durations", "Without durations"],
}

def check_db():
    if Start_month_option.objects.all().count() == 0:
        for i in ref_models.keys():
            for j in i.objects.all():
                j.delete()
            for j in ref_models[i]:
                i.objects.create(option=j)
    for i in node_standard:
        if NodeStandard.objects.filter(code=i[0], name=i[1]).count() == 0:
            NodeStandard.objects.create(code=i[0], name=i[1])
# Current

@login_required
def current_user_groups(request):
    user = request.user
    groups = list(Group.objects.filter(user=user))
    group_dict = {}
    for group in groups:
        group_users = list(group.user_set.all())
        group_dict[group] = group_users
    return group_dict

@login_required
def current_user(request):
    
    return request.user

@login_required
def current_version(request):
    user = current_user(request)

    if CurrentVersion.objects.filter(user=user).count() > 0:
        return [CurrentVersion.objects.get(user=user).version, CurrentVersion.objects.get(user=user).state, CurrentVersion.objects.get(user=user)]
    else:
        return [None, "/versions/", None]

# Utilities

def get_node_code(node):
    return node[:node.find(" ")]

def get_link_code(link):
    return link[0][:link[0].find(" ")] + "-" + link[1][:link[1].find(" ")]

def get_loop_links(loop_list):
    links = []
    for i in range(len(loop_list)):
        if i == len(loop_list) - 1:
            links.append(loop_list[i] + "-" + loop_list[0])
        else:    
            links.append(loop_list[i] + "-" + loop_list[i+1])
    return links  

@login_required
def create_colour_dict(request):
    [version, state, currentversion] = current_version(request)
    colour_list = ['#838B8B', '#7AC5CD', '#DAA520','#CD6839', '#8A2BE2', '#8B7355', '#C1CDCD', '#00008B', '#66CDAA', '#CD3333', '#CDAA7D', '#458B00', '#BCEE68', '#CD1076', '#66CDAA', '#4D4D4D', '#66CDAA', '#66CDAA', '#66CDAA', '#66CDAA', '#66CDAA', '#66CDAA', '#66CDAA']
    colour_dict = {}
    counter = 0
    categories = list(sorted(Category.objects.filter(version=version), key = lambda x: x.category_code))
    categories.append(categories.pop(categories.index(Category.objects.get(version=version, category_code=">"))))

    for i in categories:
        colour_dict[i] = colour_list[counter]
        counter += 1            
    return colour_dict

def check_version_selected(version):

    if version == None:
        version_selected = False
    else:
        version_selected = True
    return version_selected

def get_network_params(version):

    params = {}
    for i in network_lookup.keys():
        if type(network_lookup[i]).__name__ == "list":
            params[network_lookup[i][0]] = getattr(NetworkParam.objects.get(version=version), network_lookup[i][0]).option
        else:
            params[network_lookup[i]] = getattr(NetworkParam.objects.get(version=version), network_lookup[i])

    return(params)

@login_required
def get_data(request):
    # user = current_user()
    # version = CurrentVersion.objects.get(user=user).version
    [version, state, currentversion] = current_version(request)
    data = {"nodes": {}, "links": {}, "network_params": {}}

    for i in Node.objects.filter(version=version):
        data["nodes"][i.id] = {"xpos": i.xpos, "ypos": i.ypos}
    for i in Link.objects.filter(version=version):
        data["links"][i.id] = {"from_node": i.from_node.id, "to_node": i.to_node.id, "xmid": i.xmid, "ymid": i.ymid}

    for i in network_lookup.keys():
        
        if type(network_lookup[i]).__name__ == "list":

            data["network_params"][network_lookup[i][0]] = getattr(NetworkParam.objects.get(version=version), network_lookup[i][0]).option
        else:
            data["network_params"][network_lookup[i]] = getattr(NetworkParam.objects.get(version=version), network_lookup[i])

    return data

# Copy

def make_copy(old_ver, new_ver):

    model_list = apps.get_models()

    for i in model_list:
        if i.__name__ in ["Group", "User", "Version", "LogEntry", "Permission", "ContentType", "Session", "CurrentVersion"]:
            continue
        if "version" not in [j.name for j in i._meta.get_fields()]:
            continue
        for j in i.objects.filter(version=old_ver):
            new_obj = copy.deepcopy(j)
            new_obj.id = None
            new_obj.version = new_ver
            new_obj.save()
            if i.__name__ == "Loop":
                for k in j.links.all():
                    new_obj.links.add(k)
            if i.__name__ == "Grouped":
                for k in j.loops.all():
                    new_obj.loops.add(k)            
            
            new_obj.save()

            setattr(j, "copied_to", new_obj)
            j.save()
    
    for i in model_list:
        if i.__name__ in ["Group", "User", "Version", "LogEntry", "Permission", "ContentType", "Session"]:
            continue
        if "version" not in [j.name for j in i._meta.get_fields()]:
            continue
        for j in i.objects.filter(version=new_ver):
            for k in j._meta.fields:
                fieldname = k.name
                if fieldname == "version":
                    continue
                if i._meta.get_field(fieldname).get_internal_type() == "ForeignKey":
                    ref = getattr(j, fieldname)
                    if ref == None:
                        continue
                    if "version" not in [l.name for l in ref._meta.fields]:
                        continue                    
                    copied_to = getattr(ref, "copied_to")
                    if getattr(ref, "version") != new_ver:
                        setattr(j, fieldname, copied_to)
                        j.save()
    for i in Loop.objects.filter(version=new_ver):    
        for j in i.links.all():
            if getattr(j, "version") != new_ver:
                new_obj = getattr(j, "copied_to")
                i.links.add(getattr(new_obj, "id"))
                i.links.remove(j)
                i.save()
    for i in Grouped.objects.filter(version=new_ver):    
        for j in i.loops.all():
            if getattr(j, "version") != new_ver:
                new_obj = getattr(j, "copied_to")
                i.loops.add(getattr(new_obj, "id"))
                i.loops.remove(j)
                i.save()

# Loops

def get_loop_code(i):
    loop_links = list(i.links.all())
    ordered_links = [loop_links[0]]
    for j in range(len(loop_links) - 1):
        ordered_links.append(list(filter(lambda x: x.from_node == ordered_links[len(ordered_links)-1].to_node, loop_links))[0])
    from_node_codes = []
    for j in ordered_links:
        from_node_code = j.from_node.category.category_code + j.from_node.node_code
        from_node_codes.append(from_node_code)
    
    from_node_codes_copy = copy.deepcopy(from_node_codes)
    from_node_codes_copy.sort()
    from_node_start = from_node_codes_copy[0]
    index = from_node_codes.index(from_node_start)
    from_node_codes = from_node_codes[index:] + from_node_codes[:index]

    loop_code = ""

    for j in from_node_codes:
        loop_code = loop_code + j + "-"
    
    loop_code = loop_code[:-1]

    # for j in loop_links:
    #     link = [(j.from_node.category.category_code + j.from_node.node_code + " - " + j.from_node.node_text), (j.to_node.category.category_code + j.to_node.node_code + " - " + j.to_node.node_text)]
    #     link_code = (j.from_node.category.category_code + j.from_node.node_code + "-" + j.to_node.category.category_code + j.to_node.node_code)
    
    #     loop_link_codes.append((link_code, link))
    # loop_link_codes.sort()
    # while True:
    #     change = False
        
    #     for j in range(len(loop_link_codes)):
    #         if loop_link_codes[j-1][1][1] != loop_link_codes[j][1][0]:
    #             loop_link_codes[j-1], loop_link_codes[j] = loop_link_codes[j], loop_link_codes[j-1]
    #             change = True
    #     if change == False:
    #         break
    # loop_code = loop_link_codes[0][0][:loop_link_codes[0][0].find("-")]
    # for j in range(len(loop_link_codes) - 1):
    #     loop_code = loop_code + "-" + loop_link_codes[j+1][0][:loop_link_codes[j+1][0].find("-")]
    return loop_code

def get_links_enabled(request):
    [version, state, currentversion] = current_version(request)
    links_enabled = list(Link.objects.filter(version=version, enabled=True))
    nodes_enabled = list(Node.objects.filter(version=version, enabled=True))
    categories_enabled = list(Category.objects.filter(version=version, enabled=True))
    for i in links_enabled:
        if i.from_node not in nodes_enabled or i.to_node not in nodes_enabled or i.from_node.category not in categories_enabled or i.to_node.category not in categories_enabled:
            links_enabled.remove(i)
    return links_enabled          

@login_required
def set_loops_enabled(request):
    [version, state, currentversion] = current_version(request)
    links_enabled = get_links_enabled(request)

    for i in list(Loop.objects.filter(version=version)):
        i.enabled = True
        for j in i.links.all():
            if j not in links_enabled:
                i.enabled = False
                break

        i.save()

@login_required
def updateloops(request):
    [version, state, currentversion] = current_version(request)
    edges = []
    links = list(Link.objects.filter(version=version))
    for i in links:
        # Filter links with further links connected to both from_node and to_node
        # from_links = Link.objects.filter(from_node=i.to_node)
        # to_links = Link.objects.filter(to_node=i.from_node)
        # if from_links.count() > 0 and to_links.count() > 0:
        if len(list(filter(lambda x: x.from_node == i.to_node, links)))>0 and len(list(filter(lambda x: x.to_node == i.from_node, links)))>0:
            edges.append([i.from_node.id, i.to_node.id])
    loops = []

    links_enabled = get_links_enabled(request)

    if NetworkParam.objects.get(version=version).Model_choice == "AC":

        id_loops = get_loops(edges, version, False)
        if id_loops == False:
            for i in Loop.objects.filter(version=version):
                i.delete()
            return False
    
    else:
        id_loops = []

        # for i in links:
        #     for j in list(Link.objects.filter(version=version, from_node = i.to_node)):
        #         if i.from_node == j.to_node:
        #             if i.from_node.id < j.from_node.id:
        #                 id_loops.append([[i.from_node.id, i.to_node.id], [j.from_node.id, j.to_node.id]])
        #             else:
        #                 id_loops.append([[j.from_node.id, j.to_node.id], [i.from_node.id, i.to_node.id]])                    
        #             continue
        #         poss_loop = [[i.from_node.id, i.to_node.id], [j.from_node.id, j.to_node.id], [j.to_node.id, i.from_node.id]]
        #         min_id = min([i.from_node.id, j.from_node.id, j.to_node.id])
        #         start_link = list(filter(lambda x: x[0] == min_id, poss_loop))[0]
        #         poss_loop = poss_loop[poss_loop.index(start_link):] + poss_loop[:poss_loop.index(start_link)]
        #         if poss_loop in id_loops: continue

        #         if len(Link.objects.filter(version=version, from_node = j.to_node, to_node = i.from_node)) > 0:
        #             id_loops.append(poss_loop)
        for i in edges:
            for j in filter(lambda x: x[0] == i[1] , edges):
                if i[0] == j[1]:
                    if [[i[0], i[1]], [j[0], j[1]]] in id_loops or [[j[0], j[1]], [i[0], i[1]]] in id_loops: continue
                    if i[0] < j[1]:
                        id_loops.append([[i[0], i[1]], [j[0], j[1]]])
                    else:
                        id_loops.append([[j[0], j[1]], [i[0], i[1]]])                    
                    continue
                poss_loop = [[i[0], i[1]], [j[0], j[1]], [j[1], i[0]]]
                min_id = min([i[0], j[0], j[1]])
                start_link = list(filter(lambda x: x[0] == min_id, poss_loop))[0]
                poss_loop = poss_loop[poss_loop.index(start_link):] + poss_loop[:poss_loop.index(start_link)]
                if poss_loop in id_loops: continue
                if len(list(filter(lambda x: x[0] == j[1] and x[1] == i[0], edges))):
                    id_loops.append(poss_loop)

    # Check if loops new and add new loops

    for i in id_loops:
        # loop = [Link.objects.get(from_node=Node.objects.get(id=j[0]), to_node=Node.objects.get(id=j[1]) ) for j in i]
        # loop = sorted(loop, key=lambda x:x.id)
        loop = set([Link.objects.get(from_node=Node.objects.get(id=j[0]), to_node=Node.objects.get(id=j[1]) ) for j in i])
        loops.append(loop)
    new_loops = copy.deepcopy(loops)

    for i in list(Loop.objects.filter(version=version)):
        loop = []
        i.enabled = True
        for j in i.links.all():
            loop.append(j)
            if j not in links_enabled:
                i.enabled = False
        i.save()
        # loop = sorted(loop, key=lambda x:x.id)
        loop = set(loop)
        if loop not in loops:
            i.delete()
        else:
            if loop in new_loops:
                new_loops.remove(loop)
    for i in new_loops:
        new_loop = Loop(version=version)
        new_loop.save()
        new_loop.enabled = True
        for j in i:
            new_loop.links.add(j)
            if j not in links_enabled:
                new_loop.enabled = False
        new_loop.save()
    # Set links enabled loops / groups
    loop_links = []
    group_links = []
    loop_list = list(Loop.objects.filter(version=version))
    for i in loop_list:
        loop_links = loop_links + list(i.links.all())
        if i.group:
            group_links = group_links + list(i.links.all())
    loop_links = list(set(loop_links))
    group_links = list(set(group_links))

    enabled_loop_links = []
    enabled_group_links = []
    enabled_loop_list = list(Loop.objects.filter(version=version, enabled=True))
    for i in enabled_loop_list:
        enabled_loop_links = enabled_loop_links + list(i.links.all())
        if i.group:
            enabled_group_links = enabled_group_links + list(i.links.all())
    enabled_loop_links = list(set(enabled_loop_links))
    enabled_group_links = list(set(enabled_group_links))

    link_list = list(Link.objects.filter(version=version))
    for i in link_list:
        i.in_loop = False
        i.in_enabled_loop = False
        i.in_group = False
        i.in_enabled_group = False
        if i in loop_links:
            i.in_loop = True
            if i in group_links:
                i.in_group = True
        if i in enabled_loop_links:
            i.in_enabled_loop = True
            if i in group_links:
                i.in_enabled_group = True            


        # for j in list(Loop.objects.filter(version=version)):
        #     for k in j.links.all():
        #         if k == i:
        #             i.in_loop = True
        #             if j.group == True:
        #                 i.in_group = True
        #             break
        # for j in list(Loop.objects.filter(version=version, enabled=True)):                
        #     for k in j.links.all():
        #         if k == i:
        #             i.in_enabled_loop = True
        #             if j.group == True:
        #                 i.in_enabled_group = True
        #             break
        i.save() 
    return True

@login_required
def updategroups(request):

    # Updates group objects, retaining with durations if these already exist, removing if not
    # Note this means that durations will not persist if a loop within the groups group is removed then reinstated
    # Groups can consist of one or multiple loops
    # Run on building Gantt with Accurate model if "Apply groups" option True

    [version, state, currentversion] = current_version(request)

    if GanttParam.objects.get(version=version).Enabled_only:
        loop_groups = list(Loop.objects.filter(version=version, group=True, enabled=True))
    else:
        loop_groups = list(Loop.objects.filter(version=version, group=True))
    
    loop_nodes = {}
    for i in loop_groups:
        loop_nodes[tuple([i])] = [x.from_node for x in list(i.links.all())]

    while True:
        found = False
        for i in list(loop_nodes.keys()):
            for j in list(loop_nodes.keys()):
                if i == j: continue
                for ii in loop_nodes[i]:
                    for jj in loop_nodes[j]:
                        if ii == jj:
                            found = True
                            loop_nodes[tuple(list(i)+list(j))] = list(set(loop_nodes[i] + loop_nodes[j]))
                            del loop_nodes[i]
                            del loop_nodes[j]
                            break
                    if found: break
                if found: break
            if found: break
        if not found: break

    found_groups = [set(list(i)) for i in list(loop_nodes.keys())]

    for i in list(Grouped.objects.filter(version=version)):
        group = set(list(i.loops.all()))
        if group not in found_groups:
        #     if group in found_groups_enabled:
        #         i.enabled = True
        #     else:
        #         i.enabled = False
        #     # duration = 0
        #     # for j in i.loops.all():
        #     #     for k in j.links.all():
        #     #         node_dur = k.from_node.duration
        #     #         if node_dur > duration:
        #     #             duration = node_dur
        #     # i.duration = duration
        #     i.save()
        # else:
            i.delete()

    existing_groups = [set(list(i.loops.all())) for i in list(Grouped.objects.filter(version=version))]

    for i in found_groups:
        if i not in existing_groups:
            new_group = Grouped.objects.create(version=version)
            duration = 0
            for j in i:
                new_group.loops.add(j)
                for k in j.links.all():
                    node_dur = k.from_node.duration
                    if node_dur > duration:
                        duration = node_dur
            new_group.duration = duration
            new_group.save()

    return 

def connected_nodes(data):

    conn_nodes =  list(set([data["links"][i]["from_node"] for i in data["links"].keys()] + [data["links"][i]["to_node"] for i in data["links"].keys()]))
    conn_nodes.sort()
    return conn_nodes

# Auto-layout

def node_vectors(data): 
    vectors = {}
    conn_nodes = connected_nodes(data)

    for i in conn_nodes:
        for j in conn_nodes:  
            if i == j or (j, i) in list(vectors.keys()):
                continue
            vectors[(i, j)] = {}
            dist = pow(pow(data["nodes"][j]["xpos"] - data["nodes"][i]["xpos"], 2) + pow(data["nodes"][j]["ypos"] - data["nodes"][i]["ypos"], 2), 0.5)

            if data["nodes"][j]["xpos"] == data["nodes"][i]["xpos"]:
                if data["nodes"][j]["ypos"] > data["nodes"][i]["ypos"]:
                    angle = math.pi / 2
                else:
                    angle = math.pi * 3 / 2
            else:
                if data["nodes"][j]["xpos"] > data["nodes"][i]["xpos"]:
                    angle = math.atan((data["nodes"][j]["ypos"] - data["nodes"][i]["ypos"]) / (data["nodes"][j]["xpos"] - data["nodes"][i]["xpos"]))
                else:
                    angle = math.pi + math.atan((data["nodes"][j]["ypos"] - data["nodes"][i]["ypos"]) / (data["nodes"][j]["xpos"] - data["nodes"][i]["xpos"]))
            vectors[(i, j)]["dist"] = dist
            vectors[(i, j)]["angle"] = angle
    return vectors

def node_forces(data):

    vectors = node_vectors(data)
    spring_length = data["network_params"]["Target_node_distance"]
    spring_rate = data["network_params"]["Link_attraction"]   # if link > spring length 
    repulsion = data["network_params"]["Repulsion"]   # all node pairs if distance < spring length

    links = [[data["links"][i]["from_node"], data["links"][i]["to_node"]] for i in data["links"].keys()]

    for i in list(vectors.keys()):

        if [i[0], i[1]] in links or [i[1], i[0]] in links:
            vectors[i]["link"] = True
            vectors[i]["spring force"] = (vectors[i]["dist"] - spring_length) * spring_rate # Attraction = negative force      
        else:
            vectors[i]["link"] = False
            vectors[i]["spring force"] = 0
        
        if vectors[i]["dist"] < spring_length:
            vectors[i]["repulsion"] = - (spring_length - vectors[i]["dist"]) * repulsion # Repulsion = positive force
        else:
            vectors[i]["repulsion"] = 0
    
        if vectors[i]["spring force"] == 0 and vectors[i]["repulsion"] == 0:
            del vectors[i]

    active_nodes = list(set([i[0] for i in vectors.keys()] + [i[1] for i in vectors.keys()]))

    node_forces = {i: (0,0) for i in active_nodes}      

    for i in vectors.keys():

        node_forces[i[0]] = (
            node_forces[i[0]][0] + (vectors[i]["spring force"] + vectors[i]["repulsion"]) * math.cos(vectors[i]["angle"]),
            node_forces[i[0]][1] + (vectors[i]["spring force"] + vectors[i]["repulsion"]) * math.sin(vectors[i]["angle"])
        )
        node_forces[i[1]] = (
            node_forces[i[1]][0] + (vectors[i]["spring force"] + vectors[i]["repulsion"]) * math.cos(math.pi + vectors[i]["angle"]),
            node_forces[i[1]][1] + (vectors[i]["spring force"] + vectors[i]["repulsion"]) * math.sin(math.pi + vectors[i]["angle"])
        )
    return node_forces

@login_required
def auto_layout_network(request):
    # user = current_user()
    # version = CurrentVersion.objects.get(user=user).version
    [version, state, currentversion] = current_version(request)
    if Node.objects.filter(version=version).count() == 0:
        return
    
    data = get_data(request)
    

    
    conn_nodes = connected_nodes(data)

    initial_spacing = 40
    nodes_per_row = (data["network_params"]["Legend_x_spacing"] + data["network_params"]["Legend_box_pad"] * 2) // initial_spacing

    per_row = 1
    y_offset = 3
    params = NetworkParam.objects.get(version=version)
    y_spacing = params.Legend_y_spacing
    box_pad = params.Legend_box_pad

    num_items = Category.objects.filter(version=version).count()
    if params.Model_choice == "AC":
        num_items = num_items + 3
    else:
        num_items = num_items + 2

    y_limit_unconnected = (math.ceil(num_items / per_row)) * y_spacing + y_offset + box_pad * 2


    counter = 0
    margin = data["network_params"]["Target_boundary_distance"]
    x0_limit = margin
    x_limit = data["network_params"]["Plot_width"]
    y_limit = data["network_params"]["Plot_height"]

    for i in data["nodes"].keys():
        if i in conn_nodes:
            continue
        row = counter // nodes_per_row
        col = counter % nodes_per_row
        data["nodes"][i]["xpos"] = x_limit - (col + 0.5) * initial_spacing
        data["nodes"][i]["ypos"] = y_limit_unconnected + (row + 0.5) * initial_spacing 
        counter +=1

    it_counter = 0

    while it_counter < data["network_params"]["Max_interations"]:
        move_rate = data["network_params"]["Move_rate"]
        force_threshold = data["network_params"]["Force_threshold"]
        over_threshold = False
        forces = node_forces(data)

        x0_limit = margin
        x1_limit = x_limit - data["network_params"]["Legend_x_spacing"] - data["network_params"]["Legend_box_pad"] * 2 - margin
        y0_limit = margin
        y1_limit = y_limit - margin
        fx_delta = 0
        fy_delta = 0
        for i in conn_nodes:
            boundary_repulsion = data["network_params"]["Boundry_repulsion"]
            xpos, ypos = data["nodes"][i]["xpos"], data["nodes"][i]["ypos"]
            if xpos < x0_limit:
                fx_delta = (x0_limit - xpos) * boundary_repulsion
            if xpos > x1_limit:
                fx_delta = (x1_limit - xpos) * boundary_repulsion
            if ypos < y0_limit:
                fy_delta = (y0_limit - ypos) * boundary_repulsion
            if ypos > y1_limit:
                fy_delta = (y1_limit - ypos) * boundary_repulsion                

            forces[i] = (forces[i][0] + fx_delta, forces[i][1] + fy_delta)

        for i in conn_nodes:
            if pow(pow(forces[i][0],2) + pow(forces[i][1], 2), 0.5) > force_threshold:
                over_threshold = True
                break
        if over_threshold == False:
            break
        for i in conn_nodes:
            data["nodes"][i]["xpos"] = data["nodes"][i]["xpos"] + forces[i][0] * move_rate
            data["nodes"][i]["ypos"] = data["nodes"][i]["ypos"] + forces[i][1] * move_rate
        if data["network_params"]["Slow_motion"] == True:
            break
        it_counter += 1


    for i in Node.objects.filter(version=version):
        i.placed = True
        i.xpos = data["nodes"][i.id]["xpos"]
        i.ypos = data["nodes"][i.id]["ypos"]
        i.save()

    for i in Link.objects.filter(version=version):
        i.xmid = (i.from_node.xpos + i.to_node.xpos) / 2
        i.ymid = (i.from_node.ypos + i.to_node.ypos) / 2
        i.save()

    move_links(request, data)

@login_required
def auto_layout_columns(request):
    [version, state, currentversion] = current_version(request)
    params = NetworkParam.objects.get(version=version)

    # for i in Link.objects.all():
    #     setattr(i, "xmid", None)
    #     setattr(i, "ymid", None)
    #     i.save()

    x_min = getattr(params,"Target_boundary_distance")
    x_max = getattr(params,"Plot_width") - getattr(params,"Target_boundary_distance") - getattr(params,"Legend_x_spacing") - getattr(params,"Legend_box_pad")
    y_min = getattr(params,"Target_boundary_distance")
    y_max = getattr(params,"Plot_height") - getattr(params,"Target_boundary_distance")               
    
    cats = sorted(Category.objects.filter(version=version), key = lambda x: x.category_code)
    cats.append(cats.pop(cats.index(Category.objects.get(version=version, category_code=">"))))

    cat_count = len(cats)

    if cat_count > 1:
        x_spacing = (x_max - x_min) / (cat_count - 1)
    else:
        x_spacing = 0

    cat_counter = 0
    for i in cats:
        node_count = Node.objects.filter(category = i, version=version).count()
        if node_count > 1:
            y_spacing = (y_max - y_min) / (node_count - 1)
        else:
            y_spacing = 0
        node_counter = 0
        for j in Node.objects.filter(category = i, version=version):
            # if cat_count > 1:
            
            setattr(j, "xpos", x_min + x_spacing * cat_counter)
            
            if y_spacing != 0:
                 setattr(j, "ypos", y_min + y_spacing * node_counter)
            else:
                setattr(j, "ypos", (y_min + y_max) / 2)
            setattr(j, "placed", True)
            j.save()
            node_counter +=1
        cat_counter +=1

    for i in Link.objects.filter(version=version):
        from_node = getattr(i, "from_node")
        to_node = getattr(i, "to_node")
        x_from = getattr(from_node, "xpos")
        y_from = getattr(from_node, "ypos")
        x_to = getattr(to_node, "xpos")
        y_to = getattr(to_node, "ypos")
        setattr(i, "xmid", (x_from + x_to)/2)
        setattr(i, "ymid", (y_from + y_to)/2)
        i.save()

    data = get_data(request)
    move_links(request, data)

@login_required
def auto_layout_links(request):

    data = get_data(request)
    move_links(request, data)

# Links

@login_required
def move_links(request, data):
    [version, state, currentversion] = current_version(request)

    for i in data["links"].keys():
        data["links"][i]["xmid"], data["links"][i]["ymid"] = start_mid(data, data["links"][i]["from_node"], data["links"][i]["to_node"])

    min_line_gap = data["network_params"]["Link_clearance"]
    vectors = node_vectors(data)
    for i in data["links"].keys():
        from_node = data["links"][i]["from_node"]
        to_node = data["links"][i]["to_node"]
        for j in data["nodes"].keys():
            if j == from_node or j == to_node:
                continue
            if (from_node, to_node) in vectors.keys():
                vector_angle = vectors[(from_node, to_node)]["angle"]
                vector_dist = vectors[(from_node, to_node)]["dist"]
            else:
                vector_angle = math.pi + vectors[(to_node, from_node)]["angle"]
                vector_dist = vectors[(to_node, from_node)]["dist"]
            if data["nodes"][j]["xpos"] == data["nodes"][data["links"][i]["from_node"]]["xpos"]:
                if data["nodes"][j]["ypos"] > data["nodes"][from_node]["ypos"]:
                    node_angle = math.pi / 2
                else:
                    node_angle = math.pi * 3 / 2
            else:
                if data["nodes"][j]["xpos"] > data["nodes"][data["links"][i]["from_node"]]["xpos"]:
                    node_angle = math.atan((data["nodes"][j]["ypos"] - data["nodes"][from_node]["ypos"]) / (data["nodes"][j]["xpos"] - data["nodes"][from_node]["xpos"]))
                else:
                    node_angle = math.pi + math.atan((data["nodes"][j]["ypos"] - data["nodes"][from_node]["ypos"]) / (data["nodes"][j]["xpos"] - data["nodes"][from_node]["xpos"]))
            
            dist = pow(pow((data["nodes"][j]["xpos"] - data["nodes"][from_node]["xpos"]), 2) + pow((data["nodes"][j]["ypos"] - data["nodes"][from_node]["ypos"]), 2), 0.5)
            line_dist = dist * math.sin(vector_angle-node_angle)
            if abs(line_dist) < min_line_gap and math.cos(vector_angle-node_angle) > 0 and dist < vector_dist:    
                move_angle = vector_angle + math.pi/2
                if line_dist != 0:
                    x_move = line_dist / abs(line_dist) * (min_line_gap - abs(line_dist)) * math.cos(move_angle)
                    y_move = line_dist / abs(line_dist) * (min_line_gap - abs(line_dist)) * math.sin(move_angle)
                else:
                    x_move = min_line_gap * math.cos(move_angle)
                    y_move = min_line_gap * math.sin(move_angle)
                data["links"][i]["xmid"] = data["links"][i]["xmid"] + x_move

                data["links"][i]["ymid"] = data["links"][i]["ymid"] + y_move
    
    l_dict = {(data["links"][i]["from_node"], data["links"][i]["to_node"]): i for i in data["links"].keys()}
    l_list = list(l_dict.keys())

    for i in vectors.keys():
        
        if tuple([i[1], i[0]]) in l_list and i in l_list:
            link_id_1 = l_dict[i]
            link_id_2 = l_dict[tuple([i[1], i[0]])]
            vector_angle = vectors[i]["angle"]
            pair_separation = data["network_params"]["Pair_separation"]
            data["links"][link_id_1]["xmid"] = data["links"][link_id_1]["xmid"] + math.cos(vector_angle + math.pi/2) * pair_separation / 2
            data["links"][link_id_1]["ymid"] = data["links"][link_id_1]["ymid"] + math.sin(vector_angle + math.pi/2) * pair_separation / 2
            data["links"][link_id_2]["xmid"] = data["links"][link_id_2]["xmid"] + math.cos(vector_angle - math.pi/2) * pair_separation / 2
            data["links"][link_id_2]["ymid"] = data["links"][link_id_2]["ymid"] + math.sin(vector_angle - math.pi/2) * pair_separation / 2                
    for i in Link.objects.filter(version=version):
        i.xmid = data["links"][i.id]["xmid"]
        i.ymid = data["links"][i.id]["ymid"]
        i.save()

def start_mid(data, from_node, to_node):

    x = (data["nodes"][from_node]["xpos"] + data["nodes"][to_node]["xpos"]) / 2
    y = (data["nodes"][from_node]["ypos"] + data["nodes"][to_node]["ypos"]) / 2

    return x, y  

# Backup

@login_required    
def take_snapshot(request):
    [version, state, currentversion] = current_version(request)
    data = {}

    models = django.apps.apps.get_models(include_auto_created=True, include_swapped=True)

    data = {}
    for i in models:
        if i.__name__ in ["Category", "Node", "Link", "NetworkParam", "GanttParam", "Loop", "Grouped"]:
            data[i.__name__] = []
            for j in i.objects.filter(version=version):
                obj = {}
                
                for k in j._meta.fields:
                    if i._meta.get_field(k.name).get_internal_type() == "ForeignKey":
                        if k.name != "copied_to" and k.name != "version":
                            obj[k.name] = getattr(j, k.name).id
                    else:
                        if k.name != "copied_to" and k.name != "version":
                            obj[k.name] = getattr(j, k.name)

                data[i.__name__].append(obj)
        # elif i.__name__ in ["Loop_links"]:
        #     data[i.__name__] = []
        #     for j in Loop.objects.filter(version=version):
        #         for k in i.objects.filter(loop=j):
        #             obj = {}
        #             for l in k._meta.fields:                   
        #                 if i._meta.get_field(l.name).get_internal_type() == "ForeignKey":
        #                     obj[l.name] = getattr(k, l.name).id   
        #                 else:
        #                     obj[l.name] = getattr(k, l.name)
        #             data[i.__name__].append(obj)            

    return data

@login_required
def reverse_snapshot(request, data):

    [version, state, currentversion] = current_version(request)
    models = [Category, Node, Link, Loop, Grouped, NetworkParam, GanttParam]
    for i in models:
        for j in i.objects.filter(version=version):
            j.delete()
    for i in models:
        obj = i()
        obj.version = version
        for j in data[i.__name__]:
            for k in obj._meta.fields:
                if k.name in ["copied_to", "version"]:
                    continue
                if i._meta.get_field(k.name).get_internal_type() == "ForeignKey":
                    ref_model = i._meta.get_field(k.name).related_model
                    ref = ref_model.objects.get(id=j[k.name])
                    setattr(obj, k.name, ref)
                else:
                    setattr(obj, k.name, j[k.name])
            obj.save()

@login_required
def do_undo(request, backup, restore, data_last):

    if len(restore) == 0:
        if len(backup) > 1: 
            restore.append(backup.pop())
        # data = take_snapshot(request)
        # data_old = copy.deepcopy(data)
        # temp = backup.pop()
        # data = data + temp[1]
        # restore.append([temp[0], Delta(DeepDiff(data, data_old))])
        # data_last = copy.deepcopy(data)
    if len(backup) > 1:
        
        data = backup.pop()
        restore.append(data)
        reverse_snapshot(request, data)
    elif len(backup) == 1:
        data = backup[0]

        reverse_snapshot(request, data)


        # updateloops(request)

    return backup, restore, data_last

@login_required
def do_redo(request, backup, restore, data_last):

    if len(backup) == 0:
        if len(restore) > 1:
            backup.append(restore.pop())
        # if len(backup) == 0:
        #     backup.append(restore.pop())
        # data = take_snapshot(request)
        # data_old = copy.deepcopy(data)
        # temp = restore.pop()
        # data = data + temp[1]
        # backup.append([temp[0], Delta(DeepDiff(data, data_old))])     
        # data_last = copy.deepcopy(data)

    if len(restore) > 0:        
        data = restore.pop()
        backup.append(data)

        reverse_snapshot(request, data) 
        # updateloops(request)   

    return backup, restore, data_last

@login_required
def add_backup(request, action):
    global backup, restore, data_last 
    [version, state, currentversion] = current_version(request)
    data = take_snapshot(request)

    if currentversion.history != None:

        history = pickle.loads(currentversion.history)
        backup, restore, data_last = history[0], history[1], history[2]
    else:
            data_last = {}
            backup = []

    # delta = Delta(DeepDiff(data, data_last))
    # backup.append([action, delta])

    backup.append(data)
    if len(backup) > 20: backup.pop(0)
    data_last = copy.deepcopy(data)

    currentversion.history = pickle.dumps([backup, [], data_last])
    currentversion.save()

    return

# Gantt

@login_required
def disable_redundant_links(request):
    [version, state, currentversion] = current_version(request)
    
    def disable_red(level):
        links = list(Link.objects.filter(version=version, enabled=True))
        nodes = list(Node.objects.filter(version=version, enabled=True))
        categories = list(Category.objects.filter(version=version, enabled=True))

        for i in links:
            if i.from_node not in nodes or i.to_node not in nodes or i.from_node.category not in categories or i.to_node.category not in categories:
                links.remove(i)
        goals = list(filter(lambda x: x.category.category_code == ">", nodes))
        
        link_levels = {}

        for i in links:
            if i.to_node in goals:
                link_levels[i] = 0
        
        while True:
            found = False
            for i in list(link_levels.keys()):
                for j in links:
                    if j in link_levels.keys(): continue
                    if j.to_node == i.from_node:
                        found = True
                        link_levels[j] = link_levels[i] - 1

            if found == False: break

        min_level = min(link_levels.values())
        max_chain_length = level - min_level

        link_list = [i for i in link_levels.keys() if link_levels[i] == level]
        
        for i in link_list:
            chains = []
            for j in list(filter(lambda x: x.to_node == i.to_node and x != i, links)):
                chains.append([j])
            if len(chains) == 0: continue

            chain_length = 1
            while chain_length <=max_chain_length:

                chain_length += 1
                found = False
                indirect_link = False
                for j in chains:
                    chain_to_nodes = [x.to_node for x in j]
                    for k in list(filter(lambda x: x.to_node == j[0].from_node and x != i and x not in j and x.from_node not in chain_to_nodes, links)):
                        found = True
                        if k.from_node == i.from_node:
                            # Link.objects.get(version=version, from_node = k.from_node, to_node= j[-1].to_node).delete()
                            link = Link.objects.get(version=version, from_node = k.from_node, to_node= j[-1].to_node)
                            link.enabled = False
                            link.save()
                            
                            indirect_link = True
                        
                        else:
                            chains.append([k] + j)
                        break
                    if indirect_link: break
                
                if indirect_link: break
                if not found: break

        if level > min_level + 1:
            disable_red(level - 1)
            return
        else:
            return
    disable_red(0)

def get_sequence(links_in_order, nodes_to_goals, group_dict_lookup, node_dict_lookup):

    # Generate sequences by iteratively moving nodes + all dependent nodes if link out of sequence until all links in sequence

    def move_dependants(sequence, links_in_order, node, direction, amount):
        if direction == -1:
            dependants = list(filter(lambda x: x[1] == node[0], list(sequence.keys())))
        else:
            dependants = list(filter(lambda x: x[0] == node[1], list(sequence.keys())))
        if len(dependants) > 0:
            for i in dependants:
                sequence[i] = sequence[i] + direction * amount
                move_dependants(sequence, links_in_order, i, direction, amount)
        return sequence

    latest_sequence = {i: 0 for i in nodes_to_goals}
    while True:
        found=False
        # for i in list(filter(lambda x: latest_sequence[x[0]] >= latest_sequence[x[1]], links_in_order)):
        for i in links_in_order:
            if latest_sequence[i[0]] >= latest_sequence[i[1]]:
                latest_sequence[i[0]] = latest_sequence[i[1]] - 1
                latest_sequence = move_dependants(latest_sequence, links_in_order, i, -1, 1)
                found = True
        if found == False:
            break
  
    min_sequ = min(latest_sequence.values())
    for i in latest_sequence.keys():
        latest_sequence[i] -= min_sequ

    earliest_sequence = {i: 0 for i in nodes_to_goals}
    while True:
        found=False
        # for i in list(filter(lambda x: earliest_sequence[x[0]] >= earliest_sequence[x[1]], links_in_order)):
        for i in links_in_order:
            if earliest_sequence[i[0]] >= earliest_sequence[i[1]]:
                earliest_sequence[i[1]] = earliest_sequence[i[0]] + 1
                earliest_sequence = move_dependants(earliest_sequence, links_in_order, i, 1, 1)
                found = True
        if found == False:
            break

    durations = {}
    for i in nodes_to_goals:
        if i[:1] == "N":
            durations[i] = node_dict_lookup[i].duration
        elif i[:1] == "G":
            durations[i] = group_dict_lookup[i].duration

    earliest_sequence_dur = {i: 0 for i in nodes_to_goals}
    latest_sequence_dur = {i: 0 for i in nodes_to_goals}

    while True:
        found=False
        # for i in list(filter(lambda x: earliest_sequence_dur[x[0]] + durations[x[0]]> earliest_sequence_dur[x[1]], links_in_order)):
        for i in links_in_order:
            if earliest_sequence_dur[i[0]] + durations[i[0]]> earliest_sequence_dur[i[1]]:
                earliest_sequence_dur[i[1]] = earliest_sequence_dur[i[0]] + durations[i[0]]
                earliest_sequence_dur = move_dependants(earliest_sequence_dur, links_in_order, i, 1, durations[i[0]])
                found = True
        if found == False:
            break
    
    while True:
        found=False
        # for i in list(filter(lambda x: latest_sequence_dur[x[0]] + durations[x[0]]> latest_sequence_dur[x[1]], links_in_order)):
        for i in links_in_order:
            if latest_sequence_dur[i[0]] + durations[i[0]]> latest_sequence_dur[i[1]]:
                latest_sequence_dur[i[0]] = latest_sequence_dur[i[1]] - durations[i[0]]
                latest_sequence_dur = move_dependants(latest_sequence_dur, links_in_order, i, -1, durations[i[0]])
                found = True
        if found == False:
            break
    
    min_sequ = min(latest_sequence_dur.values())
    for i in latest_sequence_dur.keys():
        latest_sequence_dur[i] -= min_sequ 
    
    return latest_sequence, earliest_sequence, latest_sequence_dur, earliest_sequence_dur, durations

def djikstra(loop_list_copy):
    
    links_out_order_dict = {}
    loop_links = []

    for i in loop_list_copy:
        for j in i:
            if tuple(j) not in loop_links:
                loop_links.append(tuple(j)) 

    count_max = len(loop_links)
    for i in loop_links:
        loop_list_temp = copy.deepcopy(loop_list_copy)

        for j in loop_list_copy:
            if list(i) in j:
                if j in loop_list_temp:
                    loop_list_temp.remove(j)
        if len(loop_list_temp) > 0:
            links_out_order_dict[tuple([i])] = False
        else:
            links_out_order_dict[tuple([i])] = True
            count_max = 1
    
    if count_max > 1:
        while True:
            found = False
            for i in list(filter(lambda x: not(links_out_order_dict[x]) and (len(list(x)) < count_max), links_out_order_dict.keys())):
                for j in loop_links:
                    if j in list(i): continue
                    if set(list(i)+[j]) in [set(k) for k in links_out_order_dict.keys()]: continue
                    found = True
                    loop_list_temp = copy.deepcopy(loop_list_copy)
                    for k in list(i)+[tuple(j)]:
                        for l in loop_list_copy:
                            if list(k) in l:
                                if l in loop_list_temp:
                                    loop_list_temp.remove(l)
                    if len(loop_list_temp) > 0:
                        links_out_order_dict[tuple(list(i)+[tuple(j)])] = False

                    else:
                        links_out_order_dict[tuple(list(i)+[tuple(j)])] = True
                        if len(tuple(list(i)+[tuple(j)])) < count_max:
                            count_max = len(tuple(list(i)+[tuple(j)]))
                            for i in list(filter(lambda x: len(x) > count_max, links_out_order_dict.keys())):
                                del links_out_order_dict[i]
                    
            if found == False: break

    links_out_order_list = list(filter(lambda x: links_out_order_dict[x] and len(x)==count_max,links_out_order_dict.keys()))
    return(links_out_order_list)

def get_group_info_dict(group_dict):
    group_info_dict={}
    for i in group_dict.keys():
        group_info_dict[i] = {}
        node_text_list = []
        node_code_list = []
        node_id_list = []
        link_id_list = []
        for j in group_dict[i]:
            for k in j.links.all():
                node_code = k.from_node.category.category_code + k.from_node.node_code
                node_text = k.from_node.category.category_code + k.from_node.node_code + ": " + k.from_node.node_text
                node_id = k.from_node_id
                link_id = k.id
                if node_code not in node_code_list:
                    node_code_list.append(node_code)
                    node_text_list.append(node_text)
                    node_id_list.append(node_id)
                if link_id not in link_id_list:
                    link_id_list.append(link_id)

        node_code_list.sort()
        node_text_list.sort()
        group_info_dict[i]["node_code_list"] = node_code_list
        group_info_dict[i]["node_text_list"] = node_text_list
        group_info_dict[i]["node_id_list"] = node_id_list
        group_info_dict[i]["link_id_list"] = link_id_list
    return(group_info_dict)

@login_required
def get_loop_func(request, apply_groups, enabled_only, link_list_full):
    [version, state, currentversion] = current_version(request)
    if apply_groups:    
        if enabled_only:
            loops = list(Loop.objects.filter(version=version, enabled=True, group=False))
        else:
            loops = list(Loop.objects.filter(version=version, group=False))
    else:
        if enabled_only:
            loops = list(Loop.objects.filter(version=version, enabled=True))
        else:
            loops = list(Loop.objects.filter(version=version))  

    for loop in list(loops):
        for link in loop.links.all():
            if link not in link_list_full:
                loops.remove(loop)
                break
    
    return loops

@login_required
def build_gantt(request, gantt_num):
    [version, state, currentversion] = current_version(request)
    
    if gantt_num == 0:
        if NetworkParam.objects.get(version=version).Model_choice == "AC":
            if GanttParam.objects.get(version=version).Apply_groups:
                updateloops(request)
                updategroups(request)

        colour_dict = create_colour_dict(request)
        params = {}

        # Create params with no django objects for export to client

        for i in gantt_lookup.keys():
            if type(gantt_lookup[i]).__name__ == "list":
                params[gantt_lookup[i][0]] = getattr(GanttParam.objects.get(version=version), gantt_lookup[i][0]).option
            else:
                params[gantt_lookup[i]] = getattr(GanttParam.objects.get(version=version), gantt_lookup[i])

        # Get enabled only / apply group settings

        gantt_params = GanttParam.objects.get(version=version)

        enabled_only = gantt_params.Enabled_only
        apply_groups = gantt_params.Apply_groups

        # Get links and nodes
        link_list, node_list, node_dict, node_dict_lookup = get_links_nodes(request, enabled_only)
        link_list_full = copy.deepcopy(link_list)
        colour_lookup = {node_dict[i]: colour_dict[i.category] for i in node_list}
        
        # Apply groups

        if apply_groups:
            group_dict, goal_codes, link_list, node_dict, group_dict_lookup = apply_groups_func(request, enabled_only, node_list, node_dict, link_list)

        # Else generate objects without groups

        else:
            link_list = [[node_dict[i.from_node], node_dict[i.to_node]] for i in link_list]
            goal_codes = []
            for i in node_dict.keys():
                if node_dict[i][:1] == "N":
                    if i.category.category_code == ">":
                        goal_codes.append(node_dict[i])       
            # group_code_list=[]
            group_dict = {}
            group_dict_lookup = {}

        # Start chain list with links to goals

        chains = {}
        for i in link_list:
            if i[1] in goal_codes:
                chains[(tuple(i))] = True

        # Add links to generate remaining chains, using flag to mark where chain complete and no further links available

        while True:
            found = False
            for i in list(chains.keys()):
                if chains[i] == False: continue
                for j in link_list:
                    if i[0] != j[1]: continue
                    if j[0] in list(i): continue
                    if tuple([j[0]]+list(i)) in chains.keys():
                        continue              
                    chains[tuple([j[0]]+list(i))] = True
                    found = True
                if found == False:
                    chains[i] == False
            if found == False:
                break
        
        # Turn chain dict of tuples into chain list of lists

        chains_list = []
        for i in chains.keys():
            chain = []
            for j in range(len(i)-1):
                chain.append([i[j], i[j+1]])
            chains_list.append(chain)

        chains = chains_list
        
        # From chains identify links and nodes connected to goals

        links_to_goals = []

        nodes_to_goals = [node_dict[i] for i in list(filter(lambda x: x.category.category_code == ">", node_list))]

        for i in chains:
            for j in i:
                if j not in links_to_goals:
                    links_to_goals.append(j)
                    for k in j:
                        if k not in nodes_to_goals:
                            nodes_to_goals.append(k)

        # Get loops not in groups

        loops = get_loop_func(request, apply_groups, enabled_only, link_list_full)

        links_in_order = links_to_goals
        links_out_order = []
        gantt_tot = 1
        links_out_order_list = []

        if len(loops) > 0:

            loop_list = []

            # Get remaining links in loops after groups applied

            for i in loops:
                links_list = []
                for j in i.links.all():
                    if j.from_node in node_dict.keys() and j.to_node in node_dict.keys():        
                        if node_dict[j.from_node] !=  node_dict[j.to_node]:
                            links_list.append([node_dict[j.from_node], node_dict[j.to_node]])
                        
                if len(links_list)> 0:
                    if links_list not in loop_list:
                        loop_list.append(links_list)
            
            # Find variant list of optimum links out order (=minimum number of links possible) if loops remaining

            if len(loop_list) > 0:
                loop_list_copy = copy.deepcopy(loop_list)

                links_out_order_list = djikstra(loop_list_copy)

                gantt_tot = len(links_out_order_list)

                if gantt_num >= gantt_tot: gantt_num = 0
                if gantt_num < 0: gantt_num = len(gantt_tot) - 1

                # Set links in order to for first Gantt variant

                links_out_order = [list(i) for i in links_out_order_list[gantt_num]]
                
                links_in_order = copy.deepcopy(links_to_goals)
                for i in links_out_order:
                    if i in links_in_order:
                        links_in_order.remove(i)

        # get node, group info and colour_ref for sending to client

        node_id_dict = {node_dict[i]: i.id for i in node_dict.keys()}

        group_info_dict = get_group_info_dict(group_dict)

        nodes_rev_dict = {}

        for i in set(node_dict.values()):
            nodes_rev_dict[i] = []
        
        for i in node_dict.keys():
            nodes_rev_dict[node_dict[i]].append(i.category.category_code + i.node_code + ": " + i.node_text)

        group_id_dict = {i: group_dict_lookup[i].id for i in group_dict_lookup.keys()}

        colour_ref = {i.category_code + ": " + i.category_text: colour_dict[i] for i in colour_dict.keys()}

        # Save to buffer to avoid regenerating for each Gantt variant

        currentversion.gantt_buffer = pickle.dumps([nodes_to_goals, group_dict_lookup, node_dict_lookup, params, colour_lookup, group_info_dict, node_dict, colour_dict, node_id_dict, [gantt_tot], links_out_order_list, links_to_goals, nodes_rev_dict, group_id_dict, colour_ref])
        currentversion.save()
    
    else:

        # Load from buffer

        [nodes_to_goals, group_dict_lookup, node_dict_lookup, params, colour_lookup, group_info_dict, node_dict, colour_dict, node_id_dict, [gantt_tot], links_out_order_list, links_to_goals, nodes_rev_dict, group_id_dict, colour_ref] = pickle.loads(currentversion.gantt_buffer)

        # Enable scrolling through gantt variants past total gantt_num and zero

        if gantt_num >= gantt_tot: gantt_num = 0
        if gantt_num < 0: gantt_num = len(gantt_tot) - 1
        
        # Get links in order for selected Gantt variant

        links_out_order = [list(i) for i in links_out_order_list[gantt_num]]
        links_in_order = copy.deepcopy(links_to_goals)
        for i in links_out_order:
            if i in links_in_order:
                links_in_order.remove(i)
    
    # Get sequences for selected Gantt variant

    latest_sequence, earliest_sequence, latest_sequence_dur, earliest_sequence_dur, durations = get_sequence(links_in_order, nodes_to_goals, group_dict_lookup, node_dict_lookup)

    gantt_data = [earliest_sequence, latest_sequence, earliest_sequence_dur, latest_sequence_dur, nodes_rev_dict, durations, params, colour_lookup, links_out_order, colour_ref, group_info_dict]

    return gantt_data, params, node_id_dict, group_id_dict, gantt_num, gantt_tot

@login_required
def build_gantt_alternative(request):
    [version, state, currentversion] = current_version(request)
    colour_dict = create_colour_dict(request)

    # Generate params for sending to client

    params = {}
    for i in gantt_lookup.keys():
        if type(gantt_lookup[i]).__name__ == "list":
            params[gantt_lookup[i][0]] = getattr(GanttParam.objects.get(version=version), gantt_lookup[i][0]).option
        else:
            params[gantt_lookup[i]] = getattr(GanttParam.objects.get(version=version), gantt_lookup[i])

    # Get enabled only setting
    gantt_params = GanttParam.objects.get(version=version)
    enabled_only = gantt_params.Enabled_only

    # Get links and nodes
    links, nodes, node_dict, node_dict_lookup = get_links_nodes(request, enabled_only)
    
    # Sort links according to number of connections to to_node, giving high probability of returning min or near min number of links out of order

    links_conn_dict = {}

    for i in links:
        links_conn_dict[i] = 0
        for j in links:
            if i==j: continue
            # if i.to_node == j.from_node:
            #     links_conn_dict[i] +=1
            if i.from_node == j.to_node:
                links_conn_dict[i] +=1            

    links = sorted(links, key = lambda x: links_conn_dict[x])


    # Get active nodes and links without loops for creating sequences

    active_nodes, active_links = get_active(request, nodes, links)

    # Generate sequences

    links_in_order = [[node_dict[i.from_node], node_dict[i.to_node]] for i in active_links]
    nodes_to_goals = [node_dict[i] for i in active_nodes]

    latest_sequence, earliest_sequence, latest_sequence_dur, earliest_sequence_dur, durations = get_sequence(links_in_order, nodes_to_goals, {}, node_dict_lookup)

    # Get durations

    durations = {}

    for i in nodes:
        durations[i] = i.duration

    ## Alternative sequence generation without moving dependants

    # latest_sequence = {i: 0 for i in active_nodes}

    # while True:
    #     found=False
    #     for i in active_links:
    #         if latest_sequence[i.from_node] >= latest_sequence[i.to_node]:
    #             latest_sequence[i.from_node] = latest_sequence[i.to_node] - 1
    #             found = True
    #     if found == False:
    #         break
    # min_sequ = min(latest_sequence.values())
    # for i in latest_sequence.keys():
    #     latest_sequence[i] -= min_sequ

    # earliest_sequence = {i: 0 for i in active_nodes}
    # while True:
    #     found=False
    #     for i in active_links:
    #         if earliest_sequence[i.from_node] >= earliest_sequence[i.to_node]:
    #             earliest_sequence[i.to_node] = earliest_sequence[i.from_node] + 1
    #             found = True
    #     if found == False:
    #         break
    
    # earliest_sequence_dur = {i: 0 for i in active_nodes}
    # latest_sequence_dur = {i: 0 for i in active_nodes}

    # while True:
    #     found=False
    #     for i in active_links:
    #         if earliest_sequence_dur[i.from_node] + durations[i.from_node]> earliest_sequence_dur[i.to_node]:
    #             earliest_sequence_dur[i.to_node] = earliest_sequence_dur[i.from_node] + durations[i.from_node]
    #             found = True
    #     if found == False:
    #         break
    # while True:
    #     found=False
    #     for i in active_links:
    #         if latest_sequence_dur[i.from_node] + durations[i.from_node]> latest_sequence_dur[i.to_node]:
    #             latest_sequence_dur[i.from_node] = latest_sequence_dur[i.to_node] - durations[i.from_node]
    #             found = True
    #     if found == False:
    #         break
    
    # min_sequ = min(latest_sequence_dur.values())
    # for i in latest_sequence_dur.keys():
    #     latest_sequence_dur[i] -= min_sequ 

    # node_dict = {}
    # counter = 0
    # for i in nodes:
    #     node_dict[i] = "N" + str(counter)
    #     counter +=1

    # latest_sequence = {node_dict[i]: latest_sequence[i] for i in latest_sequence.keys()}
    # earliest_sequence = {node_dict[i]: earliest_sequence[i] for i in earliest_sequence.keys()}
    # latest_sequence_dur = {node_dict[i]: latest_sequence_dur[i] for i in latest_sequence_dur.keys()}
    # earliest_sequence_dur = {node_dict[i]: earliest_sequence_dur[i] for i in earliest_sequence_dur.keys()}


    # Create other required data for sending to client

    node_id_dict = {node_dict[i]: i.id for i in node_dict.keys()}

    colour_lookup = {node_dict[i]: colour_dict[i.category] for i in nodes}

    nodes_rev_dict = {}

    for i in set(node_dict.values()):
        nodes_rev_dict[i] = []
    
    for i in node_dict.keys():
        nodes_rev_dict[node_dict[i]].append(i.category.category_code + i.node_code + ": " + i.node_text)

    colour_ref = {i.category_code + ": " + i.category_text: colour_dict[i] for i in colour_dict.keys()}
    colour_dict = create_colour_dict(request)

    out_order = list(filter(lambda x: x not in active_links, links))
    for i in list(out_order):
        if i.from_node not in active_nodes.keys() or i.to_node not in active_nodes.keys():
            out_order.remove(i)

    links_out_order = [[node_dict[i.from_node], node_dict[i.to_node]] for i in out_order]

    durations = {node_dict[i]: durations[i] for i in durations.keys()}

    gantt_data = [earliest_sequence, latest_sequence, earliest_sequence_dur, latest_sequence_dur, nodes_rev_dict, durations, params, colour_lookup, links_out_order, colour_ref]
    
    group_id_dict = {}
    
    return gantt_data, params, node_id_dict, group_id_dict, 0, 1

@login_required
def get_active(request, nodes, links):
    
    [version, state, currentversion] = current_version(request)
    goals = list(filter(lambda x: x.category.category_code == ">", nodes))
    
    active_links = []
    active_nodes = {}
    
    for i in goals:
        active_nodes[i] = 0
        
        for j in filter(lambda x: x.to_node == i and x.from_node not in goals, links):
            active_links.append(j)
            if j.from_node not in active_nodes:
                active_nodes[j.from_node] = -1
    
    counter = -2
    while True:
        found = False
        for i in list(active_links):
            for j in filter(lambda x: x.to_node == i.from_node, links):
                if j.from_node in active_nodes.keys(): continue
                if j in active_links: continue
                active_links.append(j)
                active_nodes[j.from_node] = counter
                found = True
        counter -= 1
        if found == False: break

    for i in links:
        if i not in active_links and i.from_node in active_nodes.keys() and i.to_node in active_nodes.keys():

            if active_nodes[i.from_node] < active_nodes[i.to_node]:
                active_links.append(i)
                continue
            success = False
            active_nodes_temp = copy.deepcopy(active_nodes)
            active_links_temp = copy.deepcopy(active_links)
            active_links_temp.append(i)   
            max_steps = len(active_links_temp)    
            while True:
                found=False
                for j in active_links_temp:
                    if  active_nodes_temp[j.from_node] >=  active_nodes_temp[j.to_node]:
                        active_nodes_temp[j.from_node] =  active_nodes_temp[j.to_node] - 1
                        found = True
                if found == False and min(active_nodes_temp.values()) > - len(set(active_nodes_temp.values())):    
                    success = True
                    break
                if min(active_nodes_temp.values()) <= - len(set(active_nodes_temp.values())) or max(active_nodes_temp.values()) < 0:

                # if min(active_nodes_temp.values()) < - max_steps:
                    break
            if success == True:

                seq_vals = list(set(list(active_nodes_temp.values())))
                min_seq_val = min(seq_vals)
                for j in range(0, min_seq_val - 1, - 1):
                    if j not in seq_vals:
                        for k in active_nodes_temp.keys():
                            if active_nodes_temp[k] < j:
                                active_nodes_temp[k] +=1

                active_nodes = copy.deepcopy(active_nodes_temp)
                active_links.append(i)
    


    return active_nodes, active_links

@login_required
def apply_groups_func(request, enabled_only, node_list, node_dict, link_list):
        [version, state, currentversion] = current_version(request)
        # groups, enabled_groups = group_data()

        groups = {i.id: [j for j in i.loops.all()] for i in list(Grouped.objects.filter(version=version))}

        group_dict  = {}
        group_dict_lookup = {}

        node_rem_list = []
        for i0 in groups.keys():
            i = groups[i0]
            for j in i:
                for k in j.links.all():
                    node_rem_list.append(k.from_node)
        node_rem_list = list(set(node_rem_list))
        for i in node_rem_list:
            node_list.remove(i)
        group_code_list = []
        for i0 in groups.keys():
            i = groups[i0]
            group_code_list.append([get_loop_code(j) for j in i])

        group_dict = {}
        counter = 0
        for i0 in groups.keys():
            i = groups[i0]
            n = []
            for j in i:
                if j not in n:
                    n.append(j)
            group_dict["G" + str(counter)] = n
            group_dict_lookup["G" + str(counter)] = Grouped.objects.get(id=i0)
            counter +=1    
        
        for i in group_dict.keys():
            for j in group_dict[i]:
                for k in j.links.all():
                    node_dict[k.from_node] = i

        rev_link_list = []
        for i in link_list:
            if node_dict[i.from_node] == node_dict[i.to_node]:
                continue
            new_link = [node_dict[i.from_node], node_dict[i.to_node]]
            if new_link not in rev_link_list:
                rev_link_list.append(new_link)
        link_list = rev_link_list

        goal_codes = []
        for i in node_dict.keys():
            if node_dict[i][:1] == "N":
                if i.category.category_code == ">":
                    goal_codes.append(node_dict[i])
            else:
                for j in group_dict[node_dict[i]]:
                    for k in j.links.all():
                        if k.from_node.category.category_code == ">":
                            if node_dict[i] not in goal_codes:
                                goal_codes.append(node_dict[i])

        return group_dict, goal_codes, link_list, node_dict, group_dict_lookup

@login_required
def get_links_nodes(request, enabled_only):
    [version, state, currentversion] = current_version(request)
    if enabled_only:
        node_list = list(Node.objects.filter(version=version, enabled=True, connected_to_goal_enabled=True))
        for i in list(node_list):
            if i.category.enabled == False:
                node_list.remove(i)
        link_list = list(Link.objects.filter(version=version, enabled=True))
        for i in list(copy.deepcopy(link_list)):
            if i.from_node not in node_list or i.to_node not in node_list:
                link_list.remove(i)
    
    else:
        node_list = list(Node.objects.filter(version=version, connected_to_goal=True))
        link_list = list(Link.objects.filter(version=version))
        for i in list(copy.deepcopy(link_list)):
            if i.from_node not in node_list or i.to_node not in node_list:
                link_list.remove(i)        
    
    node_dict = {}
    node_dict_lookup = {}
    counter = 0
    for i in node_list:
        node_dict[i] = "N" + str(counter)
        node_dict_lookup["N" + str(counter)] = i
        counter +=1
    return link_list, node_list, node_dict, node_dict_lookup

@login_required
def goal_connections(request, enabled_only):
    [version, state, currentversion] = current_version(request)

    # links, nodes, node_dict, node_dict_lookup = get_links_nodes(request, enabled_only)

    if enabled_only:
        nodes = list(Node.objects.filter(version=version, enabled=True))
        for i in list(nodes):
            if i.category.enabled == False:
                nodes.remove(i)
        links = list(Link.objects.filter(version=version, enabled=True))
        for i in list(links):
            if i.from_node not in nodes or i.to_node not in nodes:
                links.remove(i)
    else:
        nodes = list(Node.objects.filter(version=version))
        links = list(Link.objects.filter(version=version))
    
    active_nodes, active_links = get_active(request, nodes, links)

    # goals = list(filter(lambda x: x.category.category_code == ">",nodes))

    # active_links = []
    # active_nodes = {}
    
    # for i in goals:
    #     active_nodes[i] = 0
        
    #     for j in filter(lambda x: x.to_node == i, links):
    #         active_links.append(j)
    #         if j.from_node not in active_nodes:
    #             active_nodes[j.from_node] = -1

    # counter = -2
    # while True:
    #     found = False
    #     for i in list(active_links):
    #         for j in filter(lambda x: x.to_node == i.from_node, links):
    #             if j.from_node in active_nodes.keys(): continue
    #             if j in active_links: continue
    #             active_links.append(j)
    #             active_nodes[j.from_node] = counter
    #             found = True
    #     counter -= 1
    #     if found == False: break

    connected_node_list = list(active_nodes.keys())
    for i in list(Node.objects.filter(version=version)):
        if i in connected_node_list:
            if enabled_only:
                i.connected_to_goal_enabled = True
            else:
                i.connected_to_goal = True
        else:
            if enabled_only:
                i.connected_to_goal_enabled = False
            else:
                i.connected_to_goal = False
        i.save()            

# File import / export

def import_data(import_data, version):

    for i in import_data["nodes"].keys():
        category = Category.objects.create(category_text=i[i.find(" ")+3:], category_code=i[:i.find(" ")], version=version)
        for j in import_data["nodes"][i]:
            node_code = j[1:j.find(" ")]
            node_text = j[j.find(" ")+3:]
            node = Node.objects.create(category=category, node_text=node_text, node_code=node_code, version=version)
            node_data = import_data["node_data"][get_node_code(j)]
            for k in node_data.keys():
                setattr(node, k, node_data[k])
                node.save()

    for i in import_data["links"]:

        from_node = Node.objects.get(node_text=i[0][i[0].find(" ")+3:], node_code=i[0][1: i[0].find(" ")], category=Category.objects.get(version=version, category_code=i[0][:1]), version=version)
        to_node = Node.objects.get(node_text=i[1][i[1].find(" ")+3:], node_code=i[1][1: i[1].find(" ")], category=Category.objects.get(version=version, category_code=i[1][:1]), version=version)
        link = Link.objects.create(from_node=from_node, to_node=to_node, version=version)
        link_data = import_data["link_data"][get_link_code(i)]
        link.save()
        for j in link_data.keys():
            setattr(link, j, link_data[j])
            link.save()        
       
    network_params = NetworkParam.objects.create(version=version)
    gantt_params = GanttParam.objects.create(version=version)

    for i in network_lookup.keys():
        if i not in network_export: continue
        if type(network_lookup[i]).__name__ == "list":
            setattr(network_params, network_lookup[i][0], network_lookup[i][1].objects.get(option=import_data["network_params"][i][0]))
        else:
            setattr(network_params, network_lookup[i], import_data["network_params"][i])
    network_params.save()

    for i in gantt_lookup.keys():
        if i not in gantt_export: continue
        if type(gantt_lookup[i]).__name__ == "list":
            setattr(gantt_params, gantt_lookup[i][0], gantt_lookup[i][1].objects.get(option=import_data["gantt_params"][i][0]))
        else:
            setattr(gantt_params, gantt_lookup[i], import_data["gantt_params"][i])
    gantt_params.save()

@login_required
def export_data(request):
    data = {"nodes": {}, "links": [], "node_data": {}, "link_data": {}, "category_data": {}, "loops": {}, "network_params": {}, "gantt_params":{}}

    [version, state, currentversion] = current_version(request)
    if version == None:
        return
    categories = sorted(Category.objects.filter(version=version), key = lambda x: x.category_code)
    links = Link.objects.filter(version=version)

    for i in categories:
        category = i.category_code + " - " + i.category_text
        data["nodes"][category] = []
        cat_nodes = Node.objects.filter(version=version, category=i)
        fields = ["enabled", "notes"]
        data["category_data"][category] = {}
        for j in fields:
            data["category_data"][category][j] = getattr(i, j)

        for j in cat_nodes:
            node = i.category_code + j.node_code + " - " + j.node_text
            node_code = i.category_code + j.node_code
            data["nodes"][category].append(node)
            fields  = ["weight", "duration", "enabled", "notes", "xpos", "ypos", "placed"]
            data["node_data"][node_code] = {}
            for k in fields:
                data["node_data"][node_code][k] = getattr(j, k)

    for i in links:
        link = [(i.from_node.category.category_code + i.from_node.node_code + " - " + i.from_node.node_text), (i.to_node.category.category_code + i.to_node.node_code + " - " + i.to_node.node_text)]
        link_code = (i.from_node.category.category_code + i.from_node.node_code + "-" + i.to_node.category.category_code + i.to_node.node_code)
        fields  = ["weight", "enabled", "notes", "xmid", "ymid", "in_loop", "in_group", "in_enabled_loop", "in_enabled_group"]
        data["links"].append(link)
        data["link_data"][link_code] = {}
        for j in fields:
            data["link_data"][link_code][j] = getattr(i, j)

    for i in network_lookup.keys():
        if i not in network_export: continue
        if type(network_lookup[i]).__name__ == "list":
            data["network_params"][i] = ["",[]]
            options = network_lookup[i][1].objects.all()
            for j in options:
                data["network_params"][i][1].append(j.option)
            data["network_params"][i][0] = getattr(NetworkParam.objects.get(version=version), network_lookup[i][0]).option
        else:
            data["network_params"][i] = getattr(NetworkParam.objects.get(version=version), network_lookup[i])

    for i in gantt_lookup.keys():
        if i not in gantt_export: continue
        if type(gantt_lookup[i]).__name__ == "list":
            data["gantt_params"][i] = ["",[]]
            options = gantt_lookup[i][1].objects.all()
            for j in options:
                data["gantt_params"][i][1].append(j.option)
            data["gantt_params"][i][0] = getattr(GanttParam.objects.get(version=version), gantt_lookup[i][0]).option
        else:
            data["gantt_params"][i] = getattr(GanttParam.objects.get(version=version), gantt_lookup[i])
    return data 

@login_required
def import_csv(request, importfile):
    [version, state, currentversion] = current_version(request)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    counter0 = 0
    counter1 = 0
    for row in importfile:
        countertext = str(alphabet[counter0]) + str(alphabet[counter1])

        if len(row) == 0:
            continue
        if len(row[0]) == 0:
            continue
        if row[0][1:4] == " - ":
            if row[0][4:] == "Goals":
                category = "> - Goals"
            else:
                category = row[0]
            if category not in [i.category_code + " - " + i.category_text for i in Category.objects.filter(version=version)]:
                newcat = Category.objects.create(version=version, category_code=row[0][:1], category_text=row[0][4:])
                newcat.save()
            else:
                newcat = Category.objects.filter(version=version, category_text=row[0][4:])[0]
            continue

        if row[0] not in [i.node_text for i in Node.objects.filter(version=version, category=newcat)]:
            newnode = Node.objects.create(version=version, node_code=countertext, node_text=row[0], category=newcat)
            newnode.save()

        if counter1 < len(alphabet) - 1:
            counter1 +=1
            continue
        elif counter0 == len(alphabet) - 1:
            return
        else:
            counter1 = 0
            counter0 +=1

@login_required
def import_link_csv(request, importfile, mincount):
    [version, state, currentversion] = current_version(request)
    # if os.path.splitext(importfile)[1] == ".csv":
    link_import_df = pd.read_csv(importfile)
    headers = link_import_df.columns.values

    # links = Link.objects.filter(version=version)
    nodes = Node.objects.filter(version=version)
    nodelist = [i.category.category_code + i.node_code + " - " + i.node_text for i in nodes]
    # linklist = [[i.from_node.category.category_code + i.from_node.node_code + " - " + i.from_node.node_text, i.to_node.category.category_code + i.to_node.node_code + " - " + i.to_node.node_text] for i in links]
    link_dict = {}

    if link_import_df.shape[1] == 3:
        for i in link_import_df.index.values.tolist():
            n0 = link_import_df.iloc[:,1][i]
            n1 = link_import_df.iloc[:,2][i]
            name = link_import_df.iloc[:,0][i]
            from_node=Node.objects.get(version=version, node_code=n0[1:n0.find(" - ")], category=Category.objects.get(version=version, category_code=n0[:1]))
            to_node=Node.objects.get(version=version, node_code=n1[1:n1.find(" - ")], category=Category.objects.get(version=version, category_code=n1[:1]))

            if (from_node, to_node) not in list(link_dict.keys()):
                link_dict[(from_node, to_node)] = [1, name]
            else:
                link_dict[(from_node, to_node)][0] += 1



    else:

        for i in link_import_df.index.values.tolist():
            row = link_import_df.iloc[[i]]
            name = row[headers[0]].values.tolist()[0]
            if row[headers[1]].values.tolist()[0] == "Many to One":
                first = str(row[headers[3]].values.tolist()[0])
            else:
                first = str(row[headers[2]].values.tolist()[0])
            if row[headers[1]].values.tolist()[0] == "One to Many":
                second = str(row[headers[5]].values.tolist()[0])
            else:
                second = str(row[headers[4]].values.tolist()[0])

            for j in nodelist:
                for k in nodelist:
                    
                    if j==k: continue
                    if first.find(j) == -1 or second.find(k) == -1: continue
                    if Node.objects.filter(version=version, node_text=j[j.find(" - ") + 3:], node_code=j[1:j.find(" - ")], category=Category.objects.get(version=version, category_code=j[:1])).count() == 0: continue
                    if Node.objects.filter(version=version, node_text=k[k.find(" - ") + 3:], node_code=k[1:k.find(" - ")], category=Category.objects.get(version=version, category_code=k[:1])).count() == 0: continue
                    from_node=Node.objects.get(version=version, node_text=j[j.find(" - ") + 3:], node_code=j[1:j.find(" - ")], category=Category.objects.get(version=version, category_code=j[:1]))
                    to_node=Node.objects.get(version=version, node_text=k[k.find(" - ") + 3:], node_code=k[1:k.find(" - ")], category=Category.objects.get(version=version, category_code=k[:1]))
                    
                    if (from_node, to_node) not in list(link_dict.keys()):
                        link_dict[(from_node, to_node)] = [1, name]
                    else:
                        link_dict[(from_node, to_node)][0] +=1

    for i in link_dict.keys():
        if link_dict[i][0] >= int(mincount):
            if Link.objects.filter(version=version, from_node=i[0], to_node=i[1]).count() == 0:
                Link.objects.create(version=version, from_node=i[0], to_node=i[1], xmid=(i[0].xpos + i[1].xpos)/2, ymid=(i[0].ypos + i[1].ypos)/2, notes=("Added by: " + link_dict[i][1]))

