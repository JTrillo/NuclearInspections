To carry out the tests you have to use the Python files existing on **code** folder. Basically you only will have to modify the Python file **testing.py**. This file has almost 600 lines of code but only a few are modifiable. These ones are:

* Lines 17 & 18. Variables ***API_ENDPOINT*** and ***API_ENDPOINT_2*** must reference the URLs of the deployed Composer REST Servers.
* From line 522 to 534 the main code of the file is located. There is a comment per function in the Python file explaining the use of each parameter. The next tables shows which card is necessary to execute each function:

| Line 	| Function                 	| Card          	|
|------	|--------------------------	|---------------	|
| 522  	| cleanMultithreading      	| admin         	|
| 523  	| addTubes                 	| mdr           	|
| 524  	| cleanCalibrations        	| admin         	|
| 525  	| addWorkAndCalibrations   	| admin         	|
| 526  	| addAcquisitionTest       	| alba          	|
| 527  	| addAutomaticAnalysisTest 	| auto          	|
| 528  	| getCalibrations          	| esc           	|
| 529  	| getCalibrations          	| llopis        	|
| 530  	| addAnalysisTest          	| esc<br>llopis 	|
| 531  	| endCalibrations          	| esc           	|
| 532  	| endCalibrations          	| llopis        	|
| 533  	| getCalibrations          	| trillo        	|
| 534  	| addResolutionTest        	| trillo        	|

* Line 530. Function ***addAnalysisTest*** need 2 Composer REST Servers running at same time: first one running on port 3000 using **esc** card, the second one running on port 3001 using **llopis** card.