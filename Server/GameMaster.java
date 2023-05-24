import java.util.HashMap;
import java.util.Map;

public class GameMaster {
  private final String ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  private final int CODE_LENGTH = 4;
  private Map<String, Game> gameMap;

  public GameMaster() {
    gameMap = new HashMap<>();
  }

  public String addGame(String playerOne) {
    // generate the game code
    String code;
    do {
        code = generateCode();
    } while (this.gameMap.containsKey(code));

    Game game = new Game(playerOne);

    this.gameMap.put(code, game);

    // TODO: take out
    System.out.println(gameMap);

    return code;
  }

    public void addPlayer(String code, String playerTwo) {
        Game game = this.gameMap.get(code);
        game.addPlayer(playerTwo);
    }

  private String generateCode() {
    StringBuilder code = new StringBuilder();
    for (int i = 0; i < CODE_LENGTH; i++) {
      code.append(ALPHABET.charAt((int) (Math.random() * ALPHABET.length())));
    }
    return code.toString();
  }
}
