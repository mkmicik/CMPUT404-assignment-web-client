CMPUT404-assignment-web-client
==============================

CMPUT404-assignment-web-client

See requirements.org (plain-text) for a description of the project.

Make a simple web-client like curl or wget

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html

=============================
| 		 Alterations 		|
=============================
Author: 		Mike Kmicik
Date Modified: 	Jan. 31, 2016

Summary
==========
When the client receives a URL and http type, it builds the appropriate request string and connects to the server. It then receives all content returned from the server and returns it to the caller in the form of an HTTPResponse object. It will parse out the response's code and body when building the response object. It complies with all of the assignment specs and should perform as expected. See the code comments in httpclient.py for more detailed comments.

Know Issues
==========
There are no known issues with my implementation, all features should function as expected.

Collaboration
=============
I did not collaborate with any other students for this assignment.