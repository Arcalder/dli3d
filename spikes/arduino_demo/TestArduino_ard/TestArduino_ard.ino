/*
  Character echo
 */

void setup() {
  // Open serial communications:
  Serial.begin(9600);

  // send an intro:
  Serial.println("Esperando instruccion");
  Serial.println();
}

void loop() {
  // get any incoming bytes:
  if (Serial.available() > 0) {
    int thisChar = Serial.read();

    // say what was sent:
    Serial.print("Me enviaste la instruccion: \'");
    Serial.write(thisChar);

    // add some space and ask for another byte:
    Serial.println();
    Serial.println("Esperando otra instruccion:");
    Serial.println();
  }
}






