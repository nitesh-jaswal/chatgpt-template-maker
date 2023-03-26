use tide::Request;
use tide::Response;
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
            .model("gpt-3,5-turbo")
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

async fn process_events(mut req: Request<()>) -> tide::Result<String> {
    let events_request: EventsRequest = req.body_json().await?;
    log::info!("Reveived request {:?}", events_request);
    let notaker = NoTaker{
        client: Client::new(),
        system_prompt: "Your task is to `Take Meeting Notes`. I will list events that will be occouring in the meeting in the form of CamelCase \"phrases\" in English. The format of the events will be like that of Rust Enums. The events may sometimes carry some metadata about the event itself. Which will be available in a `key=value` pair format. For example: GoalsCompleted(total_count=5,completed_count=2(issue_a issue_c),discarded=(1 issue_b),did_not_complete=(2 issue_d issue_e)). There can be multiple events in a single message. But each event will only be on a single line. You will not give a response. Just an acknowledgement of receiving the event. You will acknowledge with `Ack <number_of_events_in_consumed_message>`. As soon as you encounter the `EndSession` event. You will provide a listed summary with description of all the events that happened.".to_string()
    };
    let response = notaker.send_events(&events_request).await;
    match response {
        Ok(res) => {
            if let Some(assistant_response) = res.choices.last() {
                let content = &assistant_response.message.content;
                match assistant_response.message.role {
                    Role::Assistant => return Ok(content.to_owned()),
                    _ => return Err(tide::Error::from_str(500, "OpenAI internal error. Assistant response not received."))
                }
            }
            else {
                return Err(tide::Error::from_str(500, "OpenAI internal error. Assistant response not received."))
            }
        },
        Err(err) => {
            println!("Encountered error: {:?}", err);
            return Err(tide::Error::from_str(500, "Could not process request"))
        }
        
    }


}

#[tokio::main] 
async fn main() -> tide::Result<()> {
    femme::start();
    let mut app = tide::new();
    app.at("/").get(process_events);
    app.listen("0.0.0.0:8001").await?;
    Ok(())
}
  