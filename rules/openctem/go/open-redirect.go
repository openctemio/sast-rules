package main

import "net/http"

func h(w http.ResponseWriter, r *http.Request) {
	redirectURL := r.URL.Query().Get("to")
	// ruleid: openctem.go.web.open-redirect
	http.Redirect(w, r, redirectURL, http.StatusMovedPermanently)
	// ok: openctem.go.web.open-redirect
	http.Redirect(w, r, "/login", http.StatusFound)
}
