// should not generate diagnostics

const guard = { current: false };

export function runOnce() {
  if (guard.current) {
    return;
  }
  guard.current = true;
}

declare function useRef<T>(value: T): { current: T };

const booleanRef = useRef<boolean>(false);
if (booleanRef.current) {
  console.log("already set");
}
booleanRef.current = true;

const numberRef = useRef<number>(0);
if (numberRef.current) {
  console.log("already set");
}
numberRef.current = 1;

const initiallyTrue = { current: true };
if (initiallyTrue.current) {
  console.log("initially set");
}
initiallyTrue.current = false;
