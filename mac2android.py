from bleak import BleakScanner, BleakClient
import asyncio
import logging
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class BluetoothDevice:
    name: str
    address: str
    rssi: int

class MacAndroidBridge:
    def __init__(self, log_enabled: bool = True):
        self.logger = self._setup_logger() if log_enabled else None
        self.client: Optional[BleakClient] = None
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("MacAndroidBridge")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _log(self, message: str, level: str = "info"):
        if self.logger:
            getattr(self.logger, level)(message)

    async def scan_devices(self) -> List[BluetoothDevice]:
        try:
            self._log("Recherche des appareils Bluetooth...")
            devices = await BleakScanner.discover()
            return [
                BluetoothDevice(
                    name=d.name or "Unknown",
                    address=d.address,
                    rssi=d.rssi
                ) for d in devices if d.name
            ]
        except Exception as e:
            self._log(f"Erreur lors du scan: {str(e)}", "error")
            return []

    async def connect(self, device_address: str) -> bool:
        try:
            self.client = BleakClient(device_address)
            await self.client.connect()
            self._log(f"Connecté à l'appareil {device_address}")
            return True
        except Exception as e:
            self._log(f"Erreur de connexion: {str(e)}", "error")
            return False

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            self._log("Déconnexion effectuée")
            self.client = None

    async def send_data(self, characteristic_uuid: str, data: bytes) -> bool:
        if not self.client or not self.client.is_connected:
            self._log("Aucune connexion active", "error")
            return False
        
        try:
            await self.client.write_gatt_char(characteristic_uuid, data)
            self._log(f"Données envoyées: {data.hex()}")
            return True
        except Exception as e:
            self._log(f"Erreur d'envoi: {str(e)}", "error")
            return False

if __name__ == "__main__":
    async def main():
        bridge = MacAndroidBridge()
        
        # Scan des appareils
        devices = await bridge.scan_devices()
        if not devices:
            print("Aucun appareil trouvé")
            return
            
        # Affichage des appareils trouvés
        print("\nAppareils disponibles:")
        for i, device in enumerate(devices):
            print(f"{i+1}. {device.name} ({device.address}) - RSSI: {device.rssi}")
            
        # Connexion au premier appareil trouvé
        if devices:
            device = devices[0]
            if await bridge.connect(device.address):
                # Exemple d'envoi de données (UUID à adapter selon votre appareil)
                test_uuid = "0000180d-0000-1000-8000-00805f9b34fb"
                await bridge.send_data(test_uuid, b"Hello Android!")
                await bridge.disconnect()

    # Exécution de l'exemple
    asyncio.run(main())