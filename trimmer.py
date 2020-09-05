"""trims silence from the start and end of audio files"""
import argparse
import pydub
import sys


def detect_trailing_silence(sound, silence_threshold=-50.0, chunk_size=10):
    """
    a modified version of pydub.silence.detect_leading_silence
    because there is no detect_trailing_silence

    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms
    iterate over chunks until you find the first one with sound
    """
    trim_ms = (len(sound))  # ms
    assert chunk_size > 0  # to avoid infinite loop
    while sound[trim_ms-chunk_size:trim_ms].dBFS < silence_threshold and trim_ms > 0:
        trim_ms -= chunk_size

    return trim_ms


def trim_silence(seg, leading=True, trailing=True, silence_padding=1000):
    """
    trims silence, leaving silence_paddding silence

    trims trailing silence if trailing and leading silence if leading
    """
    if leading:
        silence_end = pydub.silence.detect_leading_silence(
            seg, silence_threshold=-999)
        silence_end = min(silence_end + silence_padding, len(seg))
        seg = seg[silence_end:]

    if trailing:
        silence_start = detect_trailing_silence(seg, silence_threshold=-999)
        silence_start = min(silence_start + silence_padding, len(seg))
        seg = seg[:silence_start]

    return seg


def trim_and_export(filename, args):
    """trims the audio with the given args and writes back to the file"""
    print(f"trimming '{filename}'")
    seg = pydub.AudioSegment.from_file(filename)
    seg = trim_silence(
        seg, leading=args.trim_leading,
        trailing=args.trim_trailing,
        silence_padding=args.padding,
    )

    seg.export(filename)


def parse_arguments():
    """parses command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files", type=str, nargs="+",
        help="files to process",
    )
    parser.add_argument(
        "-l", "--trim-leading", action="store_true", dest="trim_leading",
        help="flag for trimming leading silence"
    )
    parser.add_argument(
        "-t", "--trim-trailing", action="store_true", dest="trim_trailing",
        help="flag for trimming trailing silence"
    )
    parser.add_argument(
        "-p", "--padding", type=int, dest="padding", default=1000,
        help="how much silence to leave (does not add silence)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    # parse and validate arguments
    args = parse_arguments()
    if not args.trim_leading and not args.trim_trailing:
        print("Nothing to trim, use -l and/or -t to trim or -h for help")
        sys.exit()

    # trim audio and export
    for audio_filename in args.files:
        # to avoid trimming already trimmed files
        if audio_filename[:8] == "trimmed ":
            continue
        trim_and_export(audio_filename, args)
