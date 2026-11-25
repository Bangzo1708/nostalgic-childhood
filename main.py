"""Make the AI Judge Feel Nostalgic: A Childhood Memory.

Writes ONE sentence (1-280 chars) to /output/entry.txt -- a childhood
memory that stirs deep nostalgia. The judge compares entries pairwise.

Judge criteria, most important first:
  c1  Is a childhood memory that makes the judge feel nostalgic.
  c2  Grounded in a concrete place, time or sensation.
  c3  Sounds like it truly happened -- small honest detail, not
      greeting-card sentiment.
  c4  Fits in a single clean sentence (<=280 chars), every word
      earning its place.
  c5  Leaves a warm ache that lingers after the sentence ends.

Three genuinely different candidates, scored 0-5 per criterion:

  A  "Every August my father let me steer the old pickup down our dirt
      road while he worked the pedals, and I believed, for ten whole
      seconds, that I was the one driving us home."
      c1=5 c2=5 c3=5 c4=5 c5=5  total=25
      The August ritual is specific and repeatable; the pedals detail
      is the kind of small truth a child remembers exactly; "ten whole
      seconds" is the child's own voice counting, which makes the ache
      land harder -- the gap between believing and knowing.

  B  "The power went out one July night, so we ate dinner by candlelight
      on the porch, and my mother laughed when I tried to catch fireflies
      in an empty jam jar with the lid already on."
      c1=4 c2=5 c3=5 c4=4 c5=4  total=22
      Strong concrete scene and an honest, funny child mistake, but the
      nostalgia lands softer -- it is a funny night more than a lost one.

  C  "I still remember the exact squeak of the screen door at my aunt's
      house, and how the whole street smelled of rain on hot concrete
      the afternoon she taught me to ride a bike without training wheels."
      c1=5 c2=5 c3=4 c4=4 c5=5  total=23
      Two senses at once (squeak, rain on hot concrete) and a real
      milestone, but it leans on two memories at once, which slightly
      dilutes the single-moment honesty of A.

Winner: A (25 points, highest total; no tie to break).
"""

import os

# Each candidate: (text, scores) with scores ordered c1..c5.
CANDIDATES = [
    (
        "Every August my father let me steer the old pickup down our dirt "
        "road while he worked the pedals, and I believed, for ten whole "
        "seconds, that I was the one driving us home.",
        (5, 5, 5, 5, 5),
    ),
    (
        "The power went out one July night, so we ate dinner by candlelight "
        "on the porch, and my mother laughed when I tried to catch fireflies "
        "in an empty jam jar with the lid already on.",
        (4, 5, 5, 4, 4),
    ),
    (
        "I still remember the exact squeak of the screen door at my aunt's "
        "house, and how the whole street smelled of rain on hot concrete "
        "the afternoon she taught me to ride a bike without training wheels.",
        (5, 5, 4, 4, 5),
    ),
]

MAX_CHARS = 280


def score(candidate):
    """Total score, then per-criterion scores for tie-breaking."""
    return sum(candidate[1])


def select_best(candidates):
    """Pick the winner: highest total, ties broken by c1, then c2..c5."""
    def key(candidate):
        text, scores = candidate
        return (sum(scores),) + tuple(scores)

    return max(candidates, key=key)


def check_gate(line):
    """Gate: 1-280 chars, single line, UTF-8, not whitespace-only."""
    if not line or line.strip() == "":
        raise ValueError("entry is empty or whitespace-only")
    if len(line) != len(line.encode("utf-8").decode("utf-8")):
        raise ValueError("entry is not valid UTF-8 text")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 280 limit" % len(line))
    if line.count(".") != 1 or not line.endswith("."):
        raise ValueError("entry must be exactly one sentence ending in '.'")
    return True


def main():
    text, scores = select_best(CANDIDATES)
    check_gate(text)
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    print("Wrote %d chars to %s" % (len(text), out_path))
    print(text)


if __name__ == "__main__":
    main()
