class Vertex extends Highlightable {
  constructor(x, y, color) {
    super();
    this.x = x;
    this.y = y;
    this.color = color;
    this.r = 5;
    this.scale = 1;
    this.offsetX = 0;
    this.offsetY = 0;
    this.transformedX = x;
    this.transformedY = y;
  }

  draw() {
    fill(this.isHighlighted ? color(255, 0, 0) : this.color);
    ellipse(this.transformedX, this.transformedY, this.r, this.r);
    noFill();
  }
  updateCoordinates() {
    this.transformedX = this.x * this.scale + this.offsetX;
    this.transformedY = this.y * this.scale + this.offsetY;
  }

  setOffsetX(val) {
    this.offsetX = val;
    this.updateCoordinates();
  }
  setOffsetY(val) {
    this.offsetY = val;
    this.updateCoordinates();
  }
  setScale(val) {
    this.scale = val;
    this.updateCoordinates();
  }
}
