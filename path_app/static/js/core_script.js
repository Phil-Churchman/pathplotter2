var edited_gantt_params = {};
var edited_network_params = {};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function sendPOSTRequest(data, dest) {
  let form = document.createElement("form");
  form.setAttribute("method", "post");
  form.setAttribute("action", dest);

  const csrftoken = getCookie("csrftoken");

  let csrf = document.createElement("input");
  csrf.setAttribute("type", "hidden");
  csrf.setAttribute("name", "csrfmiddlewaretoken");
  csrf.setAttribute("value", csrftoken);
  form.appendChild(csrf);
  let post_data = document.createElement("input");
  json_data = JSON.stringify(data);

  post_data.setAttribute("name", "post_data");
  post_data.setAttribute("value", json_data);

  form.style.display = "none";
  form.appendChild(post_data);

  document.body.appendChild(form);
  form.submit();
}

function saveGroup(id) {
  sendAJAXRequest(id, "/save_group/");
}

function saveSwitch(data) {
  sendAJAXRequest(data, "/switch/");
  data = JSON.parse(data);
  var id = data["id"];

  var items = Array.from(document.getElementsByClassName("item" + String(id)));
  for (let i = 0; i < items.length; i++) {
    items[i].classList.toggle("parent");
    items[i].classList.toggle("parent-disabled");
  }
}

function sendAJAXRequest(post_data, dest) {
  // e.preventDefault();
  $.post(
    dest,
    {
      post_data: post_data,
      csrfmiddlewaretoken: getCookie("csrftoken"),
    }
    //
  );
}

function editItem(evt) {
  var selectedElement = evt.target;
  var id = selectedElement.id.toString();
  var classes = selectedElement.classList;
  if (classes.contains("node")) {
    open("../edit-node/" + id, "_self");
  } else if (classes.contains("link")) {
    open("../edit-link/" + id, "_self");
  } else if (classes.contains("link_mid")) {
    open("../edit-link/" + id.slice(0, id.length - 5), "_self");
  }
  // else if (id == "network") {
  //   open("../add-node-placed/" + String(evt.x) + "/" + String(evt.y) + "/", "_self")
  // }
}

function changeParam(type, param, value) {
  if (type == "gantt") {
    edited_gantt_params[param] = value;
  } else {
    edited_network_params[param] = value;
  }
  sendAJAXRequest(JSON.stringify([type, param, value]), "/edit-param-post/");
}

function submitelement(label) {
  const formelement = document.getElementById(label);

  formelement.addEventListener("change", function () {
    formelement.getElementById(label).submit();
  });
}

function check(message) {
  console.log(message);
}

function exportSVG(id) {
  saveSvgAsPng(document.getElementById(id), "diagram.png", {
    backgroundColor: "white",
  });
}

function updateLoops() {
  sendAJAXRequest(JSON.stringify([]), "/update_loops/");
}

function delAJAX(data) {
  var parsed_data = JSON.parse(data);
  const row = document.getElementById("row" + String(parsed_data["id"]));
  row.addEventListener("click", function (event) {
    event.preventDefault();
  });
  sendAJAXRequest(data, "/del-ajax/");
  row.remove();
}

function archiveAJAX(data) {
  var parsed_data = JSON.parse(data);
  const row = document.getElementById("row" + String(parsed_data["id"]));
  row.addEventListener("click", function (event) {
    event.preventDefault();
  });
  sendAJAXRequest(data, "/archive-ajax/");
  row.remove();
}

function standardAJAX(data) {
  sendAJAXRequest(data, "/add_link_standard/");

  var data = JSON.parse(data);
  var id = data["id"];
  var remove = data["remove"];

  var icon = document.getElementById("link" + remove + String(id));
  icon.classList.toggle("standard");
  icon.classList.toggle("standard-clicked");
  setTimeout(() => {
    icon.classList.toggle("standard");
    icon.classList.toggle("standard-clicked");
  }, 500);
}

function setversionAJAX(data) {
  sendAJAXRequest(JSON.stringify(data), "/set_version_ajax/");
  var selected = document.getElementById("version" + String(data["id"]));
  selected.addEventListener("click", function (event) {
    event.preventDefault();
  });
  var prev_selected = document.getElementsByClassName("table-active");
  if (prev_selected.length > 0) {
    for (let i = 0; i < prev_selected.length; i++) {
      prev_selected[i].className = "";
    }
    selected.className = "table-active";
  }
}

function saveEnabledOnly(checked) {
  sendPOSTRequest(checked, "/enabled_loops_only/");
}
