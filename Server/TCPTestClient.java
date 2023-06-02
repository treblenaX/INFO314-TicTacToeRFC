import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class TCPTestClient {
  private static final String SERVER_IP = "localhost"; // Replace with the server IP address
  private static final int SERVER_PORT = 3116; // Replace with the server port

  public static void main(String[] args) {
    try {
      // Connect to the server
      Socket socket = new Socket(SERVER_IP, SERVER_PORT);

      // Create input and output streams for the socket
      PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
      BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

      // Create a reader for user input
      BufferedReader userInputReader = new BufferedReader(new InputStreamReader(System.in));

      Thread serverOutputThread = new Thread(() -> {
        try {
          String serverResponse;
          while ((serverResponse = in.readLine()) != null) {
            System.out.println("Server response: " + serverResponse);
          }
        } catch (IOException e) {
          e.printStackTrace();
        }
      });
      serverOutputThread.start();

      // Read user input and send it to the server
      String userInput;
      while ((userInput = userInputReader.readLine()) != null) {
        out.println(userInput); // Send the user input to the server
      }

      // Close the socket and streams
      socket.close();
      out.close();
      in.close();
      userInputReader.close();
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
