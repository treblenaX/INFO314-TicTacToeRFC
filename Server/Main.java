public class Main {
  public static void main(String[] args) throws Exception {
    UDPTTTServer server = new UDPTTTServer(31161);
    server.init();
  }
}
