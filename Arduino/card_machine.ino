#include <SPI.h>
#include <MFRC522.h>

const int RST_PIN = 9;
const int SS_PIN = 10;
MFRC522 rc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);

  SPI.begin();
  rc522.PCD_Init();
}

void loop() {
  int recv_size = 0;
  char recv_buffer[16];

  if (Serial.available() > 0)
  {
    recv_size = Serial.readBytesUntil("\n", recv_buffer, 16);
  }

  bool newCard = rc522.PICC_IsNewCardPresent();
  bool readCard = rc522.PICC_ReadCardSerial();

  if (recv_size > 0)
  {
    // Get command
    char cmd[2];
    memset(cmd, 0x00, sizeof(cmd));
    memcpy(cmd, recv_buffer, 2);

    char send_buffer[16];
    memset(send_buffer, 0x00, sizeof(send_buffer));
    memcpy(send_buffer, cmd, 2);

    // status default값은 'ERROR'
    MFRC522::StatusCode status = MFRC522::STATUS_ERROR;
    if (newCard = true && readCard == true)
    {
      if (strncmp(cmd, "GS", 2) == 0)
      {
        memset(send_buffer + 2, MFRC522::STATUS_OK, 1);
        memcpy(send_buffer + 3, rc522.uid.uidByte, 4);
        Serial.write(send_buffer, 7);
      }
      else
      {
        memset(send_buffer + 2, 0xFE, 1);
        Serial.write(send_buffer, 3);
      }
    }
    else
    {
      memset(send_buffer + 2, 0xFA, 1);
      Serial.write(send_buffer, 3);
    }

    // Send '\n'
    Serial.println();
  }
}
