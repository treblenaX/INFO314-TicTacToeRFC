import java.net.ServerSocket;
import java.net.Socket;
import java.util.logging.Logger;

public class TCPTTTServer {
  private final Logger LOGGER = Logger.getLogger(TCPTTTServer.class.getName());
  private Integer port;

  public TCPTTTServer(int port) throws Exception {
    this.port = port;
  }

//  public void init() throws Exception {
//    LOGGER.info("[TCP] - INIT - TTTServer");
//
//    Socket socket = new ServerSocket(this.port);
//
//  }
}
