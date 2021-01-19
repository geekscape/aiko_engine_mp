Usage:
a) push the left or right Oleds to invert the color
b) try the left or right touch slider to stop the frames, rewind,
   or move forward slowly

How the animations were made:
- this started with a suitable animated gif I had to find (took over 1h)
- then resizing it to 256 wide
- crop top bottom, but it was still too high
- scaled it down to 256x64 (the eyes were a bit taller)
- split it in 2 gifs of 128x64
- split out frames: convert -coalesce ../blinking_eyes2_128x64L.gif L%d.gif
- convert to pbm: for i in *.gif; do convert $i $i.pbm; done
- then manually inspect the frames to find which ones changed, and only
  import those at the right index (the gif had 53 frames)
- repeat for the other eye
- ...
- profit!

Ok, the 2 eyes aren't exactly synchronized because I can't update
both oleds at the same time, but hopefully that's close enough :)
