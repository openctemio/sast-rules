import crypto from 'crypto'
// ruleid: openctem.javascript.crypto.hardcoded-key
export const hmac = (data: string) => crypto.createHmac('sha256', 'pa4qacea4VK9t9nGv7yZtwmj').update(data).digest('hex')
// ok: openctem.javascript.crypto.hardcoded-key
export const hmac2 = (data: string) => crypto.createHmac('sha256', process.env.HMAC_KEY as string).update(data).digest('hex')
