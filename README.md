# Experimental Web Sockets stuff #

Just felt like understanding web sockets. Made some demo stuff.

Use client.html and the testserver.py from the same domain (requirements.txt has dependencies pip:able).

You will need to edit the source to configure the right IP for you server (testserver.py and client.html).

Several clients show the effect more accurately. Coordinate updates are broadcasted to all clients every tenth of a second and updates positions. Pretty fun.

Python stuff leans on Autobahn which leans on Twisted which is awesome.

