function pick(requestedFields: string[], user: any, baseUser: any) {
  for (const field of requestedFields) {
    // ruleid: openctem.javascript.injection.property-name-from-input
    baseUser[field] = user.data[field]
  }
  // ok: openctem.javascript.injection.property-name-from-input
  baseUser.name = user.data.name
}
