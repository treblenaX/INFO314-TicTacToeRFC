package Game;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Game {
  private final int numRows = 3;
  private final int numCols = 3;

  private List<String> players;
  private boolean isPlayerOneTurn;
  private char[][] gameBoard;
  private GameState gameState;
  private String[] playerOne;
  private String[] playerTwo;
  private String gameCode;
  private String winner;
  private int connectedUsers;
  private int moves;


  public Game(String code) {
    this.gameState = GameState.OPEN;
    this.players = new ArrayList<>();
    this.playerOne = new String[]{"", "X"};
    this.playerTwo = new String[]{"", "O"};
    this.winner = null;
    this.gameCode = code;

    this.gameBoard = new char[numRows][numCols];
    for (int i = 0; i < numRows; i++) {
      for (int j = 0; j < numCols; j++) {
        this.gameBoard[i][j] = '*';
      }
    }

    this.connectedUsers = 0;
    this.moves = 0;
  }

  public String getGameStatus() {
    StringBuilder sb = new StringBuilder();
    sb.append("|");
    for (int i = 0; i < numRows; i++) {
      for (int j = 0; j < numCols; j++) {
        sb.append(gameBoard[i][j] + "|");
      }
    }

    // not started yet
    if (this.gameState == GameState.OPEN) {
      String p = "";
      for (String s : getPlayers()) p += s + " ";
      
      return this.gameCode + " " + p.trim();
    }

    String focusPlayer = (this.isPlayerOneTurn)
            ? this.playerOne[0]
            : this.playerTwo[0];

    // win condition
    if (this.gameState == GameState.FINISHED) {
      return gameCode + " "
              + playerOne[0] + " "
              + playerTwo[0] + " "
              + focusPlayer + " "
              + sb.toString() + " "
              + winner;
    }

    // still playing
    return gameCode + " "
            + playerOne[0] + " "
            + playerTwo[0] + " "
            + focusPlayer + " "
            + sb.toString();
  }

  public void addPlayer(String playerName) {
    if (connectedUsers == 0) {
      this.playerOne[0] = playerName;
    } else {
      this.playerTwo[0] = playerName;
    }

    connectedUsers++;

    this.players.add(playerName);

    if (connectedUsers == 2) {  // everyone is in - start the game
      this.gameState = GameState.IN_PLAY;
      this.isPlayerOneTurn = true;
    }
  }

  public boolean isPlayersFull() {
    return (this.playerOne != null && this.playerTwo != null);
  }

  public GameState getGameState() {
    return this.gameState;
  }

  public String move(int i) {
    String[] focusPlayer = (this.isPlayerOneTurn) ? this.playerOne : this.playerTwo;

    int rowIndex = (i - 1) / numRows;
    int colIndex = (i - 1) % numRows;

    char spot = gameBoard[rowIndex][colIndex];

    if (spot == '*') {  // spot is taken
      this.moves++;

      gameBoard[rowIndex][colIndex] = focusPlayer[1].charAt(0);
      this.isPlayerOneTurn = !this.isPlayerOneTurn;

      boolean win = checkWin(focusPlayer[1].charAt(0));

      // check for tie
      if (this.moves == numCols * numRows) {
        this.gameState = GameState.FINISHED;
        return this.getGameStatus();
      }

      if (win) {  // winner!
        this.gameState = GameState.FINISHED;
        this.winner = focusPlayer[0];
      }
    }

    return this.getGameStatus();
  }

  public String move(int x, int y) {
    return move(((x - 1) * numCols) + y);
  }

  public List<String> getPlayers() {
    return this.players;
  }
  public String whoseTurn() {
    return (isPlayerOneTurn) ? playerOne[0] : playerTwo[0];
  }

  public void quitGame(String playerName) {
    this.gameState = GameState.FINISHED;
    this.players.remove(playerName);
    this.winner = (playerName.equals(playerOne[0])) ? playerTwo[0] : playerOne[0];
  }

  public boolean isPlayerInGame(String playerName) {
    return (playerOne[0].equals(playerName) || playerTwo[0].equals(playerName));
  }

  public String getWinner() {
    return this.winner;
  }

  private boolean checkWin(char mark) {
    // Rows
    for (int i = 0; i < 3; i++) {
      if (gameBoard[i][0] == mark && gameBoard[i][1] == mark && gameBoard[i][2] == mark)
        return true;
    }

    // Columns
    for (int i = 0; i < 3; i++) {
      if (gameBoard[0][i] == mark && gameBoard[1][i] == mark && gameBoard[2][i] == mark)
        return true;
    }

    // Diagonals
    if (gameBoard[0][0] == mark && gameBoard[1][1] == mark && gameBoard[2][2] == mark)
      return true;

    if (gameBoard[0][2] == mark && gameBoard[1][1] == mark && gameBoard[2][0] == mark)
      return true;

    return false;
  }
}