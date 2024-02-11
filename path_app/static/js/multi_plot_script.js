function getMulti(plot_data, version_list, params) {
  var plot_data = JSON.parse(plot_data);
  var version_list = JSON.parse(version_list);
  var params = JSON.parse(params);

  var svg = document.getElementById("multi_plot");

  var child_list = Array.from(svg.children);
  for (i = 0; i < child_list.length; i++) {
    svg.removeChild(child_list[i]);
  }

  svg.setAttribute("width", params["Plot_width"]);
  svg.setAttribute("height", params["Plot_height"]);

  var y_range = Object.keys(plot_data).length;
  var plot_items = Array.from(Object.keys(plot_data));

  var int_pad = params["Internal_padding"];
  var g_N =
    params["Legend_limit"] +
    params["Plot_padding"] +
    int_pad +
    params["Top_margin"];
  var g_S = g_N + params["Pixels_per_row"] * y_range;
  var g_W = params["Y_axis_space"];
  //  +
  // int_pad +
  // params["Plot_padding"]

  var g_E =
    params["Plot_width"] -
    // params["Plot_padding"] -
    // int_pad -
    params["Right_margin"].toFixed(0);

  var y_axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
  y_axis.setAttribute("x1", String(g_W));
  y_axis.setAttribute("y1", String(g_S + int_pad));
  y_axis.setAttribute("x2", String(g_W));
  y_axis.setAttribute("y2", String(g_N - int_pad));
  y_axis.setAttribute("stroke-width", 1);
  y_axis.setAttribute("stroke", "grey");
  y_axis.classList.add("axis", "y_axis");
  y_axis.id = "y_axis";
  svg.appendChild(y_axis);

  var x_axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
  x_axis.setAttribute("x1", String(g_W));
  x_axis.setAttribute("y1", String(g_S + int_pad));
  x_axis.setAttribute("x2", String(g_E));
  x_axis.setAttribute("y2", String(g_S + int_pad));
  x_axis.setAttribute("stroke-width", 1);
  x_axis.setAttribute("stroke", "grey");
  x_axis.classList.add("axis", "x_axis");
  x_axis.id = "x_axis";
  svg.appendChild(x_axis);
  params["Plot height"] =
    g_S + params["Plot_padding"] + params["X_axis_space"] + int_pad;

  svg.setAttribute("height", params["Plot height"]);

  var x_per_unit = (g_E - g_W) / version_list.length;
  var y_per_unit = (g_S - g_N) / y_range;

  // plot_locs = {};

  for (let i = 0; i < version_list.length; i++) {
    var versionline = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "line"
    );
    versionline.setAttribute("x1", String(g_W + x_per_unit * (i + 1)));
    versionline.setAttribute("y1", String(g_N - int_pad));
    versionline.setAttribute("x2", String(g_W + x_per_unit * (i + 1)));
    versionline.setAttribute("y2", String(g_S + int_pad));
    versionline.setAttribute("stroke-width", 1);
    versionline.setAttribute("stroke", "lightgrey");
    versionline.classList.add("versionline");
    versionline.id = "versionline" + String(i);
    svg.appendChild(versionline);
  }

  counter = 0;

  var bar_padding = params["Bar_padding"];
  var truncate = ((g_W - int_pad - 20) / 4.5).toFixed(0);
  for (let i = 0; i < plot_items.length; i++) {
    n = plot_items[i];
    // var x0 = g_W + x_per_unit * sequence[plot_items[i]];
    // if (params["Durations"] == "With durations") {
    //   var x1 = x0 + x_per_unit * durations[plot_items[i]];
    // } else {
    //   var x1 = x0 + x_per_unit;
    // }
    var y0 = g_N + y_per_unit * counter;
    var y1 = y0 + y_per_unit;
    // plot_locs[n] = ((x0+x1)/2, (y0+y1)/2)

    if (n.length > truncate) {
      var ntext = n.slice(0, truncate - 4) + "...";
    } else {
      var ntext = n;
    }

    var gridline = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "line"
    );
    gridline.setAttribute("x1", String(g_W));
    gridline.setAttribute("y1", String((y0 + y1) / 2));
    gridline.setAttribute("x2", String(g_E));
    gridline.setAttribute("y2", String((y0 + y1) / 2));
    gridline.setAttribute("stroke-width", 1);
    gridline.setAttribute("stroke", "lightgrey");
    gridline.classList.add("gridline");
    gridline.id = "gridline" + String(i);
    svg.appendChild(gridline);

    var x = g_W - 10;
    var y = y0 + y_per_unit / 2 + 3;

    var nodetext = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "text"
    );
    nodetext.setAttribute("x", String(x));
    nodetext.setAttribute("y", String(y));
    nodetext.setAttribute(
      "style",
      "text-align:right; font-size:10px; text-anchor:end"
    );
    nodetext.textContent = ntext;
    nodetext.classList.add("nodetext");
    nodetext.id = "nodetext" + String(i);
    svg.appendChild(nodetext);

    var item_data = plot_data[plot_items[i]];
    var item_keys = Object.keys(item_data);

    for (j = 0; j < item_keys.length; j++) {
      var required = item_data[item_keys[j]][0];
      var dependent = item_data[item_keys[j]][1];
      var index = version_list.indexOf(item_keys[j]);
      var x_centre = g_W + x_per_unit * (index + 0.5);
      var x_required =
        x_centre - (x_per_unit * 0.5 - bar_padding * 2) * required;
      var x_dependent =
        x_centre + (x_per_unit * 0.5 - bar_padding * 2) * dependent;

      var requiredbar = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "rect"
      );
      requiredbar.setAttribute("x", String(x_required));
      requiredbar.setAttribute("y", String(y0 + bar_padding));
      requiredbar.setAttribute("height", String(y_per_unit - bar_padding * 2));
      requiredbar.setAttribute("width", String(x_centre - x_required));
      requiredbar.setAttribute("stroke-width", 0);
      requiredbar.setAttribute("stroke", "lightgrey");

      requiredbar.setAttribute("fill", "#0A42CC");

      requiredbar.classList.add("requiredbar", "rect");
      requiredbar.id = "requiredbar" + String(plot_items[i]);
      svg.appendChild(requiredbar);

      var dependentbar = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "rect"
      );
      dependentbar.setAttribute("x", String(x_centre));
      dependentbar.setAttribute("y", String(y0 + bar_padding));
      dependentbar.setAttribute("height", String(y_per_unit - bar_padding * 2));
      dependentbar.setAttribute("width", String(x_dependent - x_centre));
      dependentbar.setAttribute("stroke-width", 0);
      dependentbar.setAttribute("stroke", "lightgrey");

      dependentbar.setAttribute("fill", "#35C400");

      dependentbar.classList.add("dependentbar", "rect");
      dependentbar.id = "dependentbar" + String(plot_items[i]);
      svg.appendChild(dependentbar);
    }

    counter += 1;
  }

  var y_pos = g_S + params["Internal_padding"];

  version_list;

  for (i = 0; i < version_list.length; i++) {
    var x_pos = g_W + (i + 0.5) * x_per_unit;

    //   var tickline = document.createElementNS(
    //     "http://www.w3.org/2000/svg",
    //     "line"
    //   );
    //   tickline.setAttribute("x1", String(x_pos));
    //   tickline.setAttribute("y1", String(y_pos));
    //   tickline.setAttribute("x2", String(x_pos));
    //   tickline.setAttribute("y2", String(y_pos + params["Tick_length"]));
    //   tickline.setAttribute("stroke-width", 1);
    //   tickline.setAttribute("stroke", "grey");
    //   tickline.classList.add("tickline");
    //   tickline.id = "tickline" + String(i);
    //   svg.appendChild(tickline);

    var ticktext = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "text"
    );
    ticktext.setAttribute("x", String(x_pos));
    ticktext.setAttribute("y", String(y_pos + params["Tick_length"] + 20));
    ticktext.setAttribute(
      "style",
      "text-align:center; font-size:10px; text-anchor:middle"
    );
    ticktext.textContent = version_list[i];
    ticktext.classList.add("ticktext");
    ticktext.id = "ticktext" + String(i);
    svg.appendChild(ticktext);
  }
  additional = [
    ["rect", "#0A42CC", "#0A42CC", "Percent of nodes required"],
    ["rect", "#35C400", "#35C400", "Percent of nodes dependent"],
  ];

  legend({}, params, svg, additional);
}
