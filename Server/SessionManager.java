import java.io.PrintWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.Socket;
import java.util.*;

public class SessionManager {
  class User {
    String _uuid;
    boolean _isUDP;

//    static String _address;
//    static int _port;
    String _url;
    Socket _tcpSocket;
    DatagramSocket _udpSocket;

    public User(DatagramSocket udpSocket, String uuid, String address) {  // UDP
      _uuid = uuid;
      _url = address;
      _udpSocket = udpSocket;
      _isUDP = true;
    }

    public User(Socket tcpSocket, String uuid, String address) {  // TCP
      _uuid = uuid;
      _tcpSocket = tcpSocket;
      _url = address;
      _isUDP = false;
    }

    public String getURL() { return _url; }
    public String getUUID() { return _uuid; }

    public void send(String payload) throws Exception {
      payload = payload + "\r\n";
      if (_isUDP) {
        String url = _url.split("://")[1];
        String address = url.split(":")[0];
        int port = Integer.parseInt(url.split(":")[1]);
        DatagramPacket outPacket = new DatagramPacket(payload.getBytes(), payload.getBytes().length, InetAddress.getByName(address), port);
        _udpSocket.send(outPacket);
      } else {
        PrintWriter out = new PrintWriter(_tcpSocket.getOutputStream(), true);
        out.println(payload);
      }
    }
  }

  private Map<String, User> sessions = new HashMap<>();

  public void endSession(String playerName) { sessions.remove(playerName); }

  public boolean isUserInSession(String uuid) {
    for (Map.Entry<String, User> entry : sessions.entrySet()) {
      User u = entry.getValue();

      if (u.getUUID().equals(uuid)) return true;
    }
    return false;
  }

  public void addSession(DatagramSocket socket, String playerName, String uuid, String address, int port) {  // UDP
    sessions.put(playerName, new User(socket, uuid, "t3udp://" + address + ":" + port));
  }

  public void addSession(Socket socket, String playerName, String uuid, String address, int port) {  // TCP
    sessions.put(playerName, new User(socket, uuid, "t3tcp://" + address + ":" + port));
  }

  public User getSession(String playerName) {
    return sessions.get(playerName);
  }

  public String findPlayerNameFromIP(String sender) {
    String playerName = "";

    for (Map.Entry<String, User> entry: sessions.entrySet()) {
      if (Objects.equals(sender, entry.getValue().getURL())) {
        playerName = entry.getKey();
      }
    }

    return playerName;
  }
}
