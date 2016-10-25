#!/bin/sh

if [ $# -ne 1 ]; then
  echo "Usage: $(basename $0) <list-uri>" 1>&2
  exit 1
fi

file=/tmp/tmp.tmp
list=$1


# Sanity check
youtube-dl --flat-playlist -j "$list" > $file
if ! grep -q '"_type": "url",' $file; then
  echo "Error: not a playlist" 1>&2
  exit 1
fi

cont=()
for v in $(sed -e 's/^.*Youtube", "id": "//g' -e 's/", "title.*$//g' < $file); do
  echo "https://www.youtube.com/watch?v=$v"
done

for c in $cont; do
  oc exec -it $c test -f /ready
  if [ $? -eq 0 ]; then
    name=$(oc exec -it $c 'ls -1 /*mp3')
    oc exec -it $c cat /$name > $name
  fi
  sleep 10
done

# write-html.py

f = open('music.html','w')

message = """<html>
<head></head>
<body><p>Your Music Play List!</p>
<audio controls>
  <source src="horse.ogg" type="audio/ogg">
  <source src="horse.mp3" type="audio/mpeg">
Your browser does not support the audio element.
</audio>
</body>
</html>"""

f.write(message)
f.close()
