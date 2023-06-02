import java.io.OutputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.Socket;

public class SenderService {
  boolean isUDP;
  DatagramSocket udp_socket;
  Socket tcp_socket;

  public SenderService(DatagramSocket udp_socket) {
    this.udp_socket = udp_socket;
    this.isUDP = true;
  }

  public SenderService(Socket tcp_socket) {
    this.tcp_socket = tcp_socket;
    this.isUDP = false;
  }

  public void respond(String payload, String... destinations) throws Exception {
    for (String dest : destinations) {
      String address = dest.split(":")[0];
      int port = Integer.parseInt(dest.split(":")[1]);

      if (udp_socket != null) { // respond with UDP
        DatagramPacket outPacket = new DatagramPacket(payload.getBytes(), payload.getBytes().length, InetAddress.getByName(address), port);
        udp_socket.send(outPacket);
      } else {  // respond with TCP
        OutputStream os = tcp_socket.getOutputStream();
        os.write(payload.getBytes());
        os.flush();
      }
    }
  }
}
