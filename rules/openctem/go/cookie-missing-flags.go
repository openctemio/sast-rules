package main

import "net/http"

func set(w http.ResponseWriter) {
	// ruleid: openctem.go.web.cookie-missing-httponly
	http.SetCookie(w, &http.Cookie{Name: "sid", Value: "x"})
	// ok: openctem.go.web.cookie-missing-httponly
	http.SetCookie(w, &http.Cookie{Name: "sid", Value: "x", HttpOnly: true, Secure: true})
}
