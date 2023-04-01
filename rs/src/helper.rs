use async_openai::types::CreateChatCompletionResponse;
use axum::http::StatusCode;

pub trait ProcessResponse {
    fn process_response(r: &CreateChatCompletionResponse) -> (StatusCode, String);
}

pub trait GetSystemPrompt {
    fn get_prompt(&self) -> String;
}