import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.logging.Logger;

public class Main {
  private static final Logger LOGGER = Logger.getLogger(Main.class.getName());
  private static final byte[] BUFFER = new byte[1024];
  public static void main(String[] args) throws Exception {
    ExecutorService executor = Executors.newFixedThreadPool(12);
    GameMaster gameMaster = new GameMaster();
    SessionManager sessionManager = new SessionManager();
    int serverPort = 3116;

    Thread UDPServerThread = new Thread(() -> {
      try {
        LOGGER.info("UDP - Starting thread...");
        DatagramSocket socket = new DatagramSocket(serverPort);
        while (true) {
            DatagramPacket inPacket = new DatagramPacket(BUFFER, BUFFER.length);
            socket.receive(inPacket);

            executor.execute(() -> {
              LOGGER.info("UDP - Request received!");
              try {
                String inData = new String(inPacket.getData(), 0, inPacket.getLength(), StandardCharsets.UTF_8);
                String senderLocation = inPacket.getAddress().toString().substring(1) + ":" + inPacket.getPort();
                TTTHandler handler = new TTTHandler(socket, gameMaster, sessionManager);
                boolean isClientDone = handler.handleRequest("t3udp://", inData, senderLocation);
              } catch (Exception e) {
                e.printStackTrace();
              }
            });
        }
      } catch (Exception e) {
        e.printStackTrace();
      }
    });
    Thread TCPServerThread = new Thread(() -> {
      try {
        LOGGER.info("TCP - Starting thread...");
        ServerSocket tcpSocket = new ServerSocket(serverPort);
        do {
          Socket socket = tcpSocket.accept();

          executor.execute(() -> {  // open a stream per user
            LOGGER.info("TCP - Request received!");

            byte[] buffer = new byte[1024];
            int bytesRead;

            try {
              boolean isClientDone = false;
              do {  // r/programminghorror
                TTTHandler handler = new TTTHandler(socket, gameMaster, sessionManager);
                while ((bytesRead = socket.getInputStream().read(buffer)) != -1) {
                  isClientDone = handler.handleRequest("t3tcp://", new String(buffer, 0, bytesRead), socket.getInetAddress() + ":" + socket.getPort());
                }
              } while (!isClientDone);
              socket.close();
              LOGGER.info("TCP - thread STOPPED.");
            } catch (Exception e) {
              e.printStackTrace();
            }
          });
        } while (true);
      } catch (Exception e) {
        e.printStackTrace();
      }
    });

    UDPServerThread.start();
    TCPServerThread.start();
  }
}
