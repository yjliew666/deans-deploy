const fs = require("fs");

// test fetch crises
export const getCrises = () =>
  new Promise((resolve, reject) => {
    // load mockedData
    fs.readFile("src/api/__mockData__/crises.json", "utf8", (err, data) => {
      if (err) reject(err);
      resolve(JSON.parse(data));
    });
  });
