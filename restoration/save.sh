#!/bin/bash
for i in {2..93}
do
   curl http://utdcs.herokuapp.com/post/$i/ >$i.html
done
