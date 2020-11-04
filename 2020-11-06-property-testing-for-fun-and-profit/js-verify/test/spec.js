import jsc from "jsverify";
import { describe } from "mocha";

describe("adding properties", () => {
    jsc.property("right identity", jsc.integer, n => (n + 0) === n);

    jsc.property("left identity", jsc.integer, n => (0 + n) === n);

    jsc.property("associativity", jsc.integer, jsc.integer, jsc.integer, (a, b, c) => (a + b) + c === a + (b + c));

    // jsc.property("bad identity oops", jsc.integer, n => n + 1 === n);
});
