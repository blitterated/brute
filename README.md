# Local AI on Apple Silicon

Rude and mental harness. Not a gent, a brute.

Based on a [Tech with Tim Tutorial](https://www.youtube.com/watch?v=c9AnqCeyxbI).


## Setup the Python Project

### Initialize the project directory

```sh
uv init --no-readme --name brute --description "Rude and mental harness. Not a gent, a brute."
```

```text
Initialized project `brute`
```


### Install the OpenAI API lib

```sh
uv add openai
```

```text
Using CPython 3.14.7
Creating virtual environment at: .venv
Resolved 16 packages in 295ms
      Built brute @ file:///Users/d0rk/Development/blitterated/brute/src                                                Prepared 4 packages in 239ms                                                                                            Installed 15 packages in 16ms                                                                                            + annotated-types==0.8.0                                                                                                + anyio==4.15.1
 + brute==0.1.0 (from file:///Users/d0rk/Development/blitterated/brute/src)
 + h11==0.16.0
 + httpcore2==2.13.1
 + httpx2==2.13.1
 + idna==3.20
 + jiter==0.17.0
 + openai==3.19.2
 + pydantic==2.13.5
 + pydantic-core==2.46.5
 + sniffio==1.3.1
 + truststore==0.10.4
 + typing-extensions==4.16.0
 + typing-inspection==0.4.4
 ```
