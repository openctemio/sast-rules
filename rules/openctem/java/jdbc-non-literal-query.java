import java.sql.*;
class Lesson {
  void run(Connection connection, String accountName) throws Exception {
    Statement statement = connection.createStatement();
    String query = "SELECT * FROM user_data WHERE last_name = '" + accountName + "'";
    // ruleid: openctem.java.sqli.jdbc-non-literal-query
    ResultSet results = statement.executeQuery(query);
    // ok: openctem.java.sqli.jdbc-non-literal-query
    ResultSet all = statement.executeQuery("SELECT * FROM user_data");
    // ruleid: openctem.java.sqli.jdbc-non-literal-query
    PreparedStatement ps = connection.prepareStatement("select password from users where userid = '" + accountName + "'");
    // ok: openctem.java.sqli.jdbc-non-literal-query
    PreparedStatement ps2 = connection.prepareStatement("select password from users where userid = ?");
  }
}
