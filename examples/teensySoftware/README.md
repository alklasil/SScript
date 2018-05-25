### Teensy software
 * named such because the software is mainly aimed for teensy boards (though the software should work equally well on any arduino board supporting esp8266, mpu9250, sdfat, and sscript libraries)
 * If the board does not support one or more of the mentioned libraries, the software can still be used as long as the board supports at least esp8266 library (for configuration and webserver) and the function pointer array and library includes are modified accordingly (remove the functions and #include direcrives that are not supported or otherwise to be included)

#### Two components: webserver & sscript:
 * webserver: receive get and post requests
   * **GET** -> provide a html-page to the requester. The html-page contains two components.
     * configure: a field to which sscript scripts can be pasted and submitted to the device to configure the device.
     * data: a field which contains information provided by the device. for example: step count. 
   * **POST** -> receive post requests to configure the device (to configure sscript).
 * sscript:
   * run the scripts (provided via post requests).
     * Examples:
       * logger: log sensor data, such as acceleration and temperature.
       * thresholdcounter: increace count based on thresholding and simple filtering/data-manipulation. thresholdcounter also implements sd-card logging, serial port logging, and webserver logging.

#### main loop

* webserver: check if there are requestes:
  * if requests received: if Get-requests, provide a html-page. if POST-requests, configure sscript.
  * if no requests received: do nothing
* sscript: check if enough time elapsed since last execution (usually check, though fps can be set to inf, and in that case the checking part of the script does not get included in the code in the compiling)
  * if enough time elapsed: execute curret sscript state:
    * such as: measure data, process data, log data.
  * if not enough time elapsed: either do nothing, or modify data in some way (depends on the sscript script executed)

#### outside of the main loop

* setup:
  * webserver: initialize and connect to hotspot (if available)
  * sensors & sd-card: intialize (if available)
  * sscript: provide function pointer array.

* other:
  * webserver:
    * webserver provides a handle (stringGenerator) which a sscript script can subscribe itself to (1 sscript instance at a time for now, until better multi-instancing of sscript instances is implemented (maybe i should get to doing that next, only way to implement multi-instance subscibing at the moment is via gustom proxys, or [experiemental] variable/function/state sharing))
      * if script subscribes to the handle -> when webserver receives a get-request: webserver asks the script whether it has got some html-data to provide and then inserts it into a field in the html-page (below the configuration field)
      * if no script has subscribed to the handle -> when webserver receives a get-request: webserver does not ask for data from the script, and does not insert any data provided by the script into the html-page.
    
    
