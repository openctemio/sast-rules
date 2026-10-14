class C {
  void a(javax.servlet.http.HttpServletResponse response) {
    javax.servlet.http.Cookie cookie = new javax.servlet.http.Cookie("id", "1");
    // ruleid: openctem.java.web.cookie-missing-httponly
    response.addCookie(cookie);
  }
  void b(javax.servlet.http.HttpServletResponse response) {
    javax.servlet.http.Cookie c2 = new javax.servlet.http.Cookie("id", "1");
    c2.setHttpOnly(true);
    // ok: openctem.java.web.cookie-missing-httponly
    response.addCookie(c2);
  }
}
