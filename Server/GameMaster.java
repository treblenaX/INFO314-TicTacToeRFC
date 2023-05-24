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

	private String generateCode() {
		StringBuilder code = new StringBuilder();
		for (int i = 0; i < CODE_LENGTH; i++) {
			code.append(ALPHABET.charAt((int) (Math.random() * ALPHABET.length())));
		}
		return code.toString();
	}
}
