class Highlightable {
  constructor() {
    this.isHighlighted = false;
  }

  toggleHighlight() {
    this.isHighlighted = !this.isHighlighted;
    this.r = this.isHighlighted ? 7 : 5;
  }

  highlight() {
    this.isHighlighted = true;
    this.r = 7;
  }

  clearHighlight() {
    this.isHighlighted = false;
    this.r = 5;
  }
}
