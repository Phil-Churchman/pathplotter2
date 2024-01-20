function legend(colour_ref, params, svg, additional) {
  var x_spacing = params["Legend_x_spacing"]
  var y_spacing = params["Legend_y_spacing"]
  var box_pad = params["Legend_box_pad"]

  var per_row = 1
  var y_offset = 3
  var patch_size = 5
  var num_items = Object.keys(colour_ref).length + additional.length
  if (params.Apply_groups) {num_items ++}
  var x_limit = params["Plot_width"] - per_row * x_spacing - box_pad * 2
  var y_limit = (Math.ceil(num_items / per_row)) * y_spacing + y_offset + box_pad * 2

  if (params["Plot height"] < y_limit) {
    params["Plot height"] = y_limit
    svg.setAttribute("height", y_limit + 2)
  }

  function draw_patch(parent, x, y, patch_size, stroke, width, fill, id) {
    
    // var patch = $('<circle></circle>')
    // patch.hide()
    // patch.append(parent)
    //     patch.attr({"r": String(patch_size),
    //     "r": String(patch_size),
    //     "stroke-width": width,
    //     "stroke": stroke,
    //     "r": String(patch_size),
    //     "cy": String(y),
    //     "cx": String(x + patch_size),
    //     "fill": fill,
    //     "pointer-events": "none",
    //     })
    // patch.addClass("patch")
    // patch.id = id


    var patch = document.createElementNS('http://www.w3.org/2000/svg', 'circle')
    patch.setAttribute("r", String(patch_size))
    patch.setAttribute("stroke-width", width)
    patch.setAttribute("stroke", stroke)
    patch.setAttribute("cy", String(y))
    patch.setAttribute("cx", String(x + patch_size))
    patch.setAttribute("fill", fill)
    patch.setAttribute("pointer-events", "none")
    patch.classList.add("patch")
    patch.id = id
    parent.appendChild(patch)
  }

  function draw_arrow(parent, x1, y1, x2, y2, stroke, width, id) {
    var arrow = document.createElementNS('http://www.w3.org/2000/svg', 'line')
    arrow.setAttribute("x1", x1)
    arrow.setAttribute("y1", y1)
    arrow.setAttribute("x2", x2)
    arrow.setAttribute("y2", y2)
    arrow.setAttribute("stroke-width", width)
    arrow.setAttribute("stroke", stroke)
    arrow.setAttribute("marker-end", "url(#arrowhead" + stroke + "nooffset)")
    arrow.setAttribute("pointer-events", "none")
    arrow.classList.add("arrow")
    arrow.id = id
    parent.appendChild(arrow)
  }  

  function draw_label(parent, x, y, patch_size, x_spacing, id, ptextfull) {
    var ptextlines = []
    var maxlength = (x_spacing - patch_size * 6) / 5
    var notdone = true
    while (notdone) {
      if (ptextfull.length <= maxlength) {
        ptextlines.push(ptextfull)
        notdone = false
      }
      else {
        var ptexttemp = ptextfull.slice(0, maxlength)
        ptexttemp = ptexttemp.slice(0, ptexttemp.lastIndexOf(" "))
        ptextlines.push(ptexttemp)
        ptextfull = ptextfull.slice(ptexttemp.length + 1, ptextfull.length)
      }
    }
    if (ptextlines.length == 1) {
      var patchtext = document.createElementNS('http://www.w3.org/2000/svg', 'text')
      patchtext.setAttribute("x", String(x + patch_size * 4))
      patchtext.setAttribute("y", String(y + patch_size * 1 - 2))
      patchtext.setAttribute("style", "text-align:left; font-size:10px")
      patchtext.setAttribute("pointer-events", "none")
      patchtext.classList.add("patchtext")
      patchtext.id = "patchtext" + String(id)
      patchtext.textContent = ptextlines[0]
      parent.appendChild(patchtext)
    }
    else {
      var patchtext = document.createElementNS('http://www.w3.org/2000/svg', 'text')
      patchtext.setAttribute("x", String(x + patch_size * 4))
      patchtext.setAttribute("y", String(y + patch_size * 1 - 2 - patch_size * 1.2))
      patchtext.setAttribute("style", "text-align:left; font-size:10px")
      patchtext.setAttribute("pointer-events", "none")
      patchtext.classList.add("patchtext")
      patchtext.id = "patchtext" + String(id) + String(0)
      patchtext.textContent = ptextlines[0]
      parent.appendChild(patchtext)
      var patchtext = document.createElementNS('http://www.w3.org/2000/svg', 'text')
      patchtext.setAttribute("x", String(x + patch_size * 4))
      patchtext.setAttribute("y", String(y + patch_size * 1 - 2 + patch_size * 1.2))
      patchtext.setAttribute("style", "text-align:left; font-size:10px")
      patchtext.setAttribute("pointer-events", "none")
      patchtext.classList.add("patchtext")
      patchtext.id = "patchtext" + String(id) + String(1)
      patchtext.textContent = ptextlines[1]
      parent.appendChild(patchtext)
    }
  }

  var legendbox = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
  legendbox.setAttribute("x", String(x_limit))
  legendbox.setAttribute("y", String(1))
  legendbox.setAttribute("height", String(y_limit - 1))
  legendbox.setAttribute("width", String(params["Plot_width"] - x_limit - 1))
  legendbox.setAttribute("stroke-width", 1)
  legendbox.setAttribute("stroke", "lightgrey")
  legendbox.setAttribute("fill", "white")
  legendbox.setAttribute("pointer-events", "none")
  legendbox.classList.add("legendbox", "rect")
  legendbox.id = "legendbox"
  svg.appendChild(legendbox)

  var group = 0

  if (params.Apply_groups) {
    
    var x = params["Plot_width"] - (per_row - 0 % per_row) * x_spacing - box_pad
    var y = (Math.floor(0 / per_row) + 0.5) * y_spacing + y_offset + box_pad
    draw_patch(svg, x, y, patch_size, "none", 0, "black", "patch" + "Group")
    draw_label(svg, x, y, patch_size, x_spacing, 0, "Group")
    group = 1
  }

  var counter = 0

  for (let i = 0; i < Object.keys(colour_ref).length; i++) {
    counter = i
    var x = params["Plot_width"] - (per_row - (i + group) % per_row) * x_spacing - box_pad
    var y = (Math.floor((i + group) / per_row) + 0.5) * y_spacing + y_offset + box_pad
    var ptextfull = Object.keys(colour_ref)[i]

    draw_patch(svg, x, y, patch_size, "none", 0, colour_ref[Object.keys(colour_ref)[i]], "patch" + String(i))

    draw_label(svg, x, y, patch_size, x_spacing, i + group, ptextfull)
  }
  counter ++
  var type, stroke, fill, text

  for (let i=0; i<additional.length; i++) {
    type = additional[i][0]
    stroke = additional[i][1]
    fill = additional[i][2]
    text = additional[i][3]

    var x = params["Plot_width"] - (per_row - (i + group + counter) % per_row) * x_spacing - box_pad
    var y = (Math.floor((i + group + counter) / per_row) + 0.5) * y_spacing + y_offset + box_pad
    
    if (type =="patch") {

      draw_patch(svg, x, y, patch_size, stroke, 1, fill, "patch" + String(i + counter))
    }
    else if (type =="arrow") {

      draw_arrow(svg, x-3, y, x + 13, y, stroke, 1, "arrow" + String(i + counter))
    }
    
    draw_label(svg, x, y, patch_size, x_spacing, String(i + counter), text)
  
  }

}
