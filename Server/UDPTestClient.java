import java.io.IOException;
import java.net.*;
import java.util.Scanner;

public class UDPTestClient {
  private static final int SERVER_PORT = 3116;
  private static final int BUFFER_SIZE = 1024;

  public static void main(String[] args) throws Exception {
    try {
      DatagramSocket socket = new DatagramSocket();
      System.out.println("Client started.");
      // Messages to send
      String[] messages = {
              "HELO 1 elb",
              "CREA elb"
      };

      // Send messages sequentially
      for (String message : messages) {
        byte[] sendData = message.getBytes();

        // Create a DatagramPacket for sending
        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, InetAddress.getLocalHost(), SERVER_PORT);

        // Send the packet
        socket.send(sendPacket);

        System.out.println(message);

        // Create a buffer for receiving the server's response
        byte[] receiveData = new byte[1024];
        DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);

        // Receive the response from the server
        socket.receive(receivePacket);

        // Process the response
        String response = new String(receivePacket.getData(), 0, receivePacket.getLength());
        System.out.println("Received: " + response);

        // Wait for a short duration before sending the next message
        Thread.sleep(1000); // 1 second
      }

      // Create a separate thread for receiving packets
      Thread receiverThread = new Thread(() -> {
        System.out.println("Thread started.");
        try {
          byte[] buffer = new byte[BUFFER_SIZE];
          DatagramPacket receivePacket = new DatagramPacket(buffer, BUFFER_SIZE);

          while (true) {
            socket.receive(receivePacket); // Wait for incoming packet

            // Process the received packet
            String message = new String(receivePacket.getData(), 0, receivePacket.getLength());
            System.out.println("Received packet: " + message);
          }
        } catch (IOException e) {
          System.out.println("IOException in receiver thread: " + e.getMessage());
        }
      });
      receiverThread.start();

      // Read input from console and send packets
      Scanner scanner = new Scanner(System.in);
      String input;

      while (true) {
        System.out.print("Enter message to send (or 'exit' to quit): ");
        input = scanner.nextLine();

        if (input.equalsIgnoreCase("exit")) {
          break; // Exit the loop and terminate the program
        }

        byte[] sendData = input.getBytes();
        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, InetAddress.getLocalHost(), SERVER_PORT);
        socket.send(sendPacket);
        System.out.println("Sent packet: " + input);
      }

        // Close the socket and join the receiver thread
//      socket.close();
        receiverThread.join();
        System.out.println("Client terminated.");
      } catch(SocketException e){
        System.out.println("SocketException: " + e.getMessage());
      } catch(IOException e){
        System.out.println("IOException: " + e.getMessage());
      } catch(InterruptedException e){
        System.out.println("InterruptedException: " + e.getMessage());
  }
}

  private static void send(DatagramSocket socket, String str) throws Exception {
    byte[] sendData = str.getBytes();
    DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, InetAddress.getLocalHost(), SERVER_PORT);
    socket.send(sendPacket);
  }
}
