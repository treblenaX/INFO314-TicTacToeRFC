import Game.GameState;

import java.net.DatagramSocket;
import java.net.Socket;
import java.util.*;
import java.util.logging.Logger;

public class TTTHandler {

  private final Logger LOGGER = Logger.getLogger(TTTHandler.class.getName());
   private final List<String> SUPPORTED_PROTOCOLS = new ArrayList<>(Arrays.asList("1"));
  private final byte[] BUFFER = new byte[1024];
  private Integer PORT = 3116;
  private GameMaster gameMaster;
  private SessionManager sessionManager;
  private DatagramSocket udpSocket;
  private Socket tcpSocket;

  public TTTHandler(DatagramSocket udpSocket, GameMaster gameMaster, SessionManager sessionManager) {
    this.udpSocket = udpSocket;
    this.gameMaster = gameMaster;
    this.sessionManager = sessionManager;
  }

  public TTTHandler(Socket tcpSocket, GameMaster gameMaster, SessionManager sessionManager) {
    this.tcpSocket = tcpSocket;
    this.gameMaster = gameMaster;
    this.sessionManager = sessionManager;
  }

  public boolean handleRequest(String prefix, String input, String senderLocation) throws Exception {
    String[] tokens = input.split(" ");
    String command = tokens[0].toUpperCase(); // commands are case-insensitive

    LOGGER.info(Arrays.toString(tokens));

    switch (command) {
      case "CREA":  // create a new game
        String playerName = tokens[1];
        String gameCode = gameMaster.createGame();
        gameMaster.joinGame(gameCode, playerName);

        LOGGER.info("CREA - game created - " + gameCode);

        String response = "JOND " + playerName + " " + gameCode;
        sessionManager.getSession(playerName).send(response.trim());
        return false;
      case "GDBY":  // goodbye - finished with session
        playerName = sessionManager.findPlayerNameFromIP(prefix + senderLocation);

        if ((gameCode = gameMaster.isPlayerInGame(playerName)) != null) {
          gameMaster.playerQuitGame(gameCode, playerName);
        }

        response = "GDBY";
        sessionManager.getSession(playerName).send(response.trim());
        sessionManager.endSession(playerName);
        return true;
      case "HELO":  // initiate a session
        String protocol = tokens[1];
        playerName = tokens[2];

        // check protocol for compatibility
        if (!SUPPORTED_PROTOCOLS.contains(protocol)) {
          protocol = SUPPORTED_PROTOCOLS.get(SUPPORTED_PROTOCOLS.size() - 1);
        }

        UUID uuid;
        do {
          uuid = UUID.randomUUID();
        } while (sessionManager.isUserInSession(uuid.toString()));

        if (udpSocket != null) {
          sessionManager.addSession(udpSocket, playerName, uuid.toString(), senderLocation.split(":")[0], Integer.parseInt(senderLocation.split(":")[1]));
        } else {
          sessionManager.addSession(tcpSocket, playerName, uuid.toString(), senderLocation.split(":")[0], Integer.parseInt(senderLocation.split(":")[1]));
        }

        response = "SESS " + protocol + " " + uuid;
        sessionManager.getSession(playerName).send(response.trim());
        return false;
      case "JOIN":  // join an existing game
        gameCode = tokens[1];
        playerName = sessionManager.findPlayerNameFromIP(prefix + senderLocation);
        gameMaster.joinGame(gameCode, playerName);

        response = "JOND " + playerName + " " + gameCode;
        sessionManager.getSession(playerName).send(response.trim());

        Thread.sleep(1000);

        // if game is full - start game - send YRMV
        if (gameMaster.isGamePlayersFull(gameCode)) {
          response = "YRMV " + gameCode + " " + gameMaster.whoseTurnInGame(gameCode);
          for (String player : gameMaster.getGamePlayers(gameCode)) {
            sessionManager.getSession(player).send(response.trim());
          }
        }
        return false;
      case "LIST":  // list all games
        String filter = (tokens.length > 1) ? tokens[1] : "";
        playerName = sessionManager.findPlayerNameFromIP(prefix + senderLocation);
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

        response = "GAMS";
        for (String gameId : list) response += " " + gameId;
        sessionManager.getSession(playerName).send(response.trim());
        return false;
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

        if (gameMaster.isGameEnded(gameCode)) { // win/tie condition
          String termResponse = (!gameMaster.getGameWinner(gameCode).equals(""))
                  ? gameCode + " " + gameMaster.getGameWinner(gameCode) + " KTHXBYE"
                  : gameCode + " KTHXBYE";

          response = "TERM " + termResponse;
          for (String player : gameMaster.getGamePlayers(gameCode)) {
            sessionManager.getSession(player).send(response.trim());
          }
          break;
        }

        // Send board response
        response = "BORD " + boardResponse;
        for (String player : gameMaster.getGamePlayers(gameCode)) {
          sessionManager.getSession(player).send(response.trim());
        }
        // Say whose turn it is next
        response = "YRMV " + gameCode + " " + gameMaster.whoseTurnInGame(gameCode);
        for (String player : gameMaster.getGamePlayers(gameCode)) {
          sessionManager.getSession(player).send(response.trim());
        }
        return false;
      case "QUIT":  // quit a game
        // abandon game without terminating session
        gameCode = tokens[1];
        playerName = sessionManager.findPlayerNameFromIP(prefix + senderLocation);

        response = "TERM " + gameCode + this.gameMaster.getGameWinner(gameCode) + " KTHXBYE";
        for (String player : gameMaster.getGamePlayers(gameCode)) {
          sessionManager.getSession(player).send(response.trim());
        }

        gameMaster.playerQuitGame(gameCode, playerName);
        return false;
      case "STAT":  // get game status
        gameCode = tokens[1];
        playerName = sessionManager.findPlayerNameFromIP(prefix + senderLocation);
        response = "BORD " + gameMaster.getGameStatus(gameCode);
        sessionManager.getSession(playerName).send(response.trim());
        return false;
      default:  // undefined command
        throw new Error("Unable to understand command.");
    }
    return false;
  }
}