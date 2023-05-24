import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.logging.Logger;

public class UDPTTTServer {
  private final Logger LOGGER = Logger.getLogger(UDPTTTServer.class.getName());

  private Integer port;
  private UDPTTTServer instance;
  private byte[] BUFFER = new byte[1024];

  public UDPTTTServer(int port) throws Exception {
    this.port = port;
  }

  public void init() throws Exception {
    LOGGER.info("INIT - TTTServer");
    
    ExecutorService executor = Executors.newFixedThreadPool(10);
    DatagramSocket socket = new DatagramSocket(this.port);
    LOGGER.info("LISTENING - TTTServer - " + this.port);

    do {
      DatagramPacket inPacket = new DatagramPacket(BUFFER, BUFFER.length);
      socket.receive(inPacket);
      LOGGER.info("RECEIVED - TTTServer");
      executor.execute(() -> {
        try {
          String inData = new String(inPacket.getData());

          // process the data
          handleClientRequest(inData);
          // return the response
          DatagramPacket outPacket = new DatagramPacket(inData.getBytes(), inData.getBytes().length, inPacket.getAddress(), inPacket.getPort());
        } catch (Exception e) {
          e.printStackTrace();
        }
      });
    } while (true);

  }

  private void handleClientRequest(String data) {
    String[] tokens = data.split(" ");
    String command = tokens[0];

    switch (command) {
      case "CREA":  // create a new game

        // respond with JOIN <gid>
        break;
      case "GDBY":  // goodbye - finished with session
        // client wants to quit
        break;
      case "HELO":  // initiate a session
        String protocol = tokens[1];
        String cid_1 = tokens[2];

        // respond with SESS <protocol> <sessionID>
        break;
      case "JOIN":  // join an existing game

        // respond with JOND <cid> <gid>
        // if game is full - send YRMV
        break;
      case "LIST":  // list all games
        // if no body - respond with GAMS (open)
        // if has CURR - respond with GAMS (open | in-play)
        // if has ALL - respond with GAMS (open | in-play | finished)

        // respond with GAMS <gid_1> <gid_2> ... <gid_n>
        break;
      case "MOVE":  // make a move
        // must accept linear value (0-8)
        // must accept "X,Y" value (1-3,1-3)

        // must evaluate legality

        // respond with BORD <gid> <cid_1>(X - first) <cid_2>(O - second) <cid_m>(who moves next) <board>
        break;
      case "QUIT":  // quit a game
        // abandon game without terminating session
        // player opposite of quitter is WINNER
        break;
      case "STAT":  // get game status
        // needs <gid> body
        // respond with status
        break;
      default:  // undefined command
        throw new Error("Unable to understand command.");
    }
  }
}