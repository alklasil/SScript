#include "SEsp8266.h"

// external sources:
//  * https://forum.pjrc.com/threads/27850-A-Guide-To-Using-ESP8266-With-TEENSY-3

int bufferIndex;
char *buffer;
String header;
String content;
String requestString;
SScript *requestStringGeneratorSscript;
int32_t requestStringGeneratorStateNum;

void webserver_setup() {
    buffer = new char[BUFFER_SIZE];
    requestString = "";
    requestStringGeneratorSscript = NULL;
    requestStringGeneratorStateNum = 0;

    webserver_setupWiFi();
}

// By default we are looking for OK\r\n
byte webserver_wait_for_esp_response(int timeout, char* term) {
    unsigned long t = millis();
	bool found = false;
	int len = strlen(term);

	// wait for at most timeout milliseconds
	// or if OK\r\n is found
	while (millis()<t + timeout) {
		if (Serial1.available()) {
			buffer[bufferIndex++] = Serial1.read();
			if (bufferIndex >= len) {
				if (strncmp(buffer + bufferIndex - len, term, len) == 0) {
					found = true;
					break;
				}
			}
		}
	}
    if (!found) buffer[bufferIndex] = 0;
        return found;
}

bool webserver_read_till_eol(int timeout) {
	static int i = 0;
    if (Serial1.available()) {
        unsigned long t = millis();
        while (millis() < t + timeout) {
            if (Serial1.available()) {
                char c = Serial1.read();
                buffer[i] = c; i = i + 1;
                if (i == BUFFER_SIZE)  i = 0;
                if (i > 1 && buffer[i - 2] == 13 && buffer[i - 1] == 10) {
                    buffer[i] = 0;
                    i = 0;
                    return true;
                }
                t = millis();
            }
        }
    }
	return false;
}

void webserver_serve_page(int ch_id) {
    webserver_htmlRootPage(generateAndGetRequestString());
	Serial1.print("AT+CIPSEND=");
	Serial1.print(ch_id);
	Serial1.print(",");
	Serial1.println(header.length() + content.length());
	if (webserver_wait_for_esp_response(2000)) {
    while (!Serial1.available()) {} // wait a bit to make sure, Serial1 is available (otherwise -> BOOOM!, experiemental result)
                                    // There are other ways to handle the problem, but this seems to be the fastest, though
                                    // will have to see if it causes any problems, so far at least it seems no.
		Serial1.print(header);
		Serial1.print(content);
	}
	else {
		Serial1.print("AT+CIPCLOSE=");
		Serial1.println(ch_id); Serial.println("10");
	}
}

void webserver_loop() {
    int ch_id, packet_len;
    char *pb;

    if (webserver_read_till_eol(100)) {
        Serial.print("buffer: ");
        Serial.println(buffer);
        Serial.print(strlen(buffer));
        if (buffer[0] == '\0') {
            buffer[0] = ' ';
            buffer[1] = '\0';
        } else if (strncmp(buffer, "+IPD,", 5) == 0) {
            sscanf(buffer + 5, "%d,%d", &ch_id, &packet_len);
            if (packet_len > 0) {
                // Serial.println("packet len > 0");
                // read serial until packet_len character received
                // start from :
                pb = buffer + 5;
                pb = strchr(pb, ':');
                if (pb == NULL) {
                    return;
                } pb++;
                if (strncmp(pb, "GET /", 5) == 0) {
                    delay(500);
                    Serial.print("(GET /) packet: "); Serial.println(pb);
                    Serial.print("responsed");
                    Serial.print(ch_id);
                    webserver_serve_page(ch_id);
                }
                else if (strncmp(pb, "POST /", 5) == 0) {
                    Serial.print("(POST /) packet: "); Serial.println(pb);
                }
                else if (strncmp(pb, "conf=", 5) == 0) {
                    Serial.print("(conf=)packet:"); Serial.println(pb);

                    Serial.println("configuring..");
                    sScript->set(pb + 5);

                    Serial.println("configured..");

                    // wait for a bit. This seems to be necessary, especially if fps is not set. Otherwise the device may stop working.
                    delay(1000);
                }
            }
        } else {
            pb = buffer;
            if (strncmp(pb, "conf=", 5) == 0) {
                Serial.print("(conf=)packet:"); Serial.println(pb);

                Serial.println("configuring..");
                sScript->set(pb + 5);

                Serial.println("configured..");

                // wait for a bit. This seems to be necessary, especially if fps is not set. Otherwise the device may stop working.
                delay(1000);
            }
        }
        Serial.println("packet:end ");
    }
}

void webserver_setupWiFi() {
    // turn on echo
    Serial1.println("ATE1");
    webserver_wait_for_esp_response(1000);

    // set mode 1 (client)
    Serial1.println("AT+CWMODE=1");
    webserver_wait_for_esp_response(1000);

    // reset WiFi module (after setting mode, this is required)
    Serial1.print("AT+RST\r\n");
    webserver_wait_for_esp_response(1500);

    //join AP (ssid=SSID, password=PASS)
    Serial1.print("AT+CWJAP=\"");
    Serial1.print(SSID);
    Serial1.print("\",\"");
    Serial1.print(PASS);
    Serial1.println("\"");
    webserver_wait_for_esp_response(5000);

    // start server
    Serial1.println("AT+CIPMUX=1");
    webserver_wait_for_esp_response(1000);

    //Create TCP Server
    Serial1.print("AT+CIPSERVER=1,"); // turn on TCP service
    Serial1.println(PORT);
    webserver_wait_for_esp_response(1000);

    // set timeout)
    Serial1.println("AT+CIPSTO=5");
    webserver_wait_for_esp_response(1000);

    // ip
    Serial.println("AT+CIFSR");
    Serial1.println("AT+CIFSR");
    webserver_wait_for_esp_response(1000);
}

void webserver_htmlRootPage(String *requestString)
{
    // content (page)
    content = "<!DOCTYPE html>";
    content += "<form method='post' enctype='text/plain' action=''>";
    content += "Configuration: <input type='text' name='conf'><br>";
    content += "<input type='submit' value='Submit'>";
    content += "</form>";
    content += *requestString;

    // header
    header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\nRefresh: 300\r\n";
    header += "Content-Length:";
    header += (int)(content.length());
    header += "\r\n\r\n";
}

String *generateAndGetRequestString(){

   if (requestStringGeneratorSscript == NULL)
      return &requestString;
   SScript *_sScript = sScript;
   sScript = requestStringGeneratorSscript;

   //
   // requestStringGeneratorSscript, requestStringGeneratorState
   //   should set requestString
   (*sScript).executeState(requestStringGeneratorStateNum);

   sScript = _sScript;
   return &requestString;

}

void esp_setRequestString() {
    FUNCTION_LEFT_NOPARSE
    requestString = sScript->strings[*leftValue];
    FUNCTION_END
}

void esp_setRequestStringGenerator() {
   FUNCTION_LEFT_NOPARSE;
   requestStringGeneratorSscript = sScript;
   requestStringGeneratorStateNum = *leftValue;
   FUNCTION_END
}

void esp_setRequestStringHTMLWithTime() {
   // esp_setRequestStringHTML(#requestString, #timeOffset)
   int32_t *str = FUNCTION_ONE_NOPARSE;
   int32_t *timeOffset_millis = FUNCTION_ONE_NOPARSE;

   requestString = "";
   requestString += "<script>";
   requestString += "function f(o) {";
   requestString += "    document.getElementById('s').innerHTML = new Date(new Date().getTime() - o) + ': " + sScript->strings[*str] + ";'";
   requestString += "}";
   requestString += "</script>";
   requestString += "<body onload='f(" + sScript->strings[*timeOffset_millis] + ")'>";
   requestString += "<p id='s'>df</p>";

   FUNCTION_END
}
