class Mesh extends Highlightable {
  constructor(v1, v2, v3, color) {
    super();
    this.v1 = v1;
    this.v2 = v2;
    this.v3 = v3;
    this.color = color;
  }
  draw() {
    fill(this.isHighlighted ? color(255, 0, 0) : this.color);
    triangle(
      this.v1.transformedX,
      this.v1.transformedY,
      this.v2.transformedX,
      this.v2.transformedY,
      this.v3.transformedX,
      this.v3.transformedY,
    );
    noFill();
  }
}
