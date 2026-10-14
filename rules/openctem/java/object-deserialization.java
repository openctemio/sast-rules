import java.io.*;
class Helper {
  Object read(byte[] data) throws Exception {
    // ruleid: openctem.java.deserialization.object-input-stream
    ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
    return ois.readObject();
  }
  Object safe(byte[] data, ObjectInputFilter f) throws Exception {
    // ok: openctem.java.deserialization.object-input-stream
    ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
    ois.setObjectInputFilter(f);
    return ois.readObject();
  }
}
