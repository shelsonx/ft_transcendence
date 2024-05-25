import {
  CANVAS_HEIGHT_DEFAULT,
  CANVAS_WIDTH_DEFAULT,
  HEIGHT_FACTOR,
  WIDTH_FACTOR,
} from "../constants/game.js";

export const proportionalHeight = (size) => {
  return innerHeight * HEIGHT_FACTOR < CANVAS_HEIGHT_DEFAULT
    ? Math.ceil((size / CANVAS_HEIGHT_DEFAULT) * innerHeight * HEIGHT_FACTOR)
    : size;
};

export const proportionalWidth = (size) => {
  return innerWidth * WIDTH_FACTOR < CANVAS_WIDTH_DEFAULT
    ? Math.ceil((size / CANVAS_WIDTH_DEFAULT) * innerWidth * WIDTH_FACTOR)
    : size;
};

export const canvasWidth = () => {
  return innerWidth * WIDTH_FACTOR >= CANVAS_WIDTH_DEFAULT
    ? CANVAS_WIDTH_DEFAULT
    : innerWidth * WIDTH_FACTOR;
};

export const canvasHeight = () => {
  return innerHeight * HEIGHT_FACTOR >= CANVAS_HEIGHT_DEFAULT
    ? CANVAS_HEIGHT_DEFAULT
    : innerHeight * HEIGHT_FACTOR;
};
