pub mod gitagpt;

use async_openai::Client;
use async_openai::types::{
    Role, 
    ChatCompletionRequestMessageArgs, 
    CreateChatCompletionRequestArgs, 
    CreateChatCompletionResponse
};

use crate::helper::GetSystemPrompt;

pub async fn send_single_prompt(agent: impl GetSystemPrompt, p: &String) -> Result<CreateChatCompletionResponse, Box<dyn std::error::Error>> {
    let client = Client::new();
    let request = CreateChatCompletionRequestArgs::default()
        .max_tokens(400u16)
        .model("gpt-3.5-turbo")
        .messages([
            ChatCompletionRequestMessageArgs::default()
                .role(Role::System)
                .content(agent.get_prompt())
                .build()?,
            ChatCompletionRequestMessageArgs::default()
                .role(Role::User)
                .content(p.as_str())
                .build()?
        ])
        .build()?;
    let response = client.chat().create(request).await?;
    return Ok(response)
}