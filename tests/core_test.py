import pytest
import numpy as np
from pytunesmith import Effect, InstrumentTrack, LyricsTrack, Song

SF_PATH = 'TimGM6mb.sf2'

def test_effect_creation():
    effect = Effect('gain', {'gain': 2})
    assert effect.name == 'gain'
    assert effect.parameters['gain'] == 2

def test_effect_application():
    effect = Effect('gain', {'gain': 2})
    audio = np.array([1, 2, 3], dtype=np.float32)
    processed_audio = effect.apply(audio, 44100)
    assert np.array_equal(processed_audio, audio * 2)

def test_instrument_track_creation():
    melody = [('C4', 0, 1), ('E4', 1, 2)]
    track = InstrumentTrack('Piano', melody)
    assert track.name == 'Piano'
    assert track.melody == melody
    assert track.effects == []

def test_lyrics_track_creation():
    lyrics = [('Hello', 0.5), ('world', 1.5)]
    track = LyricsTrack(lyrics)
    assert track.lyrics == lyrics
    assert track.effects == []

def test_song_creation():
    song = Song(tempo=120, sf2_path=SF_PATH)
    assert song.tempo == 120
    assert song.sf2_path == SF_PATH
    assert song.instrument_tracks == []
    assert song.lyrics_track is None

def test_song_export(tmp_path):
    # This is a basic test to check if the export method runs without errors.
    # More comprehensive tests would require audio file analysis.
    song = Song(tempo=120, sf2_path=SF_PATH)
    melody = [('C4', 0, 1), ('E4', 1, 2)]
    track = InstrumentTrack('Acoustic Grand Piano', melody)
    song.add_instrument_track(track)
    lyrics = [('Hello', 0.5, 1.0), ('world', 1.5, 1.0)]  # Add speed value
    lyrics_track = LyricsTrack(lyrics)
    song.set_lyrics_track(lyrics_track)
    output_file = tmp_path / "test_song.wav"
    song.export(str(output_file), fs=44100)
    assert output_file.exists()
