use async_openai::types::CreateChatCompletionResponse;
use axum::http::StatusCode;

// TODO: Rename traits as a Property rather than Action -> https://www.reddit.com/r/learnrust/comments/128bsj8/naming_traits/
pub trait ProcessResponse {
    fn process_response(r: &CreateChatCompletionResponse) -> (StatusCode, String);
}

pub trait GetSystemPrompt {
    fn get_prompt(&self) -> String;
}