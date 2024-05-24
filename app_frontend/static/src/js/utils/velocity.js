const ratio = Math.PI / 180;

export const degToRad = (degrees) => {
  return degrees * ratio;
};

export const radToDeg = (radians) => {
  return radians / ratio;
};

export const rotate = (vector, angle) => {
  const newSlope = slope(vector) + angle;

  const { x, y } = vector;
  const magnitude = Math.sqrt(x * x + y * y);

  vector.x = Math.cos(newSlope) * magnitude;
  vector.y = Math.sin(newSlope) * magnitude;
  return vector;
}

export const slope = (vector) => Math.atan2(vector.y, vector.x);
