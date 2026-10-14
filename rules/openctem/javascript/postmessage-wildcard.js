// ruleid: openctem.javascript.browser.postmessage-wildcard-origin
win.postMessage(messageName, "*");
// ok: openctem.javascript.browser.postmessage-wildcard-origin
win.postMessage(messageName, "https://app.example.com");
