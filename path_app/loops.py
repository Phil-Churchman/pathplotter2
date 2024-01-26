from .models import Node
import copy
# from.utilities import current_version


def get_loops(edge_list, version, check_only):

    max_loops = 100

    edge_list = [tuple(i) for i in edge_list]
    chains_temp = {}
    loops = []
    for i in edge_list:
        chains_temp[i] = True
    while len(loops) < max_loops - 1:
        found1 = False
        for i in list(chains_temp.keys()):
            if chains_temp[i] == False: continue
            found2 = False
            for j in list(filter(lambda x: x[1] == i[0] or x[0] == i[-1], edge_list)):
            # for j in edge_list:    
                if j[1] == i[0]:
                    if j[0] == i[len(i) - 1]:
                        if check_only: return False
                        min_node = min(list(i))
                        loop = list(i)
                        index = loop.index(min_node)
                        loop = loop[index:] + loop[:index]
                        if loop not in loops:
                            loops.append(loop)
                            # found1 = True
                            # found2 = True
                    elif j[0] in list(i):
                        continue
                    elif tuple([j[0]] + list(i)) not in list(chains_temp.keys()):
                            chains_temp[tuple([j[0]] + list(i))] = True
                            found1 = True
                            found2 = True
                elif j[0] == i[len(i) - 1]:
                    if j[1] in list(i):
                        continue
                    elif tuple(list(i) + [j[1]]) not in list(chains_temp.keys()):
                        chains_temp[tuple(list(i) + [j[1]])] = True
                        found1 = True
                        found2 = True                  
                if found2 == False:
                    chains_temp[i] = False
        if found1 == False:
            break
    
    if check_only: return True

    if len(loops) >= max_loops:
        return False    
    
    new_loops = []
    for i in loops:
        loop = [[i[j], i[j + 1]] for j in range(len(i)-1)] + [[i[len(i)-1], i[0]]]
        new_loops.append(loop)
    loops = new_loops

    goal_ids = [i.id for i in filter(lambda x: x.category.category_code == ">", Node.objects.filter(version=version))]
    chains_to_goals = filter(lambda x: x[len(x) - 1] in goal_ids, chains_temp)

    # chains_to_goals = filter(lambda x: Node.objects.get(id=x[len(x) - 1]).category.category_code == ">", chains_temp)
    new_chains_to_goals = []
    for i in chains_to_goals:
        chain = [[i[j], i[j + 1]] for j in range(len(i)-1)]
        new_chains_to_goals.append(chain)
    chains_to_goals = new_chains_to_goals

    nodes_to_goals = []
    links_to_goals = []
    for i in chains_to_goals:
        for j in i:
            if j not in links_to_goals:
                links_to_goals.append(j)
                for k in j:
                    if k not in nodes_to_goals:
                        nodes_to_goals.append(k)

    return loops

