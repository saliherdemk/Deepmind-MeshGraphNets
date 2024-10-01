function createBtn(text) {
  let btn = document.createElement("button");
  btn.classList.add("highlight-btn");

  btn.innerText = text;
  let [type, id] = text.split("-");

  let isMesh = type == "M";

  isMesh ? meshContainerButtons.push(btn) : vertexContainerButtons.push(btn);

  btn.onclick = () => {
    btn.classList.toggle("active");

    if (isMesh) {
      organizer.meshes[id].toggleHighlight(true);
    } else {
      organizer.nodes[id].toggleHighlight(true);
    }
  };
  return btn;
}

function loadData(data) {
  meshData = data.cells;

  nodes = data.mesh_pos;
  organizer.setData(nodes, meshData);
}

function highlightAllVertecies() {
  vertexContainerButtons.forEach((vertex) => {
    vertex.classList.add("active");
    organizer.nodes[vertex.innerText.split("-")[1]].highlight();
  });
}

function clearAllHighlightVertecies() {
  vertexContainerButtons.forEach((vertex) => {
    vertex.classList.remove("active");
    organizer.nodes[vertex.innerText.split("-")[1]].clearHighlight();
  });
}

function highlightAllMeshes() {
  meshContainerButtons.forEach((mesh) => {
    mesh.classList.add("active");
    organizer.meshes[mesh.innerText.split("-")[1]].highlight();
  });
}

function clearAllHighlightMeshes() {
  meshContainerButtons.forEach((mesh) => {
    mesh.classList.remove("active");
    organizer.meshes[mesh.innerText.split("-")[1]].clearHighlight();
  });
}

function zoomIn() {
  scaleValue += 10;
  organizer.nodes.forEach((node) => {
    node.setScale(scaleValue);
  });
}

function zoomOut() {
  scaleValue -= 10;
  organizer.nodes.forEach((node) => {
    node.setScale(scaleValue);
  });
}

document
  .querySelector('input[type="file"]')
  .addEventListener("change", function (event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    reader.onload = function () {
      try {
        data = JSON.parse(reader.result);
        loadData(data);
        organizer.setHeader(file.name);
      } catch (e) {
        alert("Invalid data");
      }
    };
    reader.readAsText(file);
  });

vertexCheckbox.addEventListener("change", function () {
  organizer.toggleNodes();
});
meshCheckbox.addEventListener("change", function () {
  organizer.toggleMeshes();
});
