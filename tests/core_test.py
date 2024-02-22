import pytest
import numpy as np
from pytunesmith import Song, InstrumentTrack, LyricsTrack
from pytunesmith.effects import ConvolutionEffect, GainEffect
from pytunesmith.effects import EffectsPack

SF_PATH = 'tests/TimGM6mb.sf2'

def test_convolution_effect_creation():
    effect = ConvolutionEffect(impulse_response=[1, 0, 0.5])
    assert isinstance(effect, ConvolutionEffect)

def test_gain_effect_creation():
    effect = GainEffect(gain=2)
    assert effect.gain == 2

def test_echo_effect_creation():
    effect = EffectsPack.Echo(delay=0.5, decay=0.6, fs=44100)
    assert isinstance(effect, EffectsPack.Echo)

def test_instrument_track_creation():
    melody = [('C4', 0, 1), ('E4', 1, 2)]
    track = InstrumentTrack('Piano', melody)
    assert track.name == 'Piano'
    assert track.melody == melody
    assert track.effects == []

def test_lyrics_track_creation():
    lyrics = [('Hello', 0.5, 1.0), ('world', 1.5, 1.0)]
    track = LyricsTrack(lyrics)
    assert track.lyrics == lyrics
    assert track.effects == []

def test_song_creation():
    song = Song(tempo=120, sf2_path=SF_PATH)
    assert song.tempo == 120
    assert song.sf2_path == SF_PATH
    assert song.instrument_tracks == []
    assert song.lyrics_tracks == []

def test_song_export(tmp_path):
    song = Song(tempo=120, sf2_path=SF_PATH)
    melody = [('C4', 0, 1), ('E4', 1, 2)]
    track = InstrumentTrack('Acoustic Grand Piano', melody)
    song.add_instrument_track(track)
    lyrics = [('Hello', 0.5, 1.0), ('world', 1.5, 1.0)]
    lyrics_track = LyricsTrack(lyrics)
    song.add_lyrics_track(lyrics_track)
    output_file = tmp_path / "test_song.wav"
    song.export(str(output_file), fs=44100)
    assert output_file.exists()
