function set(obj, parts, value) {
  let cur = obj
  for (let i = 0; i < parts.length - 1; i++) {
    // ruleid: openctem.javascript.injection.prototype-pollution-walk
    cur = cur[parts[i]]
  }
  cur[parts[parts.length - 1]] = value
}
function get(obj) {
  let cur = obj
  // ok: openctem.javascript.injection.prototype-pollution-walk
  cur = cur["fixed"]
  return cur
}
