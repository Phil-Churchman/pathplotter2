function getGantt(gantt_data) {

  var [earliest_sequence, latest_sequence, earliest_sequence_dur, latest_sequence_dur, nodes_rev_dict, durations, params, colour_lookup, links_out_order, colour_ref, group_info_dict] = JSON.parse(gantt_data)
  if (Object.keys(edited_gantt_params).length != 0) {
    var params = edited_gantt_params
  }
  else {
    edited_gantt_params = params
  }

  var svg = document.getElementById("gantt")

  var child_list = Array.from(svg.children)
  for (i = 0; i < child_list.length; i++) {
    if (child_list[i].tagName == "defs") { continue }
    svg.removeChild(child_list[i])
  } 

  svg.setAttribute("width", params["Plot_width"])
  svg.setAttribute("height", params["Plot_height"])

  if (params["Timing"] == "Earliest") {
    if (params["Durations"] == "With durations") {
      var sequence = earliest_sequence_dur
    }
    else {
      var sequence = earliest_sequence
    }
  }
  else {
    if (params["Durations"] == "With durations") {
      var sequence = latest_sequence_dur
    }
    else {
      var sequence = latest_sequence
    }
  }
  var end = {}
  var x_range = 0
  if (params["Durations"] == "With durations") {
    for (var [key, value] of Object.entries(sequence)) {
      end[key] = value + durations[key]
      if (value + durations[key] > x_range) { x_range = value + durations[key] }
    }
  }
  else {
    for (const [key, value] of Object.entries(sequence)) {
      end[key] = value + 1
      if (value + 1 > x_range) { x_range = value + 1 }
    }
  }
  var tick_int = Math.ceil(x_range / params["Max_X_ticks"])

  x_range = Math.ceil(x_range / tick_int) * tick_int
  var y_range = Object.keys(sequence).length
  var int_pad = params["Internal_padding"]
  var g_N = params["Legend_limit"] + params["Plot_padding"] + int_pad + params["Top_margin"]
  var g_S = g_N + params["Pixels_per_row"] * y_range
  var g_W = params["Y_axis_space"] + params["Plot_padding"] + int_pad
  var g_E = params["Plot_width"] - params["Plot_padding"] - int_pad - (params["Right_margin"]).toFixed(0)

  var y_axis = document.createElementNS('http://www.w3.org/2000/svg', 'line')
  y_axis.setAttribute("x1", String(g_W - int_pad))
  y_axis.setAttribute("y1", String(g_S + int_pad))
  y_axis.setAttribute("x2", String(g_W - int_pad))
  y_axis.setAttribute("y2", String(g_N - int_pad))
  y_axis.setAttribute("stroke-width", 1)
  y_axis.setAttribute("stroke", "grey")
  y_axis.classList.add("axis", "y_axis")
  y_axis.id = "y_axis"
  svg.appendChild(y_axis)

  var x_axis = document.createElementNS('http://www.w3.org/2000/svg', 'line')
  x_axis.setAttribute("x1", String(g_W - int_pad))
  x_axis.setAttribute("y1", String(g_S + int_pad))
  x_axis.setAttribute("x2", String(g_E + int_pad))
  x_axis.setAttribute("y2", String(g_S + int_pad))
  x_axis.setAttribute("stroke-width", 1)
  x_axis.setAttribute("stroke", "grey")
  x_axis.classList.add("axis", "x_axis")
  x_axis.id = "x_axis"
  svg.appendChild(x_axis)
  params["Plot height"] = g_S + params["Plot_padding"] + params["X_axis_space"] + int_pad

 
  svg.setAttribute("height", params["Plot height"])

  var x_per_unit = (g_E - g_W) / x_range
  var y_per_unit = (g_S - g_N) / y_range

  plot_locs = {}
  counter = 0

  if (params["Order_by"] == "Time") {
    let allKeys = Object.keys(sequence);
    allKeys.sort();
    allKeys.reverse();
    let temp_obj = {};
    for (let i = 0; i < allKeys.length; i++) { 
       temp_obj[allKeys[i]] = sequence[allKeys[i]]
    }
    sequence = temp_obj
    var items = Object.keys(sequence).map(
      (key) => { return [key, sequence[key]] });
    items.sort(
      (first, second) => { return first[1] - second[1] }
    );
    var gantt_items = items.map(
      (e) => { return e[0] });
  }
  else {
    var dict_temp = {}
    for (let i = 0; i < Object.keys(sequence).length; i++) {
      if (Object.keys(sequence)[i].slice(0, 1) == "G") {
        dict_temp["#" + Object.keys(sequence)[i]] = Object.keys(sequence)[i]
      }
      else {
        dict_temp[nodes_rev_dict[Object.keys(sequence)[i]][0]] = Object.keys(sequence)[i]
      }
    }

    var items = Object.keys(dict_temp).sort()
    var gantt_items = []
    for (i = 0; i < items.length; i++) {
      gantt_items.push(dict_temp[items[i]])
    }
  }

  var bar_padding = params["Bar_padding"]
  var truncate = ((g_W - int_pad - 20) / 4.5).toFixed(0)
  for (let i = 0; i < gantt_items.length; i++) {
    if (gantt_items[i].slice(0, 1) == "G") {
      var n = String(group_info_dict[gantt_items[i]]["node_code_list"])
    }
    else {
      var n = nodes_rev_dict[gantt_items[i]][0]
    }
    var x0 = g_W + x_per_unit * sequence[gantt_items[i]]
    if (params["Durations"] == "With durations") {
      var x1 = x0 + x_per_unit * durations[gantt_items[i]]
    }
    else {
      var x1 = x0 + x_per_unit
    }
    var y0 = g_N + y_per_unit * counter
    var y1 = y0 + y_per_unit
    // plot_locs[n] = ((x0+x1)/2, (y0+y1)/2)

    if (n.length > truncate) {
      var ntext = n.slice(0, truncate - 4) + "..."
    }
    else {
      var ntext = n
    }

    var gridline = document.createElementNS('http://www.w3.org/2000/svg', 'line')
    gridline.setAttribute("x1", String(g_W - int_pad))
    gridline.setAttribute("y1", String((y0 + y1) / 2))
    gridline.setAttribute("x2", String(g_E + int_pad))
    gridline.setAttribute("y2", String((y0 + y1) / 2))
    gridline.setAttribute("stroke-width", 1)
    gridline.setAttribute("stroke", "lightgrey")
    gridline.classList.add("gridline")
    gridline.id = "gridline" + String(i)
    svg.appendChild(gridline)

    var x = g_W - int_pad - 10
    var y = y0 + y_per_unit / 2 + 3


    var nodetext = document.createElementNS('http://www.w3.org/2000/svg', 'text')
    nodetext.setAttribute("x", String(x))
    nodetext.setAttribute("y", String(y))
    nodetext.setAttribute("style", "text-align:right; font-size:10px; text-anchor:end")
    nodetext.textContent = ntext
    nodetext.classList.add("nodetext")
    nodetext.id = "nodetext" + String(i)
    svg.appendChild(nodetext)

    if (params["Durations"] == "With durations") {
      if (durations[gantt_items[i]] != 0) {
        var ganttbar = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
        ganttbar.setAttribute("x", String(x0))
        ganttbar.setAttribute("y", String(y0 + bar_padding))
        ganttbar.setAttribute("height", String(y_per_unit - bar_padding * 2))
        ganttbar.setAttribute("width", String(x_per_unit * durations[gantt_items[i]]))
        ganttbar.setAttribute("stroke-width", 0)
        ganttbar.setAttribute("stroke", "lightgrey")
        if (gantt_items[i].slice(0, 1) == "G") {
          ganttbar.setAttribute("fill", "black")
        }
        else {
          ganttbar.setAttribute("fill", colour_lookup[gantt_items[i]])
        }
        ganttbar.classList.add("ganttbar", "rect", "selectable")
        ganttbar.id = "ganttbar" + String(gantt_items[i])
        svg.appendChild(ganttbar)
      }
      else {

        var triangle_width = y1 - y0 - 2 * bar_padding

        var ganttbar = document.createElementNS('http://www.w3.org/2000/svg', 'polygon')
        ganttbar.setAttribute("points", String(x0 - triangle_width / 2) + "," + String(y1 - bar_padding) + " " + String(x0 + triangle_width / 2) + "," + String(y1 - bar_padding) + " " + String(x0) + "," + String(y0 + bar_padding))
        ganttbar.setAttribute("stroke-width", 0)
        ganttbar.setAttribute("stroke", "lightgrey")
        if (gantt_items[i].slice(0, 1) == "G") {
          ganttbar.setAttribute("fill", "black")
        }
        else {
          ganttbar.setAttribute("fill", colour_lookup[gantt_items[i]])
        }

        ganttbar.classList.add("ganttbar", "polygon", "selectable")
        ganttbar.id = "ganttbar" + String(gantt_items[i])
        svg.appendChild(ganttbar)
      }

    }
    else {
      var ganttbar = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
      ganttbar.setAttribute("x", String(x0))
      ganttbar.setAttribute("y", String(y0 + bar_padding))
      ganttbar.setAttribute("height", String(y_per_unit - bar_padding * 2))
      ganttbar.setAttribute("width", String(x_per_unit))
      ganttbar.setAttribute("stroke-width", 0)
      ganttbar.setAttribute("stroke", "lightgrey")
      if (gantt_items[i].slice(0, 1) == "G") {
        ganttbar.setAttribute("fill", "black")
      }
      else {
        ganttbar.setAttribute("fill", colour_lookup[gantt_items[i]])
      }
      ganttbar.classList.add("ganttbar", "rect", "selectable")
      ganttbar.id = "ganttbar" + String(gantt_items[i])
      svg.appendChild(ganttbar)
    }
    counter += 1
  }

  var y_pos = g_S + params["Internal_padding"]

  function polygon_points(points) {
    var points1 = points.slice(0, points.search(" "))
    points = points.slice(points.search(" ") + 1, points.length)
    var points2 = points.slice(0, points.search(" "))
    points = points.slice(points.search(" ") + 1, points.length)
    var points3 = points.slice(1, points.length)
    var points1x = parseFloat(points1.slice(0, points1.search(",")))
    var points1y = parseFloat(points1.slice(points1.search(",") + 1, points1.length))
    var points2x = parseFloat(points2.slice(0, points2.search(",")))
    var points2y = parseFloat(points2.slice(points2.search(",") + 1, points2.length))
    var points3x = parseFloat(points3.slice(0, points3.search(",")))
    var points3y = parseFloat(points3.slice(points3.search(",") + 1, points3.length))

    return [points1x, points1y, points2x, points2y, points3x, points3y]
  }
  if (params["Show_out_seq"]) {
    for (let i = 0; i < links_out_order.length; i++) {
      var l = links_out_order[i]
      var bar1 = document.getElementById("ganttbar" + l[0])
      var bar2 = document.getElementById("ganttbar" + l[1])
      if (bar2.classList.contains("rect")) {
        var x1 = parseFloat(bar1.getAttribute("x"))
        var y1 = parseFloat(bar1.getAttribute("y"))
        var width1 = parseFloat(bar1.getAttribute("width"))
        var height1 = parseFloat(bar1.getAttribute("height"))
        var xpos1 = (x1 + width1 / 2).toFixed(0)
        var ypos1 = (y1 + height1 / 2).toFixed(0)
      }
      else {
        var points1 = bar1.getAttribute("points")
        var [points1_1x, points1_1y, points1_2x, points1_2y, points1_3x, points1_3y] = polygon_points(points1)
        var xpos1 = ((points1_1x + points1_2x) / 2).toFixed(0)
        var ypos1 = ((points1_1y + points1_3y) / 2).toFixed(0)
        // var points1_1 = points1.slice(0, points1.search(" "))
        // points1 = points1.slice(points1.search(" ") + 1, points1.length)
        // var points1_2 = points1.slice(0, points1.search(" "))
        // points1 = points1.slice(points1.search(" ") + 1, points1.length)
        // var points1_3 = points1.slice(1, points1.length)
        // var points1_1x = parseFloat(points1_1.slice(0, points1_1.search(",")))
        // var points1_1y = parseFloat(points1_1.slice(points1_1.search(",") + 1, points1_1.length))
        // var points1_2x = parseFloat(points1_2.slice(0, points1_2.search(",")))
        // var points1_2y = parseFloat(points1_2.slice(points1_2.search(",") + 1, points1_2.length))
        // var points1_3x = parseFloat(points1_3.slice(0, points1_3.search(",")))
        // var points1_3y = parseFloat(points1_3.slice(points1_3.search(",") + 1, points1_3.length))
      }
      if (bar2.classList.contains("rect")) {
        var x2 = parseFloat(bar2.getAttribute("x"))
        var y2 = parseFloat(bar2.getAttribute("y"))
        var width2 = parseFloat(bar2.getAttribute("width"))
        var height2 = parseFloat(bar2.getAttribute("height"))
        var xpos2 = (x2 + width2 / 2).toFixed(0)
        var ypos2 = (y2 + height2 / 2).toFixed(0)
      }
      else {
        var points2 = bar2.getAttribute("points")
        var [points2_1x, points2_1y, points2_2x, points2_2y, points2_3x, points2_3y] = polygon_points(points2)
        var xpos2 = ((points2_1x + points2_2x) / 2).toFixed(0)
        var ypos2 = ((points2_1y + points2_3y) / 2).toFixed(0)
      }

      var d = "M " + String(xpos1) + "," + String(ypos1) + " C " + String(xpos2) + "," + String(ypos1) + " " + String(xpos1) + "," + String(ypos2) + " " + String(xpos2) + "," + String(ypos2)
      var outseq = document.createElementNS('http://www.w3.org/2000/svg', 'path')
      outseq.setAttribute("d", d)
      outseq.setAttribute("marker-end", "url(#arrowheadindianred)")
      outseq.setAttribute("stroke-width", 1)
      outseq.setAttribute("fill", "none")
      outseq.setAttribute("stroke", "indianred")
      outseq.classList.add("outseq")
      outseq.id = "outseq" + String(gantt_items[i])
      svg.appendChild(outseq)
    }
  }

  var tick_text = []

  if (params["X_axis"] != "Number" && params["Durations"] == "With durations") {

    for (i = 0; i < Math.ceil(x_range) + 1; i += tick_int) {

      x_pos = g_W + (i * x_per_unit).toFixed(0)

      if (params["X_axis"] == "Month") {

        var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        var month = months[(months.indexOf(params["Start_month_if_Month"]) + i) % 12]
        var year = String(parseInt(params["Start_year"]) + Math.ceil(i / 12))
        tick_text.push(month + " " + year.slice(2, year.length))

      }
      else if (params["X_axis"] == "Year") {

        year = String(parseInt(params["Start_year"]) + i)
        tick_text.push(year)
      }
    }
  }
  else {
    for (i = 0; i < Math.ceil(x_range) + 1; i += tick_int) {
      tick_text.push(String(i))
    }
  }
  var counter = 0
  for (i = 0; i < Math.ceil(x_range) + 1; i += tick_int) {
    var x_pos = g_W + i * x_per_unit

    var tickline = document.createElementNS('http://www.w3.org/2000/svg', 'line')
    tickline.setAttribute("x1", String(x_pos))
    tickline.setAttribute("y1", String(y_pos))
    tickline.setAttribute("x2", String(x_pos))
    tickline.setAttribute("y2", String(y_pos + params["Tick_length"]))
    tickline.setAttribute("stroke-width", 1)
    tickline.setAttribute("stroke", "grey")
    tickline.classList.add("tickline")
    tickline.id = "tickline" + String(i)
    svg.appendChild(tickline)

    var ticktext = document.createElementNS('http://www.w3.org/2000/svg', 'text')
    ticktext.setAttribute("x", String(x_pos))
    ticktext.setAttribute("y", String(y_pos + params["Tick_length"] + 20))
    ticktext.setAttribute("style", "text-align:center; font-size:10px; text-anchor:middle")
    ticktext.textContent = tick_text[counter]
    ticktext.classList.add("ticktext")
    ticktext.id = "ticktext" + String(i)
    svg.appendChild(ticktext)


    // var ticktext = document.createElementNS('http://www.w3.org/2000/svg','foreignObject')
    // ticktext.setAttribute("x", String(x_pos - x_per_unit * tick_int/2))
    // ticktext.setAttribute("y", String(y_pos + params["Tick_length"] + 10))
    // ticktext.setAttribute("width", String(x_per_unit*tick_int))
    // ticktext.setAttribute("height", String(10))
    // ticktext.setAttribute("style", "text-align:center")

    // ticktext.classList.add("ticktext" )
    // ticktext.id = "ticktext" + String(i)

    // ttext = document.createElement('p')
    // ttext.setAttribute("style", "font-size:10px; line-height:1.2")
    // ttext.textContent = tick_text[counter]
    // ticktext.appendChild(ttext)
    // svg.appendChild(ticktext)
    counter++

  }

  if (params["Durations"] == "With durations") {
    if (params["X_axis"] == "Number") {

      var axis_text = params["Time_unit_if_Number"]
    }
    else {
      var axis_text = params["X_axis"]
    }
  }
  else {
    var axis_text = "Step sequence"
  }

  var axistext = document.createElementNS('http://www.w3.org/2000/svg', 'text')
  axistext.setAttribute("x", String((g_W + g_E) / 2))
  axistext.setAttribute("y", String(g_S + 60))
  axistext.setAttribute("style", "text-align:center; font-size:10px; text-anchor:middle")
  axistext.classList.add("axistext")
  axistext.textContent = axis_text
  axistext.id = "axistext"
  svg.appendChild(axistext)

  if (params["Show_out_seq"]) {
  additional = [["arrow", "indianred", "", "Out of sequence"]]
  }
  else {
    additional = []
  }
  legend(colour_ref, params, svg, additional)
}

function makeSelectable(evt, node_id_dict, group_id_dict) {
  var node_id_dict = JSON.parse(node_id_dict)
  var group_id_dict = JSON.parse(group_id_dict)

  evt.preventDefault();
  var svg = evt.target;
  svg.addEventListener('mousedown', (evt) => {selectEvent(evt, node_id_dict, group_id_dict); });

  function selectEvent(evt, node_id_dict, group_id_dict) {

    if (evt.target.classList.contains("selectable")) {

      if (evt.altKey) {
        node = evt.target.id.slice(8,)
        if (node[0] != "G") {
          node_id = node_id_dict[node]
        open("/edit-node/" + node_id,"_self")
        }
        else {
          group_id = group_id_dict[node]
          open("/edit-group/" + group_id,"_self")
        }
      }

  }
}
}
