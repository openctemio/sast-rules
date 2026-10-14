class Pin {
  // ruleid: openctem.java.crypto.weak-random
  public static final int PINCODE = new Random().nextInt(10000);
  // ok: openctem.java.crypto.weak-random
  public static final int SAFE = new java.security.SecureRandom().nextInt(10000);
}
