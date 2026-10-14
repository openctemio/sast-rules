import javax.xml.parsers.*;
class X {
  DocumentBuilder a() throws Exception {
    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    // ruleid: openctem.java.xxe.document-builder-external-entities
    factory.setFeature("http://xml.org/sax/features/external-general-entities", true);
    // ruleid: openctem.java.xxe.document-builder-external-entities
    return factory.newDocumentBuilder();
  }
  DocumentBuilder b() throws Exception {
    DocumentBuilderFactory f = DocumentBuilderFactory.newInstance();
    f.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
    // ok: openctem.java.xxe.document-builder-external-entities
    return f.newDocumentBuilder();
  }
}
