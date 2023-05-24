import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class UDPTestClient2 {
  public static void main(String[] args) {
    try {
      // Create a UDP socket
      DatagramSocket socket = new DatagramSocket();
      sendMessage(socket, "HELO 1 treble");
      socket.close();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private static void sendMessage(DatagramSocket socket, String message) throws Exception {
    // Specify the server's IP address and port
    InetAddress serverAddress = InetAddress.getByName("localhost");
    int serverPort = 3116;

    // Create a message to send to the server
    byte[] sendData = message.getBytes();

    // Create a datagram packet with the message, server address, and port
    DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, serverAddress, serverPort);

    // Send the packet to the server
    socket.send(sendPacket);

    // Create a byte array to receive the response from the server
    byte[] receiveData = new byte[1024];

    // Create a datagram packet to store the received data
    DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);

    // Receive the packet from the server
    socket.receive(receivePacket);

    // Extract the data from the packet
    String serverResponse = new String(receivePacket.getData(), 0, receivePacket.getLength());

    // Print the server's response
    System.out.println("Server response: " + serverResponse);
  }
}
