use axum::{
    routing::get,
    http::StatusCode,
    response::IntoResponse,
    Json, Router
};
use std::net::SocketAddr;
use async_openai::Chat;
use async_openai::Client;
use async_openai::types::{Role, ChatCompletionRequestMessageArgs, CreateChatCompletionRequestArgs, CreateChatCompletionResponse};
use serde::{Serialize, Deserialize};
use std::error::Error;
use log;


#[derive(Debug, Deserialize)]
struct EventsRequest {
    events: Vec<String>
}

struct NoTaker {
    client: Client,
    system_prompt: String
}

impl NoTaker {
    async fn send_events(&self, events: &EventsRequest) -> Result<CreateChatCompletionResponse, Box<dyn Error>> {
        let events = events.events.join("\n");
        let request = CreateChatCompletionRequestArgs::default()
            .max_tokens(200u16)
            .model("gpt-3.5-turbo")
            .messages([
                ChatCompletionRequestMessageArgs::default()
                    .role(Role::System)
                    .content(self.system_prompt.as_str())
                    .build()?,
                ChatCompletionRequestMessageArgs::default()
                    .role(Role::User)
                    .content(events.as_str())
                    .build()?
            ])
            .build()?;
        let response = self.client.chat().create(request).await?;
        return Ok(response)
    }
}

async fn process_events(Json(events_request): Json<EventsRequest>) -> (StatusCode, String) {
    tracing::info!("Reveived request {:?}", events_request);
    let notaker = NoTaker{
        client: Client::new(),
        // system_prompt: "Your task is to `Take Meeting Notes`. I will list events that will be occouring in the meeting in the form of CamelCase \"phrases\" in English. The format of the events will be like that of Rust Enums. The events may sometimes carry some metadata about the event itself. Which will be available in a `key=value` pair format. For example: GoalsCompleted(total_count=5,completed_count=2(issue_a issue_c),discarded=(1 issue_b),did_not_complete=(2 issue_d issue_e)). There can be multiple events in a single message. But each event will only be on a single line. You will not give a response. Just an acknowledgement of receiving the event. You will acknowledge with `Ack <number_of_events_in_consumed_message>`. As soon as you encounter the `EndSession` event. You will provide a listed summary with description of all the events that happened.".to_string()
        system_prompt: "You are Krishna from Mahabharata, and you're here to selflessly help and answer any question or dilemma of anyone who comes to you. Analyze the person's question below and identify the base emotion and the root for this emotion, and then frame your answer by summarizing how the verses below apply to their situation and be emphatetic in your answer. Clearly label with \"Krishna\". Find my question below:".to_string()
    };
    let response = notaker.send_events(&events_request).await;
    match response {
        Ok(res) => {
            
            log::info!("usage: {}", res.usage.unwrap().total_tokens);
            if let Some(assistant_response) = res.choices.last() {
                let content = &assistant_response.message.content;
                match assistant_response.message.role {
                    Role::Assistant => return (StatusCode::OK, content.to_owned()),
                    _ => return (StatusCode::INTERNAL_SERVER_ERROR, "OpenAI internal error. Assistant response not received 1.".to_string())
                }
            }
            else {
                return (StatusCode::INTERNAL_SERVER_ERROR, "OpenAI internal error. Assistant response not received 2.".to_string())

            }
        },
        Err(err) => {
            println!("Encountered error: {:?}", err);
            return (StatusCode::INTERNAL_SERVER_ERROR, "OpenAI internal error. Assistant response not received 3.".to_string())

        }
        
    }


}

// TODO: 
// Add tiktoken token counting, to estimate and keep a track of token usage
// Automatically append EndSession
// Better errors
#[tokio::main] 
async fn main() {
    // femme::start();
    tracing_subscriber::fmt::init();
    let app = Router::new()
        .route("/", get(process_events));

    let addr = SocketAddr::from(([127, 0, 0, 1], 8001));
    tracing::debug!("Listening on {}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
  