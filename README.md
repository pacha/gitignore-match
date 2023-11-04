<p align="center">
    <img src="https://raw.githubusercontent.com/pacha/py-walk/main/docs/logo-header.png" alt="logo">
</p>

py-walk
=======

![Tests](https://github.com/pacha/py-walk/actions/workflows/tests.yaml/badge.svg)
![Type checks](https://github.com/pacha/py-walk/actions/workflows/type-checks.yaml/badge.svg)
![Code formatting](https://github.com/pacha/py-walk/actions/workflows/code-formatting.yaml/badge.svg)
![Supported Python versions](https://img.shields.io/pypi/pyversions/py-walk.svg)

_Python library to filter filesystem paths based on gitignore-like patterns._

Example:
```
from py_walk import walk

ignore = """
    **/data/*.bin

    # python files
    __pycache__/
    *.py[cod]
"""

for path in walk("some/directory", ignore=ignore):
    do_something(path)
```

py-walk can be useful for applications or tools that work with paths and aim to
offer a `.gitignore` type file to their users. It's also handy for users working
in interactive sessions who need to quickly retrieve sets of paths that must
meet relatively complex constraints.

> py-walk tries to achieve 100% compatibility with Git's gitignore (wildmatch)
> pattern syntax. Currently, it includes more than 500 tests, which incorporate
> all the original tests from the Git codebase. These tests are executed against
> `git check-ignore` to ensure as much compatibility as possible. If you find
> any divergence, please don't hesitate to open an issue or a PR.

## Installation

To install py-walk, simply use `pip`:
```shell
$ pip install py-walk
```

## Usage

With Py-Walk, you have the ability to input paths into the library to determine
whether they match with a set of gitignore-based patterns. Alternatively, you
can directly traverse the contents of a directory, based on a set of conditions
that the paths must meet.

### walk

To walk through all the contents of a directory, don't provide any constraints:
```
from py-walk import walk

for path in walk("/some/directory/"):
    print(path)
```
`walk` accepts the directory to traverse as a strings or as a `Path` object from
`pathlib`. It returns `Path` objects.

> `walk` returns a generator, if you prefer to get the results as a list or
> tuple, wrap the call with the desired data type constructor
> (eg. `list(walk("some-dir"))`).

To ignore certain paths, you can pass patterns as a text or a list of patterns:
```
ignore = """
    # these patterns use gitignore syntax
    foo.txt
    /bar/**/*.dat
"""

for path in walk("/some/directory", ignore=ignore):
    ...
```
or
```
ignore = ["foo.txt", "/bar/**/*.dat"]
for path in walk("/some/directory", ignore=ignore):
    ...
```

To only retrieve paths that match a set of patterns, use the `match` parameter
(again, passing a text blob or a list of patterns):
```
for path in walk("/some/directory", ignore=["data/"], match=["*.css", "*.js"]):
    ...
```
> Note that the `ignore` parameter has precedence: once a path is ignored it
> can't be reincluded using the `match` parameter due to performance reasons.
> That includes children of ignored directories. For example, if you ignore
> a directory "/foo/", "/foo/bar/file.txt" will be ignored even if `match`
> includes the "*.txt" pattern.

In addition, you can retrieve either only files or only directories using the
`mode` parameter:
```
for path in walk("/some/directory", ignore=["static/"], mode="only-files"):
    ...
```
```
for path in walk("/some/directory", ignore=["static/"], mode="only-dirs"):
    ...
```

You can combine `ignore`, `match` and `mode` to get the exact list of files
that you need. However, always remember that `ignore` takes precedence over the
other two.

> Note: you can convert any text containing gitignore-based patterns into a list using
> the `py_walk.pattern_text_to_pattern_list` function:
> ```
> from py_walk import pattern_text_to_pattern_list
>
> pattern_list = pattern_text_to_pattern_list("""
>     # some patterns
>     **/foo.txt
>     dir[A-Z]/
> """)

### get_parser_from_*

You can also create a parser from a gitignore-type text, a list of patterns or
a file handle to a `.gitignore` type of file. Using the `match` method of the
parser, you can directly evaluate paths.

```python
from py_walk import get_parser_from_file

parser = get_parser_from_file("path/to/gitignore-type-file")
if parser.match("file.txt"):
    print("file.txt matches!")
```

```python
from py_walk import get_parser_from_text

patterns = """
# some comment
*.txt
**/bar/*.dat
"""

parser = get_parser_from_text(patterns, base_dir="/some/folder")
if parser.match("file.txt"):
    print("file.txt matches!")
```

```python
from py_walk import get_parser_from_list

patterns = [
    "*.txt",
    "**/bar/*.dat",
]

parser = get_parser_from_list(patterns, base_dir="/some/folder")
if parser.match("file.txt"):
    ...
```

The `match` method requires either a string or a `Path` object, which must
always be defined relative to a `base_dir`. This `base_dir` represents the
directory where the files are stored. When using `get_parser_from_file`, the
`base_dir` is established based on the location of the gitignore-type file,
mirroring the functionality of an actual `.gitignore` file within a Git
repository. However, when using `get_parser_from_text` or
`get_parser_from_list`, you'll need to manually provide the `base_dir` as a
parameter.

> Note: it is possible to check non-existing paths using the parser,
> however, it needs a `base_dir` to replicate the behavior of Git,
> which checks the actual filesystem to determine some of the matches.

