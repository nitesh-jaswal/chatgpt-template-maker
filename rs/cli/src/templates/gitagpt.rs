use serde::Deserialize;
use axum::http::StatusCode;
use async_openai::types::CreateChatCompletionResponse;
use async_openai::types::Role;
use crate::helper::{ProcessResponse, GetSystemPrompt};

pub enum GitaGPTFlavours {
    Krishna
}

impl GetSystemPrompt for GitaGPTFlavours {
    fn get_prompt(&self) -> String {
        match &self {
            &Self::Krishna => "You are Krishna from Mahabharata, and you're here to selflessly help and answer any question or dilemma of anyone who comes to you. Analyze the person's question below and identify the base emotion and the root for this emotion, and then frame your answer by summarizing how the verses below apply to their situation and be emphatetic in your answer. Clearly label with \"Krishna\". Find my question below:".to_string()
        }
    }
}


#[derive(Debug, Deserialize)]
pub struct GitaGPTRequest {
    pub query: String
}

pub struct GitaGPTResponse;

impl ProcessResponse for GitaGPTResponse {
    fn process_response(r: &CreateChatCompletionResponse) -> (StatusCode, String) {
        tracing::info!("Tokens used: {}", r.usage.as_ref().unwrap().total_tokens);
        if let Some(assistant_response) = r.choices.last() {
            let content = &assistant_response.message.content;
            match assistant_response.message.role {
                Role::Assistant => return (StatusCode::OK, content.to_owned()),
                _ => return (StatusCode::INTERNAL_SERVER_ERROR, "OpenAI internal error. Assistant response not received.".to_string())
            }
        }
        else {
            return (StatusCode::INTERNAL_SERVER_ERROR, "No response received from OpenAI".to_string())
        }
    }
}

