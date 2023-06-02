import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Game.Game;
import Game.GameState;

public class GameMaster {
  private final String ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  private final int CODE_LENGTH = 4;
  private Map<String, Game> gameMap;

  public GameMaster() {
    gameMap = new HashMap<>();
  }

  public String createGame() {
    String code;
    do {
      code = generateCode();
    } while (this.gameMap.containsKey(code));

    Game game = new Game(code);

    this.gameMap.put(code, game);

    return code;
  }

  public void joinGame(String code, String player) {
    Game game = this.gameMap.get(code);
    game.addPlayer(player);
  }

  public String getGameStatus(String code) {
    return this.gameMap.get(code).getGameStatus();
  }

  public List<String> getGames() {
    List<String> gameIds = new ArrayList<>();

    for (String key : this.gameMap.keySet()) {
      gameIds.add(key);
    }

    return gameIds;
  }

  public List<String> getGames(GameState... state) {
    List<String> gameIds = new ArrayList<>();

    for (Map.Entry<String, Game> entry : this.gameMap.entrySet()) {
      GameState gameState = entry.getValue().getGameState();
      for (GameState s : state) {
        if (gameState == s) {
          gameIds.add(entry.getKey());
          break;
        }
      }
    }

    return gameIds;
  }

  public String moveInGame(String code, int linearPoint) {
    return this.gameMap.get(code).move(linearPoint);
  }
  public String moveInGame(String code, int x, int y) {
    return this.gameMap.get(code).move(x, y);
  }

  public boolean isGamePlayersFull(String code) {
    return this.gameMap.get(code).isPlayersFull();
  }

  public List<String> getGamePlayers(String code) {
    return this.gameMap.get(code).getPlayers();
  }

  public String whoseTurnInGame(String code) {
    return this.gameMap.get(code).whoseTurn();
  }

  public void playerQuitGame(String code, String playerName) {
    Game game = this.gameMap.get(code);
    game.quitGame(playerName);
    if (game.getPlayers().size() == 0) {  // end the game since no players
      this.gameMap.remove(code);
    }
  }

  public String isPlayerInGame(String playerName) {
    for (Map.Entry<String, Game> gameEntry : this.gameMap.entrySet()) {
      if (gameEntry.getValue().isPlayerInGame(playerName)) return gameEntry.getKey();
    }
    return null;
  }

  public String getGameWinner(String code) {
    return (this.gameMap.get(code).getWinner() == null) ? "" : this.gameMap.get(code).getWinner();
  }

  public boolean isGameEnded(String code) {
    return this.gameMap.get(code).getGameState() == GameState.FINISHED;
  }

  private String generateCode() {
    StringBuilder code = new StringBuilder();
    for (int i = 0; i < CODE_LENGTH; i++) {
      code.append(ALPHABET.charAt((int) (Math.random() * ALPHABET.length())));
    }
    return code.toString();
  }
}
