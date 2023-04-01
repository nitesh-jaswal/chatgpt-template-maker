# ChatGPT based Template Maker

## Note:
You need to save the `OPENAI_API_KEY` and optionally `OPENAI_ORGANIZATION` as environment variables for this to work

## Python
This version is a work in progress and is currently in a broken state.

## Rust
You need to run the following commands from the rs directory: `cd rs`
1. Install Rust  
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

2. Install dependancies
```bash
cargo build
```

3. Run server
```bash
cargo run
```

The request/response model of the api is simple for the single_prompt endpoint. You need to send a string prompt as a GET request. You will get a single string response back.  Currently the response limit is capped at 200 tokens
```bash
curl -X GET -H "Content-Type: application/json" -d '{"query": "Sample user prompt"}' 127.0.0.1:8001/single_prompt/gitagpt/krishna
```


# SPIKE

1. Use langchain?