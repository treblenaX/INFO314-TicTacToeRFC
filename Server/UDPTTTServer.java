import Game.Game;
import Game.GameState;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.logging.Logger;

public class UDPTTTServer {
  private final Logger LOGGER = Logger.getLogger(UDPTTTServer.class.getName());
  // private final Set<String> SUPPORTED_PROTOCOLS = new HashSet<String>(Arrays.asList("1"));
  private final byte[] BUFFER = new byte[1024];
  private Integer port;
  private Map<String, String> sessions;
  private GameMaster gameMaster;


  public UDPTTTServer(int port) throws Exception {
    this.port = port;
    this.sessions = new HashMap<>();
    this.gameMaster = new GameMaster();
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
          String inData = new String(inPacket.getData(), 0, inPacket.getLength(), StandardCharsets.UTF_8);
          String response = handleClientRequest(inData);
          LOGGER.info("RESPONSE - " + response);
          DatagramPacket outPacket = new DatagramPacket(response.getBytes(), response.getBytes().length, inPacket.getAddress(), inPacket.getPort());
          socket.send(outPacket);
        } catch (Exception e) {
          e.printStackTrace();
        }
      });
    } while (true);

  }

  private String handleClientRequest(String data) {
    String[] tokens = data.split(" ");
    String command = tokens[0].toUpperCase(); // commands are case-insensitive

    switch (command) {
      case "CREA":  // create a new game
        String playerName = tokens[1];

        String gameCode = gameMaster.addGame(playerName);
        LOGGER.info("CREA - game created - " + gameCode);

        // respond with JOND <cid> <gid>
        return "JOND " + playerName + " " + gameCode;
      case "GDBY":  // goodbye - finished with session
        // client wants to quit
        return "";
      case "HELO":  // initiate a session
        String protocol = tokens[1];
        String cid = tokens[2];

        UUID uuid;

        do {
          uuid = UUID.randomUUID();
        } while (sessions.containsKey(uuid.toString()));

        sessions.put(uuid.toString(), cid);

        System.out.println(sessions);

        // respond with SESS <protocol> <sessionID>
        return "SESS " + protocol + " " + uuid.toString();
      case "JOIN":  // join an existing game

        // respond with JOND <cid> <gid>
        // if game is full - send YRMV
        return "";
      case "LIST":  // list all games
        String filter = (tokens.length > 1) ? tokens[1] : "";
        List<String> list = new ArrayList<>();

        // if no body - respond with GAMS (open)
        // if has CURR - respond with GAMS (open | in-play)
        // if has ALL - respond with GAMS (open | in-play | finished)
        switch (filter) {
          case "CURR":
            list = gameMaster.getGames(GameState.OPEN, GameState.IN_PLAY);
            break;
          case "ALL":
            list = gameMaster.getGames();
            break;
          default:
            list = gameMaster.getGames(GameState.OPEN);
            break;
        }

        String response = "GAMS";
        for (String gameId : list) {
          response += " " + gameId;
        }
        // respond with GAMS <gid_1> <gid_2> ... <gid_n>
        return response;
      case "MOVE":  // make a move
        // must accept linear value (0-8)
        // must accept "X,Y" value (1-3,1-3)

        // must evaluate legality

        // respond with BORD <gid> <cid_1>(X - first) <cid_2>(O - second) <cid_m>(who moves next) <board>
        return "";
      case "QUIT":  // quit a game
        // abandon game without terminating session
        // player opposite of quitter is WINNER
        return "";
      case "STAT":  // get game status
        // needs <gid> body
        // respond with status
        return "";
      default:  // undefined command
        throw new Error("Unable to understand command.");
    }
  }
}