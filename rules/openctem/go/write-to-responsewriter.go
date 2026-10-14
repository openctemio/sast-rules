package main

import (
	"fmt"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	data := r.URL.Query().Get("q")
	// ruleid: openctem.go.web.unescaped-write-to-response
	fmt.Fprint(w, data)
	// ruleid: openctem.go.web.unescaped-write-to-response
	w.Write([]byte(data))
	// ok: openctem.go.web.unescaped-write-to-response
	fmt.Fprint(w, "ok")
}

func wrap() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		data := r.FormValue("d")
		// ruleid: openctem.go.web.unescaped-write-to-response
		fmt.Fprint(w, data)
	}
}
