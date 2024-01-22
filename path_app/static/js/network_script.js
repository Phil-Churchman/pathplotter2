var ctrl_temp = []
var id_temp = 0
var edited_nodes = []
var edited_links = []
var selected_nodes = []
var select_range = []
var selection_drag_active = false
var item_drag_active = false


function path_coords(d) {
  d = d.slice(d.search(" ") + 1, d.length)
  var x0 = d.slice(0, d.search(","))
  var y0 = d.slice(d.search(",") + 1, d.search(" "))
  d = d.slice(d.search(" ") + 1, d.length)
  d = d.slice(d.search(" ") + 1, d.length)
  var x1 = d.slice(0, d.search(","))
  d = d.slice(d.search(",") + 1, d.length)
  var y1 = d.slice(0, d.search(" "))
  d = d.slice(d.search(" ") + 1, d.length)
  var x2 = d.slice(0, d.search(","))
  var y2 = d.slice(d.search(",") + 1, d.length)
  return [Number(x0), Number(y0), Number(x1), Number(y1), Number(x2), Number(y2)];
}

function moveNode(id, n, coord_x, coord_y, backup) {
  sendAJAXRequest(JSON.stringify({ "id": id, "xpos": coord_x, "ypos": coord_y, "backup": backup}), "/new_pos/")

  const edited_node = edited_nodes.filter(checkNodeId)[0];

  function checkNodeId(node) {
    return node.id == id;
  }
  edited_node.xpos = coord_x
  edited_node.ypos = coord_y

  n["xpos"] = coord_x
  n["ypos"] = coord_y

  const edited_from_links = edited_links.filter(checkFromLinkId);

  function checkFromLinkId(link) {
    return link["from_node"] == id;
  }


  for (let i = 0; i < edited_from_links.length; i++) {


    edited_from_links[i]["xpos1"] = coord_x
    edited_from_links[i]["ypos1"] = coord_y
    edited_from_links[i]["xmid"] = (coord_x + edited_from_links[i]["xpos2"]) / 2
    edited_from_links[i]["ymid"] = (coord_y + edited_from_links[i]["ypos2"]) / 2
  }

  const edited_to_links = edited_links.filter(checkToLinkId);

  function checkToLinkId(link) {
    return link["to_node"] == id;
  }
  for (let i = 0; i < edited_to_links.length; i++) {
    edited_to_links[i]["xpos2"] = coord_x
    edited_to_links[i]["ypos2"] = coord_y
    edited_to_links[i]["xmid"] = (edited_to_links[i]["xpos1"] + edited_to_links[i]["xpos2"]) / 2
    edited_to_links[i]["ymid"] = (edited_to_links[i]["ypos1"] + edited_to_links[i]["ypos2"]) / 2
  }

  var elements = document.getElementsByClassName(id + "__label")
  if (elements.length > 0) {

    elements[0].setAttributeNS(null, "x", coord_x - 60);
    elements[0].setAttributeNS(null, "y", coord_y + 15);
  }
  var elements = document.getElementsByClassName("from_node" + id)

  if (elements.length > 0) {

    for (let i = 0; i < elements.length; i++) {
      var d = elements[i].getAttribute("d");
      const [x0, y0, x1, y1, x2, y2] = path_coords(d);

      const nx0 = (coord_x)
      const ny0 = (coord_y)
      const nx2 = (x0 + x2 - nx0)
      const ny2 = (y0 + y2 - ny0)
      const nx1 = nx2 / 2
      const ny1 = ny2 / 2

      var nd = "M " + String(nx0) + "," + String(ny0) + " q " + String(nx1) + "," + String(ny1) + " " + String(nx2) + "," + String(ny2)

      elements[i].setAttribute("d", nd);

      var mid = document.getElementById(elements[i].id.toString() + "__mid")

      if (mid != null) {
        mid.setAttribute("cx", nx0 + nx1);
        mid.setAttribute("cy", ny0 + ny1);
      }
    }

  }
  var elements = document.getElementsByClassName("to_node" + id)

  if (elements.length > 0) {
    for (let i = 0; i < elements.length; i++) {



      var d = elements[i].getAttribute("d");
      const [x0, y0, x1, y1, x2, y2] = path_coords(d);

      const nx2 = (coord_x) - x0
      const ny2 = (coord_y) - y0
      const nx0 = x0
      const ny0 = y0
      const nx1 = nx2 / 2
      const ny1 = ny2 / 2

      var nd = "M " + nx0.toString() + "," + ny0.toString() + " q " + nx1.toString() + "," + ny1.toString() + " " + nx2.toString() + "," + ny2.toString()

      elements[i].setAttribute("d", nd);

      var mid = document.getElementById(elements[i].id.toString() + "__mid")

      if (mid != null) {
        mid.setAttribute("cx", nx0 + nx1);
        mid.setAttribute("cy", ny0 + ny1);
      }

    }
  }
}

function moveNode(id, n, coord_x, coord_y, backup) {
  sendAJAXRequest(JSON.stringify({ "id": id, "xpos": coord_x, "ypos": coord_y, "backup": backup}), "/new_pos/")

  const edited_node = edited_nodes.filter(checkNodeId)[0];

  function checkNodeId(node) {
    return node.id == id;
  }
  edited_node.xpos = coord_x
  edited_node.ypos = coord_y

  n["xpos"] = coord_x
  n["ypos"] = coord_y

  const edited_from_links = edited_links.filter(checkFromLinkId);

  function checkFromLinkId(link) {
    return link["from_node"] == id;
  }


  for (let i = 0; i < edited_from_links.length; i++) {


    edited_from_links[i]["xpos1"] = coord_x
    edited_from_links[i]["ypos1"] = coord_y
    edited_from_links[i]["xmid"] = (coord_x + edited_from_links[i]["xpos2"]) / 2
    edited_from_links[i]["ymid"] = (coord_y + edited_from_links[i]["ypos2"]) / 2
  }

  const edited_to_links = edited_links.filter(checkToLinkId);

  function checkToLinkId(link) {
    return link["to_node"] == id;
  }
  for (let i = 0; i < edited_to_links.length; i++) {
    edited_to_links[i]["xpos2"] = coord_x
    edited_to_links[i]["ypos2"] = coord_y
    edited_to_links[i]["xmid"] = (edited_to_links[i]["xpos1"] + edited_to_links[i]["xpos2"]) / 2
    edited_to_links[i]["ymid"] = (edited_to_links[i]["ypos1"] + edited_to_links[i]["ypos2"]) / 2
  }

  var elements = document.getElementsByClassName(id + "__label")
  if (elements.length > 0) {

    elements[0].setAttributeNS(null, "x", coord_x - 60);
    elements[0].setAttributeNS(null, "y", coord_y + 15);
  }
  var elements = document.getElementsByClassName("from_node" + id)

  if (elements.length > 0) {

    for (let i = 0; i < elements.length; i++) {
      var d = elements[i].getAttribute("d");
      const [x0, y0, x1, y1, x2, y2] = path_coords(d);

      const nx0 = (coord_x)
      const ny0 = (coord_y)
      const nx2 = (x0 + x2 - nx0)
      const ny2 = (y0 + y2 - ny0)
      const nx1 = nx2 / 2
      const ny1 = ny2 / 2

      var nd = "M " + String(nx0) + "," + String(ny0) + " q " + String(nx1) + "," + String(ny1) + " " + String(nx2) + "," + String(ny2)

      elements[i].setAttribute("d", nd);

      var mid = document.getElementById(elements[i].id.toString() + "__mid")

      if (mid != null) {
        mid.setAttribute("cx", nx0 + nx1);
        mid.setAttribute("cy", ny0 + ny1);
      }
    }

  }
  var elements = document.getElementsByClassName("to_node" + id)

  if (elements.length > 0) {
    for (let i = 0; i < elements.length; i++) {



      var d = elements[i].getAttribute("d");
      const [x0, y0, x1, y1, x2, y2] = path_coords(d);

      const nx2 = (coord_x) - x0
      const ny2 = (coord_y) - y0
      const nx0 = x0
      const ny0 = y0
      const nx1 = nx2 / 2
      const ny1 = ny2 / 2

      var nd = "M " + nx0.toString() + "," + ny0.toString() + " q " + nx1.toString() + "," + ny1.toString() + " " + nx2.toString() + "," + ny2.toString()

      elements[i].setAttribute("d", nd);

      var mid = document.getElementById(elements[i].id.toString() + "__mid")

      if (mid != null) {
        mid.setAttribute("cx", nx0 + nx1);
        mid.setAttribute("cy", ny0 + ny1);
      }

    }
  }
}

function makeDraggable(evt, params) {
  evt.preventDefault();
  var svg = evt.target;

  var params = JSON.parse(params)


  svg.addEventListener('mousedown', mousedownEvent);
  svg.addEventListener('mousemove', drag);
  svg.addEventListener('mouseup', upEvent);
  // svg.addEventListener('touchstart', mousedownEvent);
  // svg.addEventListener('touchmove', drag);
  // svg.addEventListener('touchend', upEvent);  
  // svg.addEventListener('touchcancel', upEvent);
  // svg.addEventListener('mouseleave', endDrag);

  var selectedElement, offset;
  var starting = {}

  function mousedownEvent(evt) {
    // evt.preventDefault()
    select_range = []

    if (evt.target.classList.contains("node") || evt.target.classList.contains("link_mid") || evt.target.id == "network") {

      if (evt.ctrlKey) {
        cnrlEvent(evt)
      }
      else if (evt.altKey) {
        editItem(evt)
      }
      else if (evt.shiftKey) {

        shiftEvent(evt)
      }
      else {
        startDrag(evt)
      }
    }
    else if (evt.target.classList.contains("link")) {
      if (evt.altKey) {
        editItem(evt)
      }
    }


  }
  function upEvent(evt) {
    if (evt.ctrlKey) {
    }
    else if (evt.altKey) {
    }
    else if (evt.shiftKey) {
      if (select_range.length == 1) {
        var coord = getMousePosition(evt)
        select_range.push([coord.x, coord.y])

        var sel_nodes = edited_nodes.filter(checkSelNodes)

        function checkSelNodes(node) {
          return ((node["xpos"] >= select_range[0][0] && node["xpos"] <= select_range[1][0]) || (node["xpos"] <= select_range[0][0] && node["xpos"] >= select_range[1][0])) && ((node["ypos"] >= select_range[0][1] && node["ypos"] <= select_range[1][1]) || (node["ypos"] <= select_range[0][1] && node["ypos"] >= select_range[1][1]))
        }
        for (i = 0; i < sel_nodes.length; i++) {
          var n = document.getElementById(sel_nodes[i]["id"])
          if (selected_nodes.includes(String(sel_nodes[i]["id"]))) {

            selected_nodes.splice(selected_nodes.indexOf(sel_nodes[i]["id"]), 1)
            n.setAttribute("stroke", "grey");
            n.setAttribute("stroke-width", 1);
          }
          else {

            selected_nodes.push(sel_nodes[i]["id"])

            n.setAttribute("stroke", "black");
            n.setAttribute("stroke-width", 3);
          }
        }
      }
    }

    else {
      endDrag(evt)
    }
    select_range = []
  }
  function cnrlEvent(evt) {
    var selectedElement = evt.target;
    var id = selectedElement.id.toString();
    var classes = selectedElement.classList;
    if (classes.contains("node")) {
      
      if (selected_nodes.length > 0) {
        for (let i=0; i<selected_nodes.length; i++) {
          let node = document.getElementById(selected_nodes[i]) 
          node.setAttribute("stroke", "grey");
          node.setAttribute("stroke-width", 1);
          ctrl_temp = [selected_nodes[i], evt.target.id]
          createLink(false)
          ctrl_temp = []
        }
      }

      else if (ctrl_temp.length == 0) {
        ctrl_temp[0] = evt.target.id
        evt.target.setAttribute("stroke", "blue");
        evt.target.setAttribute("stroke-width", 3);
      }
      else if (ctrl_temp.length == 1) {
        if (ctrl_temp[0] == evt.target.id) {
          evt.target.setAttribute("stroke", "grey");
          evt.target.setAttribute("stroke-width", 1);
          ctrl_temp = []
        }
        else {
          ctrl_temp[1] = evt.target.id
          createLink(true)
          ctrl_temp = []
        }
      }
      else {
        ctrl_temp = []
      }
    }
    else if (id == "network") {
      var coord = getMousePosition(evt)
      open("../add-node-placed/" + String(coord.x.toFixed(0)) + "/" + String(coord.y.toFixed(0)) + "/", "_self")
    }
  }
  function shiftEvent(evt) {
    var selectedElement = evt.target;
    var id = selectedElement.id.toString();
    var classes = selectedElement.classList;

    if (selected_nodes.includes(parseInt(evt.target.id))) {

      selected_nodes.splice(selected_nodes.indexOf(parseInt(evt.target.id)), 1)
      evt.target.setAttribute("stroke", "grey");
      evt.target.setAttribute("stroke-width", 1);
    }
    else if (classes.contains("node")) {
      selected_nodes.push(parseInt(evt.target.id))
      evt.target.setAttribute("stroke", "black");
      evt.target.setAttribute("stroke-width", 3);
    }
    else if (id == "network") 
     {
        if (evt.shiftKey) {
          var coord = getMousePosition(evt)
          select_range = [[coord.x, coord.y]]
        }
    }

  }

  function unhighlightLink(node) {
    node.setAttribute("stroke", "grey");
    node.setAttribute("stroke-width", 1);
  }

  function createLink(backup) {

    const svg = document.getElementById("network")
    var node1 = document.getElementById(ctrl_temp[0])
    var node2 = document.getElementById(ctrl_temp[1])

    var existing_links = document.getElementsByClassName("from_node" + node1.id + " to_node" + node2.id)

    if (existing_links.length == 0) {

      if (backup) {
      sendAJAXRequest(JSON.stringify({ "from_node": ctrl_temp[0], "to_node": ctrl_temp[1] }), "/add-link-defined/")
      }
      else {
      sendAJAXRequest(JSON.stringify({ "from_node": ctrl_temp[0], "to_node": ctrl_temp[1] }), "/add-link-defined-nobackup/")  
      }

      var coords1 = [node1.getAttribute("cx"), node1.getAttribute("cy")]
      var coords2 = [node2.getAttribute("cx"), node2.getAttribute("cy")]
      var nx0 = coords1[0]
      var ny0 = coords1[1]
      var nx2 = coords2[0] - coords1[0]
      var ny2 = coords2[1] - coords1[1]
      var nx1 = nx2 / 2
      var ny1 = ny2 / 2

      var d = "M " + String(nx0) + "," + String(ny0) + " q " + String(nx1) + "," + String(ny1) + " " + String(nx2) + "," + String(ny2)

      unhighlightLink(document.getElementById(ctrl_temp[0]))

      const new_link = document.createElementNS("http://www.w3.org/2000/svg", "path");
      new_link.id = "x" + id_temp.toString()

      new_link.setAttribute("d", d)
      new_link.setAttribute("style", "stroke:lightgrey;stroke-width:1")
      new_link.setAttribute("class", "link from_node" + node1.id.toString() + " to_node" + node2.id.toString() + " editable")
      new_link.setAttribute("marker-end", "url(#arrowheadlightgrey)")

      svg.appendChild(new_link)


      // const new_mid = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      // new_mid.id = new_link.id + "__mid"
      // new_mid.setAttribute("class", "link_mid draggable")
      // new_mid.setAttribute("cx", xmid)
      // new_mid.setAttribute("cy", ymid)
      // new_mid.setAttribute("r", "2")
      // new_mid.setAttribute("style", "stroke:lightgrey;stroke-width:1")
      // new_mid.setAttribute("fill", "lightgrey")

      // svg.appendChild(new_mid)

      cloneToTop(node1)
      cloneToTop(node2)

    }

    else {
      unhighlightLink(document.getElementById(ctrl_temp[0]))
      ctrl_temp = []

    }

  }

  function cloneToTop(oldEl) {
    // already at top, don't go farther…
    if (oldEl.atTop == true) return oldEl;
    // make a copy of this node
    var el = oldEl.cloneNode(true);
    // select all draggable elements, none of them are at top anymore
    var dragEls = oldEl.ownerDocument.documentElement.querySelectorAll('.draggable');
    for (i = 0; i < dragEls.length; i++) {
      dragEls[i].atTop = null;
    }
    var parent = oldEl.parentNode;
    // remove the original node
    parent.removeChild(oldEl);
    // insert our new node at top (last element drawn is first visible in svg)
    parent.appendChild(el);
    // Tell the world that our new element is at Top
    el.atTop = true;
    return el;
  }

  function startDrag(evt) {


    if (evt.target.classList.contains('draggable')) {
      if (selected_nodes.includes(parseInt(evt.target.id))) {
        selection_drag_active = true
        offset = getMousePosition(evt);
        for (let i = 0; i < selected_nodes.length; i++) {

          var node = cloneToTop(document.getElementById(String(selected_nodes[i])))

          var node_coord = {}
          node_coord["x"] = parseFloat(node.getAttribute("cx"))
          node_coord["y"] = parseFloat(node.getAttribute("cy"))
          starting[selected_nodes[i]] = node_coord
        }
      }
      else {
        selectedElement = cloneToTop(evt.target);
        offset = getMousePosition(evt);
        offset.x -= parseFloat(selectedElement.getAttributeNS(null, "cx"));
        offset.y -= parseFloat(selectedElement.getAttributeNS(null, "cy"));

          item_drag_active = true

      }
    }
  }

  function drag(evt) {
    evt.preventDefault();
    if (selection_drag_active) {

      var coord = getMousePosition(evt);
      for (let i = 0; i < selected_nodes.length; i++) {
        var node = document.getElementById(String(selected_nodes[i]))
        var cx = starting[selected_nodes[i]].x + coord.x - offset.x
        var cy = starting[selected_nodes[i]].y + coord.y - offset.y

        if (cx < 10) {
          cx = 10
        }
        
        else if (cx > params["Plot_width"] - params["Legend_x_spacing"] - params["Legend_box_pad"] * 2 - 10) {
          // else if (cx > params["Plot_width"] - 10) {  
          cx = params["Plot_width"] - params["Legend_x_spacing"] - params["Legend_box_pad"] * 2 - 10
        }

        if (cy < 10) {
          cy = 10
        }
        else if (cy > params["Plot_height"] - 10) {
          cy = params["Plot_height"] - 10
        }

        node.setAttributeNS(null, "cx", cx);
        node.setAttributeNS(null, "cy", cy);
      }
    }

    // if (selectedElement) {

    // if (selected_nodes.includes(parseInt(evt.target.id))) {

    else if (item_drag_active) {
      var coord = getMousePosition(evt);
      selectedElement.setAttributeNS(null, "cx", coord.x - offset.x);
      selectedElement.setAttributeNS(null, "cy", coord.y - offset.y);
    }
  }

  function endDragNode(coord) {

    var id = parseInt(selectedElement.id)

    moveNode(id, selectedElement, coord.x - offset.x, coord.y - offset.y, true)
  }

  function endDragSelection(coord) {
    for (let i = 0; i < selected_nodes.length; i++) {
      var node = document.getElementById(selected_nodes[i])
      var cx = starting[selected_nodes[i]].x + coord.x - offset.x
      var cy = starting[selected_nodes[i]].y + coord.y - offset.y

      if (cx < 10) {
        cx = 10
      }
      else if (cx > params["Plot_width"] - 10) {
        cx = params["Plot_width"] - 10
      }

      if (cy < 10) {
        cy = 10
      }
      else if (cy > params["Plot_height"] - 10) {
        cy = params["Plot_height"] - 10
      }
      moveNode(selected_nodes[i], node, cx, cy, false)

    }

  }

  function endDragMid(coord) {
    var id = String(selectedElement.id)
    var linkid = id.slice(0, id.length - 5)
    if (document.getElementById(linkid) != null) {
      var link = document.getElementById(linkid)
      var d = link.getAttribute("d");

      const [x0, y0, x1, y1, x2, y2] = path_coords(d);

      nx1 = ((coord.x - offset.x) - (x0 + x2 / 2)) * 2 + (x0 + x2 / 2) - x0
      ny1 = ((coord.y - offset.y) - (y0 + y2 / 2)) * 2 + (y0 + y2 / 2) - y0

      var nd = "M " + String(x0) + "," + String(y0) + " q " + String(nx1) + "," + String(ny1) + " " + String(x2) + "," + String(y2)

      var l = edited_links.filter(findLink)[0]

      function findLink(lx) {
        return lx.id == parseInt(linkid)
      }

      l["xmid"] = x0 + nx1
      l["ymid"] = y0 + ny1

      link.setAttribute("d", nd);
    }
  }

  function endDrag(evt) {

    var coord = getMousePosition(evt);

    if (selection_drag_active) {
      // for (let i=0; i<selected_nodes.length; i++) {
      endDragSelection(coord)
      selection_drag_active = false
      // }

    }

    else if (evt.target.classList.contains('node')) {

      endDragNode(coord)
      item_drag_active = false
    }

    else if (evt.target.classList.contains('link_mid')) {
      // sendPOSTRequest({ id: selectedElement.getAttribute("id"), xmid_draw: coord.x - offset.x, ymid_draw: coord.y - offset.y }, "/new_mid/")

      var classes = selectedElement.classList

      var id = selectedElement.getAttribute("id")
      id = id.slice(0, id.length - 5)
      sendAJAXRequest(JSON.stringify({ "id": id, xmid_draw: coord.x - offset.x, ymid_draw: coord.y - offset.y }), "/new_mid/")

      endDragMid(coord)
      item_drag_active = false
    }

    selectedElement = null;
    starting = {}


  }

  function getMousePosition(evt) {
    var CTM = svg.getScreenCTM();
    return {
      x: (evt.clientX - CTM.e) / CTM.a,
      y: (evt.clientY - CTM.f) / CTM.d
    };
  }
}

function getNetwork(network_data, colour_ref, conn_to_goal_legend, legend_loop, legend_group) {

  var [categories, nodes, links, params] = JSON.parse(network_data)
  var colour_ref = JSON.parse(colour_ref)
  var [conn_to_goal_legend] = JSON.parse(conn_to_goal_legend)
  var [legend_loop] = JSON.parse(legend_loop)
  var [legend_group] = JSON.parse(legend_group)
  var loop_options = true
  // if (params["Model_choice"] == "AC") {
  //   var loop_options = true
  // }
  // else {
  //   var loop_options = false
  // }
  if (Object.keys(edited_network_params).length != 0) {
    var params = edited_network_params
    var nodes = edited_nodes
    var links = edited_links
  }
  else {
    edited_network_params = params
    edited_nodes = nodes
    edited_links = links
  }

  var svg = document.getElementById("network")

  var child_list = Array.from(svg.children)
  for (i = 0; i < child_list.length; i++) {
    if (child_list[i].tagName == "defs") { continue }
    svg.removeChild(child_list[i])
  }

  // svg.setAttribute("width", params["Plot_width"])
  // svg.setAttribute("height", params["Plot_height"])

  if (params["Hide_links"] == false) {

    for (i = 0; i < links.length; i++) {

      l = links[i]
      if (l["show"]) {
        var d = "M " + String(l["xpos1"]) + "," + String(l["ypos1"]) + " q " + String(l["xmid"] - l["xpos1"]) + "," + String(l["ymid"] - l["ypos1"]) + " " + String(l["xpos2"] - l["xpos1"]) + "," + String(l["ypos2"] - l["ypos1"])
        var link = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        link.setAttribute("d", d)
        
        link.setAttribute("stroke-width", 1)
        link.setAttribute("fill", "none")
        if (loop_options == true) {
          link.setAttribute("marker-end", "url(#arrowhead" + links[i]["colour"] + ")")
          link.setAttribute("stroke", links[i]["colour"])         
        } 
        else {
          link.setAttribute("marker-end", "url(#arrowheadlightgrey)")
          link.setAttribute("stroke", "lightgrey")         
        }
        link.setAttribute("onload", "makeEditable(evt)")
        link.setAttribute("pointer-events", "none")
        link.classList.add("link", "from_node" + String(links[i]["from_node"]), "to_node" + String(links[i]["to_node"]))
        link.id = String(l["id"])
        svg.appendChild(link)

      }
    }
  }
  for (i = 0; i < nodes.length; i++) {
    if (nodes[i]["show"]) {

      if (params["Labels"] != "No labels") {

        if (params["Labels"] == "Full labels") {
          l_text = nodes[i]["full_label"]

        }
        else {
          l_text = nodes[i]["short_label"]
        }

        var label = document.createElementNS('http://www.w3.org/2000/svg', 'foreignObject')
        label.setAttribute("x", String(nodes[i]["xpos"] - 60))
        label.setAttribute("y", String(nodes[i]["ypos"] + 15))
        label.setAttribute("width", "120")
        label.setAttribute("height", "100")
        label.setAttribute("style", "text-align:center")
        label.setAttribute("class", String(nodes[i]["id"]) + "__label label")
        label.setAttribute("pointer-events", "none")
        label.id = String(nodes[i]["id"]) + "__label"

        var label_text = document.createElement('p')
        label_text.setAttribute("style", "font-size:10px; line-height:1.2")
        // label_text.setAttribute("pointer-events", "none")
        label_text.textContent = l_text
        label_text.id = String(nodes[i]["id"] + " label")
        label.appendChild(label_text)
        svg.appendChild(label)
      }
    }
  }

  if (params["Hide_links"] == false && params["Link_midpoints"]) {
    for (i = 0; i < links.length; i++) {
      if (links[i]["show"]) {

        var cx = (links[i]["xmid"] + (links[i]["xpos1"] + links[i]["xpos2"]) / 2) / 2
        var cy = (links[i]["ymid"] + (links[i]["ypos1"] + links[i]["ypos2"]) / 2) / 2
        var mid = document.createElementNS('http://www.w3.org/2000/svg', 'circle')
        mid.setAttribute("cx", String(cx))
        mid.setAttribute("cy", String(cy))
        mid.setAttribute("r", "2")
        if (loop_options) {
        mid.setAttribute("stroke", links[i]["colour"])
        mid.setAttribute("fill", links[i]["colour"])
        }
        else {
          mid.setAttribute("stroke", "lightgrey")
          mid.setAttribute("fill", "lightgrey")
        }
        mid.setAttribute("stroke-width", "1")
        
        mid.setAttribute("class", "link_mid draggable")
        mid.id = String(links[i]["id"]) + "__mid"
        svg.appendChild(mid)
      }
    }
  }

  for (i = 0; i < nodes.length; i++) {
    if (nodes[i]["show"]) {
      var node = document.createElementNS('http://www.w3.org/2000/svg', 'circle')
      node.setAttribute("cx", String(nodes[i]["xpos"]))
      node.setAttribute("cy", String(nodes[i]["ypos"]))
      node.setAttribute("r", "10")
      if (params["Enabled_select"] == "All") {
        if ((nodes[i]["connected_to_goal"] == false) && loop_options)  {
          node.setAttribute("stroke", "red")
          node.setAttribute("stroke-width", "2")
        }
        else {
          node.setAttribute("stroke", "grey")
          node.setAttribute("stroke-width", "1")
        }
      }
      else if (params["Enabled_select"] == "Enabled only") {
        if ((nodes[i]["connected_to_goal_enabled"] == false) && loop_options) {
          node.setAttribute("stroke", "red")
          node.setAttribute("stroke-width", "2")
        }
        else {
          node.setAttribute("stroke", "grey")
          node.setAttribute("stroke-width", "1")
        }
      }
      else {
        node.setAttribute("stroke", "grey")
      }
      // node.setAttribute("stroke", "grey")
      
      node.setAttribute("fill", nodes[i]["colour"])
      node.setAttribute("class", "node draggable editable")
      node.setAttribute("onload", "makeEditable(evt)")
      node.id = String(nodes[i]["id"])
      svg.appendChild(node)
    }
  }
  additional = []
  if (params["Model_choice"] == "AC") {
    if (legend_loop) {additional.push(["arrow", "burlywood", "", "In loop"])}
    if (legend_group) {additional.push(["arrow", "cornflowerblue", "", "In group"])}
    // additional = [["arrow", "cornflowerblue", "", "In group"], ["arrow", "burlywood", "", "In loop"]]
    // additional = [["arrow", "cornflowerblue", "", "In group"]]
    }
    else {
    if (legend_loop) {additional.push(["arrow", "burlywood", "", "In loop"])}
    // additional = [["arrow", "burlywood", "", "In loop"]]
    // additional = []
    }
    if (conn_to_goal_legend) {
      additional.push(["patch", "indianred", "white", "Not connected to goal"])
    }
    
    legend(colour_ref, params, svg, additional)
}

function clearSelection() {

  for (i = 0; i < selected_nodes.length; i++) {
    var n = document.getElementById(String(selected_nodes[i]))
    n.setAttribute("stroke", "grey");
    n.setAttribute("stroke-width", 1);
  }
  selected_nodes = []
}

function align(side) {

  for (i = 0; i < selected_nodes.length; i++) {
    var n = document.getElementById(String(selected_nodes[i]))

    if (i == 0) {
      var min_x = parseFloat(n.getAttribute("cx"))
    }
    else {
      if (parseFloat(n.getAttribute("cx")) < min_x) {
        min_x = parseFloat(n.getAttribute("cx"))
      }
    }

    if (i == 0) {
      var max_x = parseFloat(n.getAttribute("cx"))
    }
    else {
      if (parseFloat(n.getAttribute("cx")) > max_x) {
        max_x = parseFloat(n.getAttribute("cx"))
      }
    }

    if (i == 0) {
      var min_y = parseFloat(n.getAttribute("cy"))
    }
    else {
      if (parseFloat(n.getAttribute("cy")) < min_y) {
        min_y = parseFloat(n.getAttribute("cy"))
      }
    }

    if (i == 0) {
      var max_y = parseFloat(n.getAttribute("cy"))
    }
    else {
      if (parseFloat(n.getAttribute("cy")) > max_y) {
        max_y = parseFloat(n.getAttribute("cy"))
      }
    }
  }
  if (["top", "bottom", "left", "right"].includes(side)) {
    for (let i = 0; i < selected_nodes.length; i++) {
      var n = document.getElementById(String(selected_nodes[i]))
      if (side == "top") {
        n.setAttribute("cy", String(min_y));
        moveNode(selected_nodes[i], n, parseFloat(n.getAttribute("cx")), min_y, false)
      }
      else if (side == "bottom") {
        n.setAttribute("cy", String(max_y));
        moveNode(selected_nodes[i], n, parseFloat(n.getAttribute("cx")), max_y, false)

    }
      else if (side == "left") {
        n.setAttribute("cx", String(min_x));

        moveNode(selected_nodes[i], n, min_x, parseFloat(n.getAttribute("cy")), false)
   
      }
      else if (side == "right") {
        n.setAttribute("cx", String(max_x));

        moveNode(selected_nodes[i], n, max_x, parseFloat(n.getAttribute("cy")), false)

      }
    }
    return
  }

  if (selected_nodes.length > 2) {
    if (side == "horizontal") {
      selected_nodes = selected_nodes.sort(function (a, b) {
        var pos_a = edited_nodes.filter(function (node) { return node.id == a })[0].xpos
        var pos_b = edited_nodes.filter(function (node) { return node.id == b })[0].xpos
        return (pos_a - pos_b)
      })
      var spacing = (max_x - min_x) / (selected_nodes.length - 1)

      for (let i = 0; i < selected_nodes.length; i++) {

        var n = document.getElementById(String(selected_nodes[i]))
        n.setAttribute("cx", min_x + spacing * i);
        moveNode(selected_nodes[i], n, min_x + spacing * i, parseFloat(n.getAttribute("cy")), false)

      }
      return
    }
    else if (side = "vertical") {
      selected_nodes = selected_nodes.sort(function (a, b) {
        var pos_a = edited_nodes.filter(function (node) { return node.id == a })[0].ypos
        var pos_b = edited_nodes.filter(function (node) { return node.id == b })[0].ypos
        return (pos_a - pos_b)
      })
      var spacing = (max_y - min_y) / (selected_nodes.length - 1)

      for (let i = 0; i < selected_nodes.length; i++) {

        var n = document.getElementById(String(selected_nodes[i]))
        n.setAttribute("cy", min_y + spacing * i);
        moveNode(selected_nodes[i], n, parseFloat(n.getAttribute("cx")), min_y + spacing * i, false)

      }
      return
    }
  }
}

function delSelection() {
  for (let i = 0; i < selected_nodes.length; i++) {
    var node = document.getElementById(String(selected_nodes[i]));
    var from_links = Array.from(document.getElementsByClassName("from_node" + String(selected_nodes[i])));
    var to_links = Array.from(document.getElementsByClassName("to_node" + String(selected_nodes[i])));
    var label = document.getElementById(String(selected_nodes[i])+"__label");
    
    for (link of from_links) {
      var mid = document.getElementById(String(link.id)+"__mid");
      if (mid != null) {
      mid.remove();
      }
      link.remove();

    }
    for (link of to_links) {
      var mid = document.getElementById(String(link.id)+"__mid");
      if (mid != null); {
      mid.remove();
      }
      link.remove();
      
    }    
    node.remove();
    label.remove();

    sendAJAXRequest(JSON.stringify({"ob_type": "node", "id": selected_nodes[i], "backup": false}), "/del-ajax/");

    
  }
  selected_nodes = [];
}