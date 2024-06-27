export function objValidation(class_type, obj) {
  const mustHaveKeys = [...class_type.mustHaveKeys];

  mustHaveKeys.forEach((key) => {
    if (!obj.hasOwnProperty(key)) {
      throw new Error(
        `Cannot create '${class_type.name}' from object.
        The object must have a '${key}' property.`
      );
    }
    if (obj[key] === undefined) {
      throw new Error(
        `Cannot create '${class_type.name}' from object.
        Key '${key}' is undefined.`
      );
    }
  });
}
