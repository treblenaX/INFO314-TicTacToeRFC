import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Game {
  enum GameState {
    OPEN, 
    IN_PLAY,
    FINISHED
  }
  private List<String> players;
  private boolean isPlayerOneTurn;
  private char[][] gameBoard;
  private GameState gameState;

  public Game(String player) {
    this.players = new ArrayList<String>();
    this.players.add(player);
    this.gameState = GameState.OPEN;
  }

  public void addPlayer(String player) {
    this.players.add(player);

    if (this.players.size() == 2) { // all players are in - commence the game
      this.gameState = GameState.IN_PLAY;
      isPlayerOneTurn = new Random().nextBoolean();
    }
  }

  public void update() {
    switch (this.gameState) {
      case OPEN:  // wait for players
        break;
      case IN_PLAY: // game is in session!

        break;
      case FINISHED:  // game is over
        break;
    }
  }
}
