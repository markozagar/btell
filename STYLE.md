# Coding Style

## Why?

If code by all authors looks approximately the same and uses the same style, it will be easier to read and review.

## Basics

The style guide is loosely based on Google's [Python Style Guide](https://google.github.io/styleguide/pyguide.html#4-parting-words).
Exceptions and deviations are noted below.

## Exceptions and Deviations

### 2.17 Function and Method Decorators

Decorators for functions and methods are generally allowed. In particular, a lot of Django's functionality is expressed
through decorators, and it is preferrable to use those rather than reinvent common functionality. It is also okay
to use `staticmethod` and `classmethod` where appropriate, with the following provision:

* `staticmethod` is allowed if it returns an instance of the containing class. Otherwise, prefer to use a standalone function
  in the same module.
* `classmethod` is allowed if it uses class variables. If not, prefer to use `staticmethod` or a standalone function.

Writing new decorators should be carefully considered.

### 3.2 Line length

Line length is not strictly enforced and lines can be any length. Prefer shorter lines and aim to stay below ~100
characters to allow easier side-by-side comparisons in code diffs, but going a few characters over is preferred
over awkward line breaks.


## Conclusion

The style is not strictly enforced for pull requests, but large deviations may be noted and the reviewer may request
changes to keep the codebase as consistent as possible.
