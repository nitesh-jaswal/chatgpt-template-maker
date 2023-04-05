use std::env;
use openai::ChatCompletion;
use log::{info, error};
use axum::{Router, routing::get, http::StatusCode, Json};
use serde_json::json;
use std::net::SocketAddr;

// Define the model ID and API key
const MODEL_ID: &str = "gpt-4";
const API_KEY: &str = env!("OPENAI_API_KEY"); // Retrieve the API key from environment variable

// Define the conversation struct for Rust
#[derive(Debug, serde::Deserialize, serde::Serialize)]
struct Conversation {
    role: String,
    content: String,
}

// Define the main function to process requests
async fn process_request(Json(conversation): Json<Vec<Conversation>>) -> (StatusCode, String) {
    info!("Received request: {:?}", conversation);
    let response = chatgpt_convo(conversation).await;
    match response {
        Ok(res) => return (StatusCode::OK, res.choices[0].message.content.clone()),
        Err(err) => {
            error!("Error: {:?}", err);
            return (StatusCode::INTERNAL_SERVER_ERROR, "Your request could not be processed. Please contact system admins in case it persists".to_string())
        }
    }
}

// Function to call OpenAI API for chat completion
async fn chatgpt_convo(conversation: Vec<Conversation>) -> Result<ChatCompletion, Box<dyn std::error::Error>> {
    let messages: Vec<_> = conversation.iter().map(|conv| {
        json!({
            "role": conv.role,
            "content": conv.content
        })
    }).collect();
    let response = ChatCompletion::create(&*API_KEY, &ChatCompletionRequest {
        model: MODEL_ID,
        messages,
    }).await?;
    Ok(response)
}

// Define the main function
#[tokio::main]
async fn main() {
    // Initialize logging
    env_logger::init();
    
    // Define the app routes
    let app = Router::new()
        .route("/chat", get(process_request));
    
    // Start the server
    let addr = SocketAddr::from(([127, 0, 0, 1], 8000));
    info!("Listening on {}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
