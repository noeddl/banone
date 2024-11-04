# banone

This is a fun project for generating (currently only German) joke riddles of the following form:

```
Was ist gelb, krumm und kann schießen?
Eine Banone.
```

Each riddle consists of a question asking for an object or a creature with certain features which usually includes a color and one or two other traits. The question above can be translated as *What is yellow, crooked and can shoot?*. The answer to such riddles is always a word combined of two words that have some phonetic resemblance. In the example above, *Banone* is a combination of the words *Banane (banana)* and *Kanone (cannon, gun)*.

The generation process basically consists of two steps:

1. Find words that somehow overlap phonetically and can be combined into a new compound word.
2. Generate a question that combines some prototypical features describing the words used for forming the compound.

Both is done with the help of a dictionary listing words and information about how they are pronounced together with some characteristic features of the thing or creature they denote. For example, the entry for the word *Banane* looks like this:

```
Banane:
    phon: "ba-'na:-n@"
    pos: NN
    determiner: eine
    color: gelb
    property: krumm
```

The phonetic transcription is given in [SAMPA](https://en.wikipedia.org/wiki/SAMPA) notation.

One goal of this project is to explore what it takes to create a *good* (i.e. funny or interesting) pun of this kind. The main goal, however, is to have some fun with language and programming.

## Status

Ironically, even though the project is called `banone` the generator is not yet able to create the word *Banone* (see the first joke riddle shown above). As it turned out this is a special case of the type of joke riddles I want to generate.

Let's take a look at an example that already works.

```
Was ist braun, gefährlich und schwimmt im Wasser?
Ein Schokodil.
```

*What is brown, dangerous and swims in the water?*</br>
*Schokodil = schoko (chocolate) + Krokodil (crocodile)*

This is quite easy to generate because of the obvious overlap of the two words (in this case both in sound and spelling).

```
sch[oko]
 Kr[oko]dil
```

In many cases, the different spellings of two words do not match as nicely but their pronounciations actually do. Therefore, the generator uses the phonetic transcriptions of the words to be combined so that it can easily handle variations in spelling.

```
Was ist rot, fruchtig und macht nur Ärger?
Eine Schlimmbeere.
```

*What is red, fruity and causes a lot of trouble?*</br>
*Schlimmbeere = schlimm (bad, evil) + Himbeere (raspberry)*

Both the words *schlimm* and *Himbeere* contain a short *i* which is marked with double *m* in *schlimm* but not in *Himbeere*.

```
schl[imm]
   H[im_]beere
```

This is not a problem when comparing the phonetic transcriptions of the words.

```
'Sl[Im]
 'h[Im]-be:-R@
```

Another, more advanced example:

```
Was ist niedlich, hoppelt über die Wiese und qualmt?
Ein Kaminchen.
```

*What is cute, hops over the meadow and smokes?*</br>
*Kaminchen = Kamin (fireplace, chimney) + Kaninchen (rabbit)*

This is more advanced because the overlap involves the change of a consonant (from *n* to *m*).

```
[Ka|m|in]
[Ka|n|in]chen
```

The creation of *Banone* from *Banane* and *Kanone* involves the change of a vowel (from *a* to *o*) that is not implemented yet.

```
K[an|o|ne]
B[an|a|ne]
```

## Requirements

1. Python 3.9+
2. [Poetry](https://github.com/sdispater/poetry) for dependency management and packaging. Install with `pip install poetry`.

## Build and run

```
poetry install
poetry build
```

Now you can generate all currently possible riddles.

```
banone-run
```

## Development and unit tests

`banone` comes with some [pre-commit](https://pre-commit.com/) hooks for easy validation and formatting. After cloning the repo and building the project, run

```
pre-commit install
```

From now on, the pre-commit hooks will be run on every commit.

`banone` has a test suite that can be run as follows:

```
pytest
```
