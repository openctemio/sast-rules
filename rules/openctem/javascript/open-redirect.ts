export function performRedirect () {
  return ({ query }: any, res: any) => {
    const toUrl: string = query.to as string
    // ruleid: openctem.javascript.express.open-redirect
    res.redirect(toUrl)
    // ok: openctem.javascript.express.open-redirect
    res.redirect('/login')
  }
}
