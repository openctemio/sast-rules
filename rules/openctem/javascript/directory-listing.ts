// ruleid: openctem.javascript.express.directory-listing
app.use('/ftp', serveIndexMiddleware, serveIndex('ftp', { icons: true }))
// ok: openctem.javascript.express.directory-listing
app.use('/public', express.static('public'))
