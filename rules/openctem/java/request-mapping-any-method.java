@RestController
class HashingController {
  @RequestMapping(path = "/crypto/hashing/md5")
  // ruleid: openctem.java.spring.request-mapping-any-method
  public String md5() { return ""; }

  @RequestMapping(path = "/x", method = RequestMethod.POST)
  // ok: openctem.java.spring.request-mapping-any-method
  public String post() { return ""; }
}
