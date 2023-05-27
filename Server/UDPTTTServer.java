import Game.Game;
import Game.GameState;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.logging.Logger;

public class UDPTTTServer {
  class User {
    String uuid;
    String address;
    int port;

    public User(String uuid, String address, int port) {
      this.uuid = uuid;
      this.address = address;
      this.port = port;
    }

    public String toString() {
      return this.uuid + " " + this.address + " " + port;
    }
  }

  private final Logger LOGGER = Logger.getLogger(UDPTTTServer.class.getName());
  // private final Set<String> SUPPORTED_PROTOCOLS = new HashSet<String>(Arrays.asList("1"));
  private final byte[] BUFFER = new byte[1024];
  private Integer port;
  private Map<String, User> sessions;
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
          handleClientRequest(socket, inData, inPacket.getAddress().toString().substring(1) + ":" + Integer.toString(inPacket.getPort()));
        } catch (Exception e) {
          e.printStackTrace();
        }
      });
    } while (true);

  }

  private void handleClientRequest(DatagramSocket socket, String input, String senderLocation) throws Exception {
    String[] tokens = input.split(" ");
    String command = tokens[0].toUpperCase(); // commands are case-insensitive

    switch (command) {
      case "CREA":  // create a new game
        String playerName = tokens[1];
        String gameCode = gameMaster.createGame();
        gameMaster.joinGame(gameCode, playerName);
        LOGGER.info("CREA - game created - " + gameCode);

        respond(socket, "JOND " + playerName + " " + gameCode, senderLocation);
        break;
      case "GDBY":  // goodbye - finished with session
        // client wants to quit
        break;
      case "HELO":  // initiate a session
        String protocol = tokens[1];
        String cid = tokens[2];
        UUID uuid;
        do {
          uuid = UUID.randomUUID();
        } while (sessions.containsKey(uuid.toString()));
        sessions.put(cid, new User(uuid.toString(), senderLocation.split(":")[0], Integer.parseInt(senderLocation.split(":")[1])));

        respond(socket, "SESS " + protocol + " " + uuid.toString(), senderLocation);
        break;
      case "JOIN":  // join an existing game
        gameCode = tokens[1];
        playerName = findPlayerNameFromIP(senderLocation);
        gameMaster.joinGame(gameCode, playerName);
        respond(socket, "JOND " + playerName + " " + gameCode, senderLocation);

        // if game is full - start game - send YRMV
        if (gameMaster.isGamePlayersFull(gameCode)) {
          List<String> locations = new ArrayList<>();
          for (String s : gameMaster.getGamePlayers(gameCode)) {
            User u = this.sessions.get(s);
            locations.add(u.address + ":" + u.port);
          }

          respond(socket, "YRMV " + gameCode + " " + gameMaster.whoseTurnInGame(gameCode), locations.toArray(new String[0]));
        }
        break;
      case "LIST":  // list all games
        String filter = (tokens.length > 1) ? tokens[1] : "";
        List<String> list;

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

        String response = "";
        for (String gameId : list) response += " " + gameId;
        respond(socket, "GAMS" + response, senderLocation);

        break;
      case "MOVE":  // make a move
        gameCode = tokens[1];

        String boardResponse = "";
        if (tokens.length < 4) {  // must accept linear value (0-8)
          int linearPoint = Integer.parseInt(tokens[2]);
          boardResponse = gameMaster.moveInGame(gameCode, linearPoint);
        } else {  // must accept "X,Y" value (1-3,1-3)
          int x = Integer.parseInt(tokens[2]);
          int y = Integer.parseInt(tokens[3]);
          boardResponse = gameMaster.moveInGame(gameCode, x, y);
        }

        List<String> locations = new ArrayList<>();
        for (String s : gameMaster.getGamePlayers(gameCode)) {
          User u = this.sessions.get(s);
          locations.add(u.address + ":" + u.port);
        }

        // Send board response
        respond(socket, "BORD " + boardResponse, locations.toArray(new String[0]));

        // Say whose turn it is next
        respond(socket, "YRMV " + gameCode + " " + gameMaster.whoseTurnInGame(gameCode), locations.toArray(new String[0]));
        break;
      case "QUIT":  // quit a game
        // abandon game without terminating session
//        gameCode = tokens[1];
//        playerName = "";
//
//        for (Map.Entry<String, User> entry: this.sessions.entrySet()) {
//          if (Objects.equals(ipAddress + ":" + port, entry.getValue().address + ":" + entry.getValue().port)) {
//            playerName = entry.getKey();
//          }
//        }
//
//        String winner = gameMaster.playerQuitGame(gameCode, playerName);
//        return "BORD " + gameCode
//                + " " + players.get(0) + " " + players.get(1)
//                + " " + playerTurn + " " + gameMaster.getGameBoard(gameCode);
        break;
      case "STAT":  // get game status
        gameCode = tokens[1];
        System.out.println(this.gameMaster.getGameStatus(gameCode));
        respond(socket, "BORD " + this.gameMaster.getGameStatus(gameCode), senderLocation);
        break;
      default:  // undefined command
        throw new Error("Unable to understand command.");
    }
  }

  private void sendPackets(String payload, String... destinations) {

  }

  private void respond(DatagramSocket socket, String payload, String... destinations) throws Exception {
    for (String dest : destinations) {
      String address = dest.split(":")[0];
      int port = Integer.parseInt(dest.split(":")[1]);

      DatagramPacket outPacket = new DatagramPacket(payload.getBytes(), payload.getBytes().length, InetAddress.getByName(address), port);
      socket.send(outPacket);
    }
  }

  private String findPlayerNameFromIP(String sender) {
    String playerName = "";

    for (Map.Entry<String, User> entry: this.sessions.entrySet()) {
      if (Objects.equals(sender, entry.getValue().address + ":" + entry.getValue().port)) {
        playerName = entry.getKey();
      }
    }

    return playerName;
  }
}