use tide::Request;

async fn hello_world(req: Request<()>) -> tide::Result<String> {
    Ok("Hello, world!".to_string())
}

#[async_std::main] 
async fn main() -> tide::Result<()> {
    let mut app = tide::new();

    app.at("/").get(hello_world);

    app.listen("0.0.0.0:8001").await?;

    Ok(())
}
