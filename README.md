# number2music

## What this program does

This program simply takes one argument, an input list of numbers, and converts
it to `output.wav` using the algorithm described below. Often, the music will
sound horrible; the algorithm is not very well developed.

## Algorithms

There is currently only one type of algorithm. Over time, more algorithms may
be added, to make the music sound better. The older algorithms will be able to
be accessed via `git`.

### A

The initial algorithm, 'A', uses the following steps to generate the music.

#### Step 1: Split into blocks of 3

The first step is the program reads the file and splits it into blocks of 3. Any
trailing numbers that do not fit into the last block of 3 are discarded. The
first number is used for the direction, the second for the change, and the third
for the duration.

#### Step 2: Get the direction

All the notes are relative to each other, so the music is not jumping around
wildly. The logic process is:

If the number is 0 or 1, we use the same note as the previous note.

If the number is 2, 3, 4, or 5, we will move upwards.

If the number is 6, 7, 8, or 9, we will move downwards.

#### Step 3: Get the change

The change of notes is now determined.

If there is no change, this step is skipped and the change is set to 0.

If the direction is upwards, we set the change to the "change number".

If the direction is downwards, we set the change to the negative of the "change
number", as we are moving in a direction negative to the previous note.

#### Step 4: Ensure that the note isn't too high or low

In some circumstances, the notes can get very high or very low, and our
rendering program dosen't work. This step ensures that notes above B7 or below
C0 are not used. If the note is above B7 or below C0, then the change and
direction are reversed.

#### Step 5: Get the note

This is determined by the previous note minus the change.

#### Step 6: Get the duration

There is no relativetly here.

If the number is 0, then a semibreve is used.

If the number is 1 or 2, then a minim is used.

If the number is 3, 4 or 5, a crotchet is used.

If the number is 6 or 7, a quaver is used.

If the number is 8 or 9, a semiquaver is used.
