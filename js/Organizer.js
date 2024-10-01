class Organizer {
  constructor() {
    this.nodes = [];
    this.meshes = [];
    this.showNodes = true;
    this.showMeshes = true;
    this.setHeader("Deepmind-MeshGraphNets");
  }

  setHeader(text) {
    document.getElementById("header").innerText = text;
  }

  setFrame(nodeData, meshData) {
    nodeData.forEach((node, index) => {
      this.nodes.push(new Vertex(node[0], node[1], color(0)));
      vertexBtnContainer.appendChild(createBtn("V-" + index));
    });

    meshData.forEach((mesh, index) => {
      let v1 = this.nodes[mesh[0]];
      let v2 = this.nodes[mesh[1]];
      let v3 = this.nodes[mesh[2]];

      this.meshes.push(new Mesh(v1, v2, v3, color(255)));
      meshBtnContainer.appendChild(createBtn(`M-${index}`));
    });
  }

  toggleNodes() {
    this.showNodes = !this.showNodes;
  }
  toggleMeshes() {
    this.showMeshes = !this.showMeshes;
  }

  reset() {
    this.nodes = [];
    this.meshes = [];
    vertexContainerButtons = [];
    meshContainerButtons = [];
    vertexBtnContainer.innerHTML = "";
    meshBtnContainer.innerHTML = "";
  }
  setData(nodes, meshes) {
    this.reset();
    this.setFrame(nodes, meshes);
  }

  draw() {
    this.showMeshes &&
      this.meshes.forEach((mesh) => {
        mesh.draw();
      });

    this.showNodes &&
      this.nodes.forEach((vertex) => {
        vertex.draw();
      });
  }
}
