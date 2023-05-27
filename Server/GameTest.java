public class GameTest {
  public static void main(String[] args) throws Exception {
    GameMaster gm = new GameMaster();

    String gameCode = gm.createGame();
    gm.joinGame(gameCode, "elbert");
    // should not have a board
    System.out.println(gm.getGameStatus(gameCode));

    gm.joinGame(gameCode, "treble");
    // should have a board
    System.out.println(gm.getGameStatus(gameCode));

    gm.moveInGame(gameCode, 1);
    System.out.println(gm.getGameStatus(gameCode));

    gm.moveInGame(gameCode, 3);
    System.out.println(gm.getGameStatus(gameCode));

    gm.moveInGame(gameCode, 2);
    System.out.println(gm.getGameStatus(gameCode));

    gm.moveInGame(gameCode, 6);
    System.out.println(gm.getGameStatus(gameCode));

    gm.moveInGame(gameCode, 9);
    System.out.println(gm.getGameStatus(gameCode));

    gm.moveInGame(gameCode, 4);
    System.out.println(gm.getGameStatus(gameCode));
    gm.moveInGame(gameCode, 8);
    System.out.println(gm.getGameStatus(gameCode));
    gm.moveInGame(gameCode, 7);
    System.out.println(gm.getGameStatus(gameCode));
    gm.moveInGame(gameCode, 5);
    System.out.println(gm.getGameStatus(gameCode));
  }
}
