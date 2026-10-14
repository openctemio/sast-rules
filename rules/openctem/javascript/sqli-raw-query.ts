function search(models: any, criteria: string) {
  // ruleid: openctem.javascript.sqli.string-built-raw-query
  models.sequelize.query(`SELECT * FROM Products WHERE name LIKE '%${criteria}%'`)
  // ruleid: openctem.javascript.sqli.string-built-raw-query
  models.sequelize.query("SELECT * FROM Products WHERE name = '" + criteria + "'")
  // ok: openctem.javascript.sqli.string-built-raw-query
  models.sequelize.query('SELECT * FROM Products WHERE name = ?', { replacements: [criteria] })
}
