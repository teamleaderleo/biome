const objectBoolean = { current: false };
if (objectBoolean.current) {
  console.log("already set");
}
objectBoolean.current = true;

const objectNumber = { current: 0 };
if (objectNumber.current) {
  console.log("already nonzero");
}
objectNumber.current = 1;

const objectString = { current: "" };
if (objectString.current) {
  console.log("already nonempty");
}
objectString.current = "ready";

const nestedObject = { state: { ready: false } };
if (nestedObject.state.ready) {
  console.log("already ready");
}
nestedObject.state.ready = true;

declare function useRef<T>(value: T): { current: T };

const inferredBooleanRef = useRef(false);
if (inferredBooleanRef.current) {
  console.log("already set");
}
inferredBooleanRef.current = true;

const explicitBooleanRef = useRef<boolean>(false);
if (explicitBooleanRef.current) {
  console.log("already set");
}
explicitBooleanRef.current = true;

const inferredNumberRef = useRef(0);
if (inferredNumberRef.current) {
  console.log("already nonzero");
}
inferredNumberRef.current = 1;

interface MutableBox<T> {
  current: T;
}

const contextualBoolean: MutableBox<boolean> = { current: false };
if (contextualBoolean.current) {
  console.log("already set");
}
contextualBoolean.current = true;

const collection = [{ current: false }];
if (collection[0].current) {
  console.log("already set");
}
collection[0].current = true;
