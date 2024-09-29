var vertexContainerButtons = [];
var meshContainerButtons = [];
var organizer;
var scaleValue = 1;
var canvasHeight = 400;
let isResizing = false;
const controls = {
  view: { x: 0, y: 0, zoom: 1 },
  viewPos: { prevX: null, prevY: null, isDragging: false },
};
const vertexBtnContainer = document.getElementById("vertex-btn-container");
const meshBtnContainer = document.getElementById("mesh-btn-container");
const vertexCheckbox = document.getElementById("vertex-checkbox");
const meshCheckbox = document.getElementById("mesh-checkbox");
const canvasContainer = document.getElementById("canvas-container");
