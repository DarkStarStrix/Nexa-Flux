use clap::{App, Arg};
use std::process::Command;

fn main() {
    let matches = App::new("Python CLI")
        .version("1.0")
        .author("Your Name <your.email@example.com>")
        .about("Executes Python scripts")
        .arg(
            Arg::new("script")
                .about("The Python script to execute")
                .required(true)
                .index(1),
        )
        .get_matches();

    let script = matches.value_of("script").unwrap();

    let output = Command::new("python")
        .arg(script)
        .output()
        .expect("Failed to execute command");

    println!("Output: {}", String::from_utf8_lossy(&output.stdout));
}
