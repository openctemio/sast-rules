class Exec {
  void run(java.util.List<String> command) throws Exception {
    // ruleid: openctem.java.injection.process-non-literal-command
    new ProcessBuilder(command).start();
    // ok: openctem.java.injection.process-non-literal-command
    new ProcessBuilder("uptime").start();
  }
}
