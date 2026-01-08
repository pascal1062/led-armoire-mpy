import usocket as socket
import uselect as select
import time

class UDPHandler:
    def __init__(self, ip="0.0.0.0", port=12345):
        self.addr = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.addr)
        self.sock.setblocking(False)
        
        # Initialisation du poller
        self.poller = select.poll()
        self.poller.register(self.sock, select.POLLIN)
        print("Serveur UDP initialisé sur {}:{}".format(ip, port))

    def check_messages(self, timeout_ms=100):
        """Vérifie si des messages sont arrivés sans bloquer le programme."""
        events = self.poller.poll(timeout_ms)
        for sock, event in events:
            if event & select.POLLIN:
                try:
                    data, addr = self.sock.recvfrom(1024)
                    return data, addr
                except Exception as e:
                    print("Erreur de réception:", e)
        return None, None

    def send(self, message, target_addr):
        """Envoie un message à une adresse spécifique."""
        try:
            if isinstance(message, str):
                message = message.encode()
            self.sock.sendto(message, target_addr)
        except Exception as e:
            print("Erreur d'envoi:", e)

    def stop(self):
        """Ferme proprement le socket."""
        print("Fermeture du socket...")
        self.poller.unregister(self.sock)
        self.sock.close()

# --- Exemple d'utilisation ---

network = UDPHandler(port=12345)

try:
    print("Boucle principale lancée (Ctrl+C pour arrêter)")
    while True:
        # 1. Vérification des messages entrants
        msg, sender = network.check_messages(timeout_ms=50)
        
        if msg:
            print("Reçu de {}: {}".format(sender, msg.decode()))
            # Réponse automatique
            network.send("Message bien reçu", sender)
        
        # 2. Emplacement pour d'autres tâches (ex: lire un capteur)
        # print("Le microcontrôleur fait autre chose...")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nArrêt interrompu.")

finally:
    # 3. Libération cruciale des ressources
    network.stop()
