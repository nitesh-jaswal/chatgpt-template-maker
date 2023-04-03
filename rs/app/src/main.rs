use axum::{
    routing::get,
    http::StatusCode,
    Json, Router
};
use std::net::SocketAddr;

use cli::templates::send_single_prompt;
use cli::templates::gitagpt::{
    GitaGPTFlavours,
    GitaGPTResponse,
    GitaGPTRequest,
};
use cli::helper::ProcessResponse;


async fn process_gitagpt_krishna_request(Json(r): Json<GitaGPTRequest>) -> (StatusCode, String) {
    tracing::info!("Reveived request {:?}", r);
    let response = send_single_prompt(GitaGPTFlavours::Krishna, &r.query).await;
    match response {
        Ok(res) => return GitaGPTResponse::process_response(&res),
        Err(err) => {
            tracing::error!("[ERROR] {:?}", err);
            return (StatusCode::INTERNAL_SERVER_ERROR, "Your request could not be processed. Please contact system admins in case it persists".to_string())
        }
    }
}

// TODO: 
// Run clippy and fix things
// Add tiktoken token counting, to estimate and keep a track of token usage
// Automatically append EndSession
// Better errors
#[tokio::main] 
async fn main() {
    tracing_subscriber::fmt::init();
    let app = Router::new()
        .route("/single_prompt/gitagpt/krishna", get(process_gitagpt_krishna_request));
    
    let addr = SocketAddr::from(([127, 0, 0, 1], 8001));
    
    tracing::info!("Listening on {}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}