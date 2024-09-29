function setup() {
  const cnv = createCanvas(600, 500);
  cnv.parent("canvas-container");
  cnv.mouseWheel(cnvMouseWheel);
  cnv.mousePressed(cnvMousePressed);
  cnv.mouseReleased(cnvMouseReleased);
  organizer = new Organizer();
  organizer.setData(nodes, meshData);

  const resizeHandle = document.getElementById("resize-handle");

  resizeHandle.addEventListener("mousedown", startResize);
  window.addEventListener("mousemove", resize);
  window.addEventListener("mouseup", stopResize);

  resizeCanvas(canvasContainer.clientWidth, canvasContainer.clientHeight);
}
function draw() {
  background(255);
  strokeWeight(0.2);
  stroke(123);

  organizer.draw();
}

function cnvMouseWheel(event) {
  event.preventDefault();
  scaleValue += event.deltaY < 0 ? 20 : -20;
  organizer.nodes.forEach((node) => {
    node.setScale(scaleValue);
  });
}
function cnvMousePressed(e) {
  controls.viewPos.isDragging = true;
  controls.viewPos.prevX = e.clientX;
  controls.viewPos.prevY = e.clientY;
}

function mouseDragged(e) {
  const { prevX, prevY, isDragging } = controls.viewPos;
  if (!isDragging) return;

  const pos = { x: e.clientX, y: e.clientY };
  const dx = pos.x - prevX;
  const dy = pos.y - prevY;

  if (prevX || prevY) {
    controls.view.x += dx;
    controls.view.y += dy;
    (controls.viewPos.prevX = pos.x), (controls.viewPos.prevY = pos.y);
  }
  organizer.nodes.forEach((node) => {
    node.setOffsetX(controls.view.x);
    node.setOffsetY(controls.view.y);
  });
}

function cnvMouseReleased() {
  controls.viewPos.isDragging = false;
  controls.viewPos.prevX = null;
  controls.viewPos.prevY = null;
}

function startResize(e) {
  isResizing = true;
}

function resize(e) {
  if (!isResizing) return;

  const newHeight = e.clientY - canvasContainer.getBoundingClientRect().top;

  canvasContainer.style.height = `${newHeight}px`;

  resizeCanvas(canvasContainer.clientWidth, newHeight);
}

function stopResize() {
  isResizing = false;
}

function windowResized() {
  resizeCanvas(canvasContainer.clientWidth, canvasContainer.clientHeight);
}
