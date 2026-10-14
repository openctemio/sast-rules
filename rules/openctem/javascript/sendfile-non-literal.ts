function serve(req: any, res: any, path: any) {
  const file = req.params.file
  // ruleid: openctem.javascript.express.sendfile-non-literal-path
  res.sendFile(path.resolve('ftp/', file))
  // ok: openctem.javascript.express.sendfile-non-literal-path
  res.sendFile('index.html')
  // ok: openctem.javascript.express.sendfile-non-literal-path
  res.sendFile(file, { root: 'public' })
}
