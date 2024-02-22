import pretty_midi
import numpy as np
from scipy.io.wavfile import write as wav_write
from gtts import gTTS
from pydub import AudioSegment
import os

class Effect:
    """Base class for audio effects."""
    def apply(self, audio, fs):
        """Apply the effect to the audio."""
        raise NotImplementedError("This method should be implemented by subclasses.")

class InstrumentTrack:
    """A class representing a musical instrument track."""
    def __init__(self, name: str, melody: list, effects: list = None):
        self.name = name
        self.melody = melody
        self.effects = effects or []

    def synthesize(self, midi_data: pretty_midi.PrettyMIDI, fs: int, sf2_path: str) -> np.ndarray:
        """Synthesize the instrument track audio."""
        instrument = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program(self.name))
        for note, start, end in self.melody:
            midi_note = pretty_midi.Note(
                velocity=100,
                pitch=pretty_midi.note_name_to_number(note),
                start=start,
                end=end
            )
            instrument.notes.append(midi_note)
        midi_data.instruments.append(instrument)
        instrument_audio = midi_data.fluidsynth(fs=fs, sf2_path=sf2_path)
        for effect in self.effects:
            instrument_audio = effect.apply(instrument_audio, fs)
        return instrument_audio

class LyricsTrack:
    """A class representing a lyrics track."""
    def __init__(self, lyrics: list, effects: list = None):
        self.lyrics = lyrics
        self.effects = effects or []

    def synthesize(self, fs: int) -> np.ndarray:
        """Synthesize the lyrics track audio."""
        lyrics_audio = np.zeros(int(fs * max([t for _, t, _ in self.lyrics]) * 1.5))
        for text, start_time, speed in self.lyrics:
            tts = gTTS(text, lang='en')
            tts.save('temp_lyrics.mp3')
            word_audio = AudioSegment.from_mp3('temp_lyrics.mp3').get_array_of_samples()
            word_audio = np.array(word_audio, dtype=np.float32)
            word_audio /= np.max(np.abs(word_audio))

            word_audio = np.interp(
                np.arange(0, len(word_audio), speed),
                np.arange(0, len(word_audio)),
                word_audio
            )

            start_index = int(start_time * fs)
            end_index = start_index + len(word_audio)
            lyrics_audio[start_index:end_index] += word_audio

            os.remove('temp_lyrics.mp3')

        for effect in self.effects:
            lyrics_audio = effect.apply(lyrics_audio, fs)
        return lyrics_audio

class Song:
    """A class representing a song."""
    def __init__(self, tempo: int = 120, sf2_path: str = None):
        self.tempo = tempo
        self.instrument_tracks = []
        self.lyrics_tracks = []
        self.sf2_path = sf2_path

    def add_instrument_track(self, instrument_track: InstrumentTrack):
        """Add an instrument track to the song."""
        self.instrument_tracks.append(instrument_track)

    def add_lyrics_track(self, lyrics_track: LyricsTrack):
        """Set the lyrics track for the song."""
        self.lyrics_tracks.append(lyrics_track)

    def export(self, filename: str, fs: int = 44100):
        """Export the song to a WAV file."""
        midi_data = pretty_midi.PrettyMIDI(initial_tempo=self.tempo)
        instrument_audios = [track.synthesize(midi_data, fs, self.sf2_path) for track in self.instrument_tracks]
        midi_audio = np.sum(instrument_audios, axis=0)
        midi_audio /= np.max(np.abs(midi_audio))  # Normalize

        if self.lyrics_tracks:
            max_length = max(len(track.synthesize(fs)) for track in self.lyrics_tracks)
            lyrics_audios = [np.pad(track.synthesize(fs), (0, max_length - len(track.synthesize(fs))), mode='constant') for track in self.lyrics_tracks]
            lyrics_audio = np.sum(lyrics_audios, axis=0)
            lyrics_audio /= np.max(np.abs(lyrics_audio))  # Normalize
        else:
            lyrics_audio = np.zeros_like(midi_audio)

        # Ensure both arrays are of the same length
        max_length = max(len(midi_audio), len(lyrics_audio))
        midi_audio = np.pad(midi_audio, (0, max_length - len(midi_audio)), mode='constant')
        lyrics_audio = np.pad(lyrics_audio, (0, max_length - len(lyrics_audio)), mode='constant')

        mixed_audio = midi_audio + lyrics_audio
        mixed_audio /= np.max(np.abs(mixed_audio))  # Normalize

        mixed_audio_int16 = (mixed_audio * 32767).astype(np.int16)
        wav_write(filename, fs, mixed_audio_int16)

