TCP-Like Protocol Simulation with Sliding Window & Retransmissions

Overview

This project simulates a simplified TCP-like protocol for reliable data transmission. It uses a client-server architecture to ensure efficient and orderly communication with key mechanisms like sliding window, segmentation, acknowledgments (ACKs), timeout-based retransmissions, and out-of-order handling. The project is designed to handle real-world challenges like packet loss, disorder, and delays while providing packet-level analysis through .pcapng files.

Features
	•	Sliding Window Protocol: Ensures controlled data flow between client and server.
	•	Timeout and Retransmissions: Handles packet loss and ensures message delivery.
	•	Segmentation and Reassembly: Splits large messages into smaller packets for transmission.
	•	Out-of-Order Packet Handling: Buffers packets to maintain correct sequence.
	•	Configurable Parameters:
	•	Message size
	•	Window size
	•	Timeout duration
	•	Packet-Level Analysis: Provides .pcapng files for deeper insights into communication behavior.

Requirements
	•	Python 3.6 or higher
	•	Wireshark (optional, for packet analysis)

Files
	•	client.py: Client-side implementation of the protocol.
	•	server.py: Server-side implementation of the protocol.
	•	.pcapng Files: Packet captures for analyzing communication scenarios.
	•	input.txt: Configurable parameters like message size, window size, and timeout.
	•	Assignment3-Report.pdf: Detailed documentation of the implementation and analysis.

How to Run
	1.	Clone the Repository:

git clone [https://github.com/your-repo-name.git](https://github.com/baruhifraimov/TCP-Like-Protocol-Simulation-with-Sliding-Window---Retransmissions.git)

	2.	Start the Server:

python server.py


	3.	Run the Client:

python client.py


	4.	Configure Parameters:
	•	Choose between manual input or reading from input.txt.
	5.	Analyze Communication:
	•	Use .pcapng files with Wireshark for detailed analysis.

Examples

Example Input (input.txt):

message:"DOR AND BARUH LOVE PIGS"
maximum_msg_size:5
window_size:5
timeout:5

Example Workflow:
	•	The client sends a message, splitting it into packets based on the maximum_msg_size.
	•	The server acknowledges received packets, handling out-of-order and lost packets.
	•	Retransmissions are triggered if timeouts occur.

Use Cases
	•	Learn and understand TCP fundamentals.
	•	Simulate network scenarios like packet loss, reordering, and timeouts.
	•	Analyze packet behavior using Wireshark.

Contributors
	•	Baruh Ifraimov
	•	Dor Cohen

License

This project is licensed under the MIT License. See the LICENSE file for details.
