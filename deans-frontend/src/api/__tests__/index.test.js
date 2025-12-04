jest.mock("../index.js"); // this will search for index.js at __mocks__ folder

const api = require("../index.js"); // this will search for index.js at api folder

describe("getCrises()", () => {
  it("should load crises", () => {
    return api.getCrises().then(data => {
      expect(data).toBeDefined();
    });
  });
});

describe("getCrisisType()", () => {
  it("should load crisis type", () => {
    return new Promise(resolve => resolve(true)); // TODO
  });
});

describe("getAssistanceType()", () => {
  it("should load assistance type", () => {
    return new Promise(resolve => resolve(true)); // TODO
  });
});

describe("getEmergencyAgencies()", () => {
  it("should load emergency agencies", () => {
    return new Promise(resolve => resolve(true)); // TODO
  });
});

describe("getHumidity()", () => {
  it("should load humidity", () => {
    return new Promise(resolve => resolve(true)); // TODO
  });
});

describe("getPSI()", () => {
  it("should load PSI", () => {
    return new Promise(resolve => resolve(true)); // TODO
  });
});

describe("getRainfall()", () => {
  it("should load rainfall", () => {
    return new Promise(resolve => resolve(true)); // TODO
  });
});

describe("getTemperature()", () => {
  it("should load temperature", () => {
    return new Promise(resolve => resolve(true)); // TODO
  });
});
