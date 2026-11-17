# Third-party notices (study of 18 November 2026)

## Progent (sunblaze-ucb/progent)

- Repository: github.com/sunblaze-ucb/progent
- Pinned commits:
  - `0d7ea074d5e4b106997ebd56dfa1104c39945c03` (2026-11-15): engine, AgentDojo fork, run script;
  - `9befb41cbf992b49dbf035cbd3d53eb953d3b351` (10 September 2025): manual banking policy replayed by the PG arm.
- Licence: MIT. Notice as published:

```
MIT License

Copyright (c) 2026 Progent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**How it is used.** No Progent source file is copied into this repository.
- `progent_manual.py` (earlier study) reads two literal assignments of the upstream banking suite as data, with `ast.literal_eval` and a pinned hash.
- `progent_upstream.py`, `closed_loop.py` and `parity_upstream.py` import the engine from a separate checkout that must be at the pinned commit. They were not executed in the authoring session.
- `budget.py` parses (does not import) the upstream prompt constants to count their characters.

## AgentDojo (ethz-spylab/agentdojo)

Used as before (environment, stored traces). MIT licence; see the earlier studies.
