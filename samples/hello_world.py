import pytunesmith

# Define the song structure
song = pytunesmith.Song(tempo=120, sf2_path='TimGM6mb.sf2')

# Define an echo effect with a longer impulse response
echo_impulse_response = [1] + [0] * 2000 + [0.6] + [0] * 2000 + [0.3]
echo_effect = pytunesmith.Effect('convolution', {'impulse_response': echo_impulse_response})

# Add a piano track with a melody and the echo effect
piano_track = pytunesmith.InstrumentTrack(
    name="Acoustic Grand Piano",
    melody=[
        ('C4', 0, 1), ('E4', 1, 2), ('G4', 2, 3), ('C5', 3, 5),
        ('E5', 5, 6), ('G5', 6, 7), ('C6', 7, 8), ('E6', 8, 10)
    ],
    effects=[echo_effect]
)
song.add_instrument_track(piano_track)

# Add a violin track with a different melody
violin_track = pytunesmith.InstrumentTrack(
    name="Violin",
    melody=[
        ('G4', 0, 2), ('E5', 2, 4),
        ('C5', 4, 6), ('G5', 6, 8)
    ]
)
song.add_instrument_track(violin_track)

# Add lyrics with varying speeds and the echo effect
lyrics_track = pytunesmith.LyricsTrack(
    lyrics=[
        ("Hello", 1.5, 0.6),
        ("world", 3, 0.4),
        ("this", 4.5, 0.7),
        ("is", 5, 0.5),
        ("music", 6, 0.3)
    ],
    effects=[echo_effect]
)
song.set_lyrics_track(lyrics_track)

# Export the song to a WAV file
song.export("hello_world_song.wav")
